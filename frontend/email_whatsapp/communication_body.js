document.getElementById("excel-upload").addEventListener("change", async function () {
    const file = this.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://127.0.0.1:8080/api/get_excel_columns/", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Failed to fetch column headers.");
        }

        const result = await response.json();
        const columnSelect = document.getElementById("email-column-select");
        columnSelect.innerHTML = '<option value="">-- Choose Column --</option>';

        result.columns.forEach(column => {
            const option = document.createElement("option");
            option.value = column;
            option.textContent = column;  // This should be "column" and not "columns"
            columnSelect.appendChild(option);
        });

        document.getElementById("email-column-section").style.display = "block";
    } catch (error) {
        console.error("Error fetching columns:", error);
        alert("Received the File");
    }
});

document.getElementById("mail-sms-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const form = e.target;
    const fileInput = document.getElementById("excel-upload");
    const subjectInput = document.getElementById("email-subject");
    const messageInput = document.getElementById("message-content");
    const columnSelect = document.getElementById("email-column-select");

    if (!fileInput.files.length || !subjectInput.value || !messageInput.value || !columnSelect.value) {
        alert("Please fill in all fields and upload a file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("subject", subjectInput.value);
    formData.append("email_col", columnSelect.value);  // Ensure email column is sent
    formData.append("email_message", messageInput.value);

    try {
        const response = await fetch("http://127.0.0.1:8080/api/send_emails/", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();

        if (!response.ok) {
            alert(`Error: ${result.error}`);
            return;
        }

        alert("Emails sent successfully!");
    } catch (error) {
        console.error("Error submitting form:", error);
        alert("Failed to submit form. Please try again.");
    }
});
