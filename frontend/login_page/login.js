document.getElementById("loginForm").onsubmit = async function(e) {
    e.preventDefault();
    
    const data = {
        username: document.getElementById("username").value,
        password: document.getElementById("password").value
    };

    try {
        const response = await fetch("http://localhost:8080/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            // console.log("Full response:", result); // Log the entire response to confirm structure

            // Exact match on role
            if (result["user"]["role"] === "Admin") {
                // alert("Admin login successful!");
                window.location.href = "/frontend/admin_panel/admin.html"; // Redirect to admin page
            } else if (result["user"]["role"] === "HR") {
                // alert("HR login successful!");
                window.location.href = "/frontend/body/hr_body.html"; // Redirect to HR page
            } else {
                // alert("Login successful!");
                window.location.href = "/frontend/welcome_page/welcomeCan.html"; // Redirect to general welcome page
            }
        } else {
            alert("Login failed. Please check your credentials.");
        }
    } catch (error) {
        console.error("Error during login:", error);
        alert("An error occurred. Please try again.");
    }
};

document.getElementById("signupButton").onclick = function() {
    window.location.href = "/frontend/signup_page/index.html";
};

document.getElementById("test_resume").onclick = function() {
    window.location.href = "/frontend/test_resume/test_resume.html";
};
