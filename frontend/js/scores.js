// ------------------------------------
// AUTH CHECK
// ------------------------------------
const token = localStorage.getItem("token");
const role = localStorage.getItem("role");

if (!token) {
    window.location.href = "index.html";
}

if (role !== "student") {
    window.location.href = "login.html";
}

// ------------------------------------
// LOAD SCORES (STUDENT ONLY)
// ------------------------------------
function loadScores() {
    fetch("http://127.0.0.1:5000/student/scores", {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => {
        if (!res.ok) {
            throw new Error("Failed to load scores");
        }
        return res.json();
    })
    .then(data => {
        const scoreDiv = document.getElementById("scores");

        if (!data.length) {
            scoreDiv.innerText = "No scores available yet";
            return;
        }

        scoreDiv.innerText = JSON.stringify(data, null, 2);
    })
    .catch(err => {
        console.error(err);
        document.getElementById("scores").innerText =
            "Error loading scores";
    });
}

// ------------------------------------
// AUTO LOAD ON PAGE OPEN
// ------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    loadScores();
});

// ------------------------------------
// NAVIGATION
// ------------------------------------
function back() {
    window.location.href = "student.html";
}
