document.getElementById("signupForm").onsubmit = async function(e) {
    e.preventDefault();
    const data = {
        first_name: document.getElementById("first_name").value,
        last_name: document.getElementById("last_name").value,
        username: document.getElementById("username").value,
        phone: document.getElementById("phone").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
        role: document.getElementById("role").value
    };

    const response = await fetch("http://localhost:8080/api/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        alert("Signup successful. Please log in.");
        console.log("Data sent to server:", data); // Debugging line to verify data
        window.location.href = "/frontend/login_page/login.html";
    } else {
        alert("Signup failed.");
        const error = await response.text();
        console.log("Error response from server:", error); // Debugging error from server
    }
}

document.getElementById("loginButton").onclick = function() {
    window.location.href = "/frontend/login_page/login.html";
};