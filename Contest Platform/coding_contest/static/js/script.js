document.addEventListener("DOMContentLoaded", function () {
    const submitBtn = document.getElementById("submit-code");
    const languageSelect = document.getElementById("language");
    const codeEditor = document.getElementById("code-editor");
    const outputBox = document.getElementById("output-box");

    if (submitBtn) {
        submitBtn.addEventListener("click", function () {
            submitCode();
        });
    }

    function submitCode() {
        const code = codeEditor.value.trim();
        const language = languageSelect.value;

        if (!code) {
            alert("Please write some code before submitting!");
            return;
        }

        fetch("/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code: code, language: language })
        })
        .then(response => response.json())
        .then(data => {
            outputBox.innerHTML = `<strong>${data.message}</strong>`;
            if (data.score !== undefined) {
                outputBox.innerHTML += `<br>Score: ${data.score}/${data.total_tests}`;
            }
            updateLeaderboard();
        })
        .catch(error => {
            console.error("Error:", error);
            outputBox.innerHTML = "<strong>Submission failed. Try again.</strong>";
        });
    }

    function updateLeaderboard() {
        fetch("/update_leaderboard", {
            method: "POST"
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
        })
        .catch(error => console.error("Error updating leaderboard:", error));
    }
});
