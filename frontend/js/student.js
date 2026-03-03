// ------------------------------------
// AUTH CHECK
// ------------------------------------
if (!localStorage.getItem("token")) {
    window.location.href = "index.html";
}

if (localStorage.getItem("role") !== "student") {
    window.location.href = "login.html";
}

// ------------------------------------
// NAVIGATION
// ------------------------------------
function go(page) {
    window.location.href = page;
}

function upload() {
    window.location.href = "student_upload.html";
}

// ------------------------------------
// LOGOUT
// ------------------------------------
function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    window.location.href = "index.html";
}

// ------------------------------------
// UPLOAD ASSIGNMENT (FIXED)
// ------------------------------------
function uploadAssignment() {
    const token = localStorage.getItem("token");
    const fileInput = document.getElementById("file");
    const msg = document.getElementById("msg");

    if (!fileInput.files.length) {
        msg.innerText = "Please select a file";
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("http://127.0.0.1:5000/student/upload", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token
        },
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        msg.innerText = data.status || data.error;
    })
    .catch(() => {
        msg.innerText = "Upload failed";
    });
}

// ------------------------------------
// SUBMIT QUIZ (CRITICAL)
// ------------------------------------
function submitQuiz() {
    const token = localStorage.getItem("token");

    const quizName = document.getElementById("quiz_name").value;
    const instructorId = document.getElementById("instructor_id").value;

    if (!quizName || !instructorId) {
        alert("Quiz name and instructor ID required");
        return;
    }

    // Example answers object (customize as needed)
    const answers = {
        q1: document.getElementById("q1")?.value || "",
        q2: document.getElementById("q2")?.value || ""
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
        alert(data.status || data.error);
    })
    .catch(() => {
        alert("Quiz submission failed");
    });
}

// ------------------------------------
// SUBMIT DOUBT (FIXED)
// ------------------------------------
function submitDoubt() {
    const token = localStorage.getItem("token");

    const question = document.getElementById("question").value;
    const quizId = document.getElementById("quiz_id").value;

    if (!question || !quizId) {
        alert("Question and Quiz ID required");
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
        alert(data.status || data.error);
    })
    .catch(() => {
        alert("Doubt submission failed");
    });
}
