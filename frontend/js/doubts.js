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
// SUBMIT DOUBT (REAL BACKEND CALL)
// ------------------------------------
function submitDoubt() {
    const question = document.getElementById("question").value;
    const quizId = document.getElementById("quiz_id").value;
    const msg = document.getElementById("msg");

    if (!question || !quizId) {
        msg.innerText = "Question and Quiz ID are required";
        return;
    }

    fetch("http://127.0.0.1:5000/student/submit-doubt", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            question: question,
            quiz_id: quizId
        })
    })
    .then(res => res.json())
    .then(data => {
        msg.innerText = data.status || data.error;
    })
    .catch(() => {
        msg.innerText = "Doubt submission failed";
    });
}

function loadMyDoubts() {
    fetch("http://127.0.0.1:5000/student/my-doubts", {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {
        const box = document.getElementById("my_doubts");
        if (!data.length) {
            box.innerText = "No doubts yet";
            return;
        }
        box.innerText = JSON.stringify(data, null, 2);
    });
}

document.addEventListener("DOMContentLoaded", loadMyDoubts);


// ------------------------------------
// NAVIGATION
// ------------------------------------
function back() {
    window.location.href = "student.html";
}
