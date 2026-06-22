import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Import helper functions from your project configuration
from helpers import apology, login_required, call_ai_risk_engine

# Configure application
app = Flask(__name__)

# Configure session infrastructure to use filesystem storage
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize database using the CS50 engine
db = SQL("sqlite:///database.db")


@app.after_request
def after_request(response):
    """Ensure browser caching doesn't mask interface state changes"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Main Risk Management Portfolio Dashboard"""
    user_id = session["user_id"]

    # Query summary metrics for user's assets and corresponding open vulnerabilities
    assets_summary = db.execute(
        "SELECT a.*, COUNT(v.id) AS open_vulns, AVG(v.risk_score) AS avg_risk "
        "FROM assets a LEFT JOIN vulnerabilities v ON a.id = v.asset_id AND v.status = 'Open' "
        "WHERE a.user_id = ? GROUP BY a.id",
        user_id
    )

    return render_template("index.html", assets=assets_summary)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("must provide username and passwords", 400)
        if password != confirmation:
            return apology("passwords must match", 400)

        try:
            password_hash = generate_password_hash(password)
            user_id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username, password_hash
            )
        except ValueError:
            return apology("username already exists", 400)

        session["user_id"] = user_id
        flash("Registration complete!")
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("must provide username and password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/asset/add", methods=["GET", "POST"])
@login_required
def add_asset():
    """Log an enterprise infrastructure asset into inventory"""
    if request.method == "POST":
        name = request.form.get("name")
        asset_type = request.form.get("asset_type")
        criticality = request.form.get("criticality")

        if not name or not asset_type or not criticality:
            return apology("missing asset payload parameters", 400)

        db.execute(
            "INSERT INTO assets (user_id, name, asset_type, criticality) VALUES (?, ?, ?, ?)",
            session["user_id"], name, asset_type, criticality
        )
        flash("Asset successfully added to registry portfolio!")
        return redirect("/")
    else:
        return render_template("add_asset.html")


@app.route("/assess", methods=["GET", "POST"])
@login_required
def assess_vulnerability():
    """Submit a vulnerability to be audited by the AI analysis engine"""
    user_id = session["user_id"]

    if request.method == "POST":
        asset_id = request.form.get("asset_id")
        title = request.form.get("title")
        description = request.form.get("description")
        severity = request.form.get("severity")

        if not asset_id or not title or not description or not severity:
            return apology("missing assessment data fields", 400)

        # Verify user ownership of targeted asset
        asset_check = db.execute("SELECT id FROM assets WHERE id = ? AND user_id = ?", asset_id, user_id)
        if not asset_check:
            return apology("unauthorized asset lookup access", 403)

        # 1. Fire up the LLM Prompt Routing Wrapper
        ai_data = call_ai_risk_engine(title, description, severity)

        # 2. Extract standard values and commit the threat profile record
        vuln_id = db.execute(
            "INSERT INTO vulnerabilities (asset_id, title, description, severity, risk_score, ai_analysis_summary) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            asset_id, title, description, severity, ai_data["risk_score"], ai_data["summary"]
        )

        # 3. Dissect JSON array elements returned by AI to build compliance checklist entries
        for control in ai_data["suggested_controls"]:
            db.execute(
                "INSERT INTO implemented_controls (vulnerability_id, framework_standard, control_id, control_name, remediation_steps) "
                "VALUES (?, ?, ?, ?, ?)",
                vuln_id, control["framework"], control["id"], control["name"], control["steps"]
            )

        flash("Vulnerability successfully processed and mapped to control layers!")
        return redirect(f"/vulnerability/{vuln_id}")
    else:
        user_assets = db.execute("SELECT id, name FROM assets WHERE user_id = ?", user_id)
        return render_template("assess.html", assets=user_assets)


@app.route("/vulnerability/<int:vuln_id>")
@login_required
def view_vulnerability(vuln_id):
    """Inspect specific threat context and its implementation checklist"""
    user_id = session["user_id"]

    # Secure row retrieval via cross-table structural verification
    vuln = db.execute(
        "SELECT v.*, a.name AS asset_name FROM vulnerabilities v JOIN assets a ON v.asset_id = a.id "
        "WHERE v.id = ? AND a.user_id = ?", vuln_id, user_id
    )
    if not vuln:
        return apology("vulnerability records not found", 404)

    controls = db.execute("SELECT * FROM implemented_controls WHERE vulnerability_id = ?", vuln_id)
    return render_template("view_vuln.html", vulnerability=vuln[0], controls=controls)


@app.route("/control/toggle", methods=["POST"])
@login_required
def toggle_control():
    """Asynchronous AJAX Endpoint to check off control elements on the fly"""
    user_id = session["user_id"]
    data = request.get_json()
    control_id = data.get("id")
    current_state = data.get("state") # 1 for complete, 0 for incomplete

    # Cross-verify user session holds authority over the linked asset data pool
    auth_check = db.execute(
        "SELECT c.id FROM implemented_controls c "
        "JOIN vulnerabilities v ON c.vulnerability_id = v.id "
        "JOIN assets a ON v.asset_id = a.id "
        "WHERE c.id = ? AND a.user_id = ?", control_id, user_id
    )
    if not auth_check:
        return jsonify({"error": "unauthorized parameter transaction"}), 403

    # Toggle state matching incoming check indicator
    db.execute("UPDATE implemented_controls SET is_implemented = ? WHERE id = ?", current_state, control_id)

    return jsonify({"success": True})
