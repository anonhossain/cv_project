async function submitForm() {
  const jobDesc = document.querySelector('textarea[name="job_desc"]').value;
  const resumeFile = document.querySelector('input[name="resume"]').files[0];

  // Create a FormData object and append data
  const formData = new FormData();
  formData.append("job_desc", jobDesc);
  formData.append("resume", resumeFile);
  formData.append("action", "submit");

  // Send the request with fetch
  try {
    const response = await fetch("http://localhost:8080/api/upload_files/", {
      method: "POST",
      body: formData,
    });

    // Check if the request was successful
    if (response.ok) {
      document.getElementById("analyzeButton").disabled = false;
      document.getElementById("generateButton").disabled = false;
      alert(
        "Files uploaded successfully. You can now analyze the resume or generate questions."
      );
    } else {
      alert("File upload failed. " + response.statusText);
    }
  } catch (error) {
    loadingIndicator.style.display = "none"; // Hide loading indicator
    console.error("Error uploading files:", error);
    alert("An error occurred during file upload.");
  }
}
async function analyzeResume() {
  const loading = document.getElementById("loading");
  const container = document.getElementById("container");

  loading.style.display = "block";
  container.style.display = "none";
  try {
    const response = await fetch("http://localhost:8080/api/analyze_resume/", {
      method: "GET", 
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();

    if (response.ok) {
      // Show a success alert
      // alert("Resume analysis successful");
      var text = JSON.stringify(data.response);
      text = text.replace(/\\n/g, "<br>");
      text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
      text = text.replace(/\*(.*?)\*/g, "<em>$1</em>");
      text = text.replace(/__(.*?)__/g, "<u>$1</u>");
      text = text.replace('"', " ");
      text = text.replace(/\\"/g, ' " ');

      // Dynamically display the result on the frontend
      const resultContainer = document.getElementById("resultContent");
      resultContainer.innerHTML = `
        <h3>Resume Analysis Result:</h3>
        <p>${text}</p>
      `;
      loading.style.display = "none";
      document.getElementById("resultPanel").style.display = "block";
    } else {
      // Handle API errors
      alert(`Resume analysis failed: ${data.detail}`);
    }
  } catch (error) {
    // Handle network or other unexpected errors
    alert("An error occurred while analyzing the resume");
    console.error(error);
  }
}

function generateQuestions() {
  // Displaying simulated questions for testing
  const resultPanel = document.getElementById("resultPanel");
  const resultContent = document.getElementById("resultContent");

  resultPanel.style.display = "block";
  resultContent.textContent =
    "Generated Questions:\n1. What are your strengths?\n2. Describe your experience with similar roles.\n3. How would you contribute to our team?";
}

function loginPage() {
  window.location.href = "/frontend/login_page/login.html";
}

// document.addEventListener("DOMContentLoaded", function () {
//   document.getElementById("loginButton").onclick = function () {
//     window.location.href = "/frontend/login_page/login.html";
//   };
// });
