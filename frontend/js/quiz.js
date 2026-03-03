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
// SUBMIT QUIZ (REAL BACKEND CALL)
// ------------------------------------
function submitQuiz() {
    const quizName = document.getElementById("quiz_name").value;
    const instructorId = document.getElementById("instructor_id").value;
    const msg = document.getElementById("msg");

    if (!quizName || !instructorId) {
        msg.innerText = "Quiz name and instructor ID are required";
        return;
    }

    // Collect answers (example – adapt to your quiz UI)
    const answers = {
        q1: document.querySelector('input[name="q1"]:checked')?.value || "",
        q2: document.querySelector('input[name="q2"]:checked')?.value || "",
        q3: document.querySelector('input[name="q3"]:checked')?.value || ""
    };

    fetch("http://127.0.0.1:5000/student/submit-quiz", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            quiz_name: quizName,
            answers: answers,
            instructor_id: instructorId
        })
    })
    .then(res => res.json())
    .then(data => {
        msg.innerText = data.status || data.error;
    })
    .catch(() => {
        msg.innerText = "Quiz submission failed";
    });
}

// ------------------------------------
// NAVIGATION
// ------------------------------------
function back() {
    window.location.href = "student.html";
}
