let selectedCV = [];
document.getElementById("upload-form").addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent the default form submission behavior

    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch("http://localhost:8080/api/hr-submit-resume", {
            method: "POST",
            body: formData,
        });
        console.log(formData);
        

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail}`);
            return;
        }

        const result = await response.json();
        alert("File uploaded successfully");
        
        
    } catch (error) {
        console.error("Error submitting form:", error);
        alert("Filed saved successfully");
    }
});
document.getElementById("analyze_existing").addEventListener("click", async function(){
    const matching_table = document.getElementById("cv-matching-table-body");
    matching_table.innerHTML = "";
    document.getElementById("loading11").style.display="block";
    try {
        const response = await fetch("http://localhost:8080/api/analyze_resume_hr/");
        

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail}`);
            return;
        }

        const result = await response.json();

        document.getElementById("table12").style.display = "block";
        document.getElementById("loading11").style.display="none";
        
        var rowID = 0;
        for (var [key, value] of Object.entries(result.response)) {
            var newRow = document.createElement("tr");
            id = "row"+rowID;
            newRow.setAttribute("id", id);

            var td1 = document.createElement("td");
            td1.textContent = key;
            selectedCV.push(key);

            var td2 = document.createElement("td");
            td2.textContent = value+'%';

            var td3 = document.createElement("td");
            td3.innerHTML = `<button style="padding: 8px 16px; font-size: 14px; cursor: pointer; border: none; border-radius: 4px; background-color: #f44336; color: white; transition: background-color 0.3s ease;" 
                            onmouseover="this.style.backgroundColor='#d32f2f'" onmouseout="this.style.backgroundColor='#f44336' " onclick= "rowDelete(${id})">Delete</button>`; 

            newRow.appendChild(td1);
            newRow.appendChild(td2);
            newRow.appendChild(td3);

            matching_table.appendChild(newRow);
            rowID++;
        }
        

    } catch (error) {
        console.error("Error submitting form:", error);
        alert("Failed to submit form. Please try again.");
    }
})

function rowDelete(rowID){
    
    rowID.remove();
    
    selectedCV.pop(rowID.firstChild.innerHTML);
}   

document.getElementById("extract_trig").addEventListener("click", async function(){
    console.log(JSON.stringify(selectedCV));
    
    try {
        const response = await fetch("http://localhost:8080/api/extract_resume_info", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
              },
            body: JSON.stringify( selectedCV ),
        });
        

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData}`);
            return;
        }

        const result = await response.json();
        console.log(JSON.stringify(result));

        
        sessionStorage.setItem('resultData', JSON.stringify(result));
        console.log(sessionStorage.getItem('resultData'));
        
        alert("Information extracted successfully!");

        
    } catch (error) {
        console.error("Error submitting form:", error);
        alert("Failed to submit form. Please try again.");
    }
})


document.querySelector('button[name="action"][value="extract_info"]').addEventListener('click', async () => {
    try {
        // Fetch filenames from the server
        const filenamesResponse = await fetch('http://localhost:8080/api/get_resume_filenames/');
        
        if (!filenamesResponse.ok) throw new Error(`Failed to fetch filenames: ${filenamesResponse.status}`);
        
        const filenamesData = await filenamesResponse.json();
        
        if (filenamesData.error) {
            console.error("Error fetching filenames:", filenamesData.error);
            alert("Failed to retrieve resume filenames.");
            return;
        }

        const fileNames = filenamesData.filenames;
        
        // Now send the filenames to the extract_resume_info API
        const response = await fetch('http://localhost:8080/api/extract_resume_info/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(fileNames)
        });

        if (!response.ok) throw new Error(`Failed to extract resume info: ${response.status}`);

        const data = await response.json();

        console.log("Extracted Resume Info:", data);

        // Optional: Display the result in the browser
        let resultDiv = document.getElementById("resumeResult");
        resultDiv.innerHTML = "<pre>" + JSON.stringify(data, null, 2) + "</pre>";

        alert("All information extracted and saved.");

    } catch (error) {
        console.error("Error:", error);
        alert("All information extracted and saved.");
    }
});


document.getElementById("generateQuestion").addEventListener("click", async function () {
    const loading = document.getElementById("loading11");

    // Show loading and update message
    loading.style.display = "block";
    loading.children[1].innerHTML = "Generating Questions...";
    loading.children[1].style.fontSize = "20px";
    loading.children[1].style.fontWeight = "bold";

    try {
        const response = await fetch("http://localhost:8080/api/generate_hr_questions", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.message || "Unknown error occurred."}`);
        } else {
            const result = await response.json();
            console.log("Questions generated:", result);
            alert("Questions generated successfully!");
        }
    } catch (error) {
        console.error("Error generating questions:", error);
        alert("Failed to generate questions. Please make sure the server is running.");
    } finally {
        loading.style.display = "none";
        loading.children[1].innerHTML = "Analysing All CVs...";
    }
});


document.getElementById("generateQuestion").addEventListener("click", async function () {
    const loading = document.getElementById("loading11");
    const loadingMessage = document.getElementById("loadingMessage");
    const progressBar = document.getElementById("progressBar");
    const progressFill = document.getElementById("progressFill");

    // Show loading and update message
    loading.style.display = "block";
    loadingMessage.innerHTML = "Generating Questions...";
    loadingMessage.style.fontSize = "20px";
    loadingMessage.style.fontWeight = "bold";

    try {
        const response = await fetch("http://localhost:8080/api/generate_hr_questions", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.message || "Unknown error occurred."}`);
        } else {
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let progress = 0;
            const chunkSize = 1024;
            let result = "";
            let done = false;
            
            while (!done) {
                const { value, done: readerDone } = await reader.read();
                done = readerDone;
                result += decoder.decode(value, { stream: true });

                // Update progress bar
                // Assuming the backend is sending a percentage value in the response body
                if (result.includes("data:")) {
                    const progressMatch = result.match(/data: (\d+)/);
                    if (progressMatch) {
                        progress = parseInt(progressMatch[1], 10);
                        progressFill.style.width = progress + "%";  // Update progress bar
                        loadingMessage.innerHTML = `Generated: ${progress}%`;  // Update message
                    }
                }
            }

            console.log("Questions generated:", result);
            alert("Questions generated successfully!");
        }
    } catch (error) {
        console.error("Error generating questions:", error);
        alert("Failed to generate questions. Please make sure the server is running.");
    } finally {
        loading.style.display = "none";
    }
});
