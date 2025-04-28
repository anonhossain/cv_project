document.getElementById("signupForm").onsubmit = async function(e) {
    e.preventDefault();
    const data = {
        first_name: document.getElementById("first_name").value,
        last_name: document.getElementById("last_name").value,
        username: document.getElementById("username").value,
        phone: document.getElementById("phone").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
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
        window.location.href = "login.html";
    } else {
        const errorData = await response.json();
        alert(`Signup failed: ${errorData.detail}`);
    }
};
