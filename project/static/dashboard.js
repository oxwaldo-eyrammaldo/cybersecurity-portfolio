document.addEventListener("DOMContentLoaded", function() {
    // Select all interactive framework compliance control checkboxes
    const checkboxes = document.querySelectorAll(".control-toggle-checkbox");

    checkboxes.forEach(function(box) {
        box.addEventListener("change", function() {
            const controlId = this.getAttribute("data-control-id");
            const isChecked = this.checked ? 1 : 0;

            // Visually fade the checklist row container style layout to show an update is processing
            const rowContainer = this.closest("tr");
            if (rowContainer) {
                rowContainer.style.opacity = "0.5";
            }

            // Asynchronous FETCH submission back to the Flask API
            fetch("/control/toggle", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    id: parseInt(controlId),
                    state: isChecked
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network transaction security verification failed.");
                }
                return response.json();
            })
            .then(data => {
                // Restore transparency and adjust color status context depending on result states
                if (rowContainer) {
                    rowContainer.style.opacity = "1";
                    if (isChecked === 1) {
                        rowContainer.classList.add("table-success");
                    } else {
                        rowContainer.classList.remove("table-success");
                    }
                }
            })
            .catch(error => {
                console.error("Error managing backend state synchronizations:", error);
                // Revert interface view to state consistency if server error triggers
                this.checked = !this.checked;
                if (rowContainer) {
                    rowContainer.style.opacity = "1";
                }
                alert("Failed to modify compliance control status. Ensure session authentication state remains active.");
            });
        });
    });
});
