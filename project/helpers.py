import os
import json
from flask import render_template, session, redirect
from functools import wraps
import google.generativeai as genai  # or use standard openai import patterns

def login_required(f):
    """Wrap routes to ensure standard login restrictions apply"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def apology(message, code=400):
    """Render error messages securely to client displays"""
    return render_template("apology.html", top=code, bottom=message), code

def call_ai_risk_engine(title, description, severity):
    """Queries AI API to derive architectural metrics and precise JSON objects"""

    # Configure API access token strings securely from system environments
    # genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

    system_prompt = (
        "You are an elite expert cybersecurity risk modeling engine specializing in NIST SP 800-53 and ISO 27001.\n"
        "Analyze the threat payload provided and output strict raw JSON matching this structure exactly. "
        "Do not wrap output strings in markdown blocks.\n"
        "Required Schema Structure:\n"
        "{\n"
        '  "risk_score": 7.5,\n'
        '  "summary": "Contextual overview of why this threat exploits systems",\n'
        '  "suggested_controls": [\n'
        '    {"framework": "NIST SP 800-53", "id": "SI-10", "name": "Information Input Validation", "steps": "Perform strict white-list parameters checks via middleware regex bindings"}\n'
        '  ]\n'
        "}"
    )

    user_input = f"Vulnerability Title: {title}\nDescription: {description}\nProvided Baselines: {severity}"

    try:
        # Mocking connection response processing schema block.
        # Replace this structure block with actual API invocation objects:
        # response = model.generate_content(f"{system_prompt}\n\n{user_input}")
        # parsed_payload = json.loads(response.text)

        # Safe Fallback Structure template to ensure app compiles safely without API credentials active:
        parsed_payload = {
            "risk_score": 8.2 if severity == "Critical" else 5.0,
            "summary": f"Automated structural analysis evaluation for: '{title}'. Possible input execution path breakout risk vector detected.",
            "suggested_controls": [
                {
                    "framework": "NIST SP 800-53",
                    "id": "SI-10",
                    "name": "Information Input Validation",
                    "steps": "Sanitize fields using parameter bindings or server-side structural checking scripts."
                },
                {
                    "framework": "ISO 27001",
                    "id": "A.14.2.1",
                    "name": "Secure Engineering Principles",
                    "steps": "Enforce strict types check arrays inside development architecture components."
                }
            ]
        }
        return parsed_payload

    except Exception as e:
        # Fallback processing if string decoding checks trigger errors
        return {
            "risk_score": 1.0,
            "summary": "AI generation runtime exception encountered.",
            "suggested_controls": []
        }
