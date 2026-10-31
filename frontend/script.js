"use strict";

// ========================================
// LEON'S AI RESUME ANALYZER
// ========================================

console.log("Resume Analyzer JavaScript loaded!");

const resumeForm = document.getElementById("resumeForm");
const resumeInput = document.getElementById("resume");
const jobDescriptionInput = document.getElementById("jobDescription");

const analyzeButton = document.getElementById("analyzeButton");
const statusMessage = document.getElementById("statusMessage");
const resultsSection = document.getElementById("results");

const matchScore = document.getElementById("matchScore");
const matchedSkills = document.getElementById("matchedSkills");
const missingSkills = document.getElementById("missingSkills");


// Check that all required elements exist

if (
    !resumeForm ||
    !resumeInput ||
    !jobDescriptionInput ||
    !analyzeButton ||
    !statusMessage ||
    !resultsSection ||
    !matchScore ||
    !matchedSkills ||
    !missingSkills
) {
    console.error("HTML elements are missing. Check index.html IDs.");

} else {

    // Handle the form submission

    resumeForm.addEventListener("submit", async function (event) {

        event.preventDefault();
        event.stopPropagation();

        console.log("Analyze button clicked!");

        const resumeFile = resumeInput.files[0];
        const jobDescription = jobDescriptionInput.value.trim();

        // Validate the PDF

        if (!resumeFile) {
            showError("Please upload your resume PDF.");
            return;
        }

        if (!resumeFile.name.toLowerCase().endsWith(".pdf")) {
            showError("Please upload a PDF file.");
            return;
        }

        if (resumeFile.size > 5 * 1024 * 1024) {
            showError("The PDF must be smaller than 5 MB.");
            return;
        }

        // Validate the job description

        if (!jobDescription) {
            showError("Please enter a job description.");
            return;
        }

        // Prepare form data

        const formData = new FormData();

        formData.append("resume", resumeFile);
        formData.append("job_description", jobDescription);

        // Show loading state

        analyzeButton.disabled = true;
        analyzeButton.textContent = "Analyzing...";

        statusMessage.style.color = "#333";
        statusMessage.textContent = "Analyzing your resume...";

        resultsSection.hidden = true;

        try {

            // Send the request to Flask

            console.log("Sending request to Flask...");

            const response = await fetch(
                "http://127.0.0.1:5000/analyze-pdf",
                {
                    method: "POST",
                    body: formData
                }
            );

            console.log("HTTP status:", response.status);

            const result = await response.json();

            console.log("Server response:", result);

            // Handle errors

            if (!response.ok) {
                throw new Error(
                    result.error || "Resume analysis failed."
                );
            }

            // Validate the response

            if (
                typeof result.match_score !== "number" ||
                !Array.isArray(result.matched_skills) ||
                !Array.isArray(result.missing_skills)
            ) {
                throw new Error("The server returned invalid analysis data.");
            }

            // Display the score

            matchScore.textContent = result.match_score + "%";

            // Display skills

            displaySkills(matchedSkills, result.matched_skills);
            displaySkills(missingSkills, result.missing_skills);

            // Show results

            resultsSection.hidden = false;

            statusMessage.style.color = "green";
            statusMessage.textContent =
                "Resume analysis completed successfully!";

            console.log("Analysis completed successfully!");
            console.log("Results section visible:", !resultsSection.hidden);

            // Scroll to the results

            resultsSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        } catch (error) {

            console.error("Analysis error:", error);
            showError(error.message);

        } finally {

            analyzeButton.disabled = false;
            analyzeButton.textContent = "Analyze Resume";

        }

    });

}


// Display error messages

function showError(message) {

    statusMessage.textContent = "Error: " + message;
    statusMessage.style.color = "red";
    statusMessage.style.fontWeight = "bold";

    resultsSection.hidden = true;

}


// Display skills

function displaySkills(listElement, skills) {

    listElement.replaceChildren();

    if (skills.length === 0) {

        const li = document.createElement("li");
        li.textContent = "No skills found.";

        listElement.appendChild(li);

        return;
    }

    skills.forEach(function (skill) {

        const li = document.createElement("li");
        li.textContent = skill;

        listElement.appendChild(li);

    });

}