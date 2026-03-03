const token = localStorage.getItem("token");

// 🔐 Auth protection
if (!token) {
    window.location.href = "index.html";
}


// =====================================================
// 📄 QUIZZES PAGE
// (instructor_quizzes.html)
// =====================================================
function loadQuizzes() {

    fetch("http://127.0.0.1:5000/instructor/quizzes", {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {

        const box = document.getElementById("quizList"); // ⚠️ FIXED ID
        box.innerHTML = "";

        if (!data.length) {
            box.innerHTML = "No quiz submissions";
            return;
        }

        data.forEach(q => {

            let answersObj = q.answers || {};
            let answersHTML = "";

            if (Object.keys(answersObj).length) {

                for (let key in answersObj) {
                    answersHTML += `
                        <b>${key}:</b> ${answersObj[key]}<br>
                    `;
                }

            } else {
                answersHTML = "No answers";
            }

            box.innerHTML += `
                <div class="quiz-card">
                    <b>ID:</b> ${q.id}<br>
                    <b>Quiz:</b> ${q.quiz_name}<br><br>

                    <b>Answers:</b><br>
                    ${answersHTML}<br>

                    <b>Evaluated:</b> ${q.evaluated}
                </div>
            `;
        });
    });
}



// =====================================================
// 📝 EVALUATE QUIZ
// =====================================================
function evaluateQuiz() {

    const quizId =
        document.getElementById("quiz_id").value;

    const score =
        document.getElementById("score").value;

    if (!quizId || !score) {
        alert("Enter quiz ID & score");
        return;
    }

    fetch("http://127.0.0.1:5000/instructor/evaluate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            quiz_id: quizId,
            score: score
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.status || data.error);
        loadQuizzes();
    });
}


// =====================================================
// 💬 DOUBTS PAGE
// (instructor_doubts.html)
// =====================================================
function loadDoubts() {

    fetch("http://127.0.0.1:5000/instructor/doubts", {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {

        const box =
            document.getElementById("doubtList");

        box.innerHTML = "";

        if (!data.length) {
            box.innerHTML = "No doubts submitted";
            return;
        }

        data.forEach(d => {

            box.innerHTML += `
                <div class="quiz-card">

                    <b>ID:</b> ${d.id}<br>

                    <b>Question:</b><br>
                    ${d.question}<br><br>

                    <b>Reply:</b><br>
                    ${d.reply || "<i>No reply yet</i>"}<br><br>

                    <!-- ✏️ Reply Input -->
                    <textarea
                        id="reply_${d.id}"
                        placeholder="Type reply..."
                        style="width:100%;height:70px;">
                    </textarea>

                    <button
                        onclick="sendReply(${d.id})">
                        Send Reply
                    </button>

                </div>
            `;
        });
    });
}

function sendReply(doubtId) {

    const replyText =
        document.getElementById(
            "reply_" + doubtId
        ).value;

    if (!replyText) {
        alert("Reply cannot be empty");
        return;
    }

    fetch("http://127.0.0.1:5000/instructor/reply", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            doubt_id: doubtId,
            reply: replyText
        })
    })
    .then(res => res.json())
    .then(data => {

        alert(data.status || data.error);

        // Reload doubts
        loadDoubts();
    });
}





// =====================================================
// 📂 ASSIGNMENTS PAGE
// (instructor_assignments.html)
// =====================================================
function viewAssignments() {

    fetch("http://127.0.0.1:5000/instructor/assignments", {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {

        const box =
            document.getElementById("assignments");

        if (!box) return;

        box.innerHTML = "";

        if (!data.length) {
            box.innerHTML = "No assignments uploaded";
            return;
        }

        data.forEach(a => {

            box.innerHTML += `
                <div class="quiz-card">

                    <b>ID:</b> ${a.id}<br>
                    <b>File:</b> ${a.filename}<br>

                    <button onclick="
                        downloadAssignment('${a.filename}'
                    )">
                        📥 Download
                    </button>

                </div>
            `;
        });
    });
}


// =====================================================
// 📥 DOWNLOAD ASSIGNMENT
// =====================================================
function downloadAssignment(filename) {

    fetch(
        "http://127.0.0.1:5000/instructor/download-assignment/" + filename,
        {
            headers: {
                "Authorization": "Bearer " + token
            }
        }
    )
    .then(res => res.blob())
    .then(blob => {

        const url =
            window.URL.createObjectURL(blob);

        const a =
            document.createElement("a");

        a.href = url;
        a.download =
            filename.replace(".enc", "");

        a.click();
    })
    .catch(() => {
        alert("Unable to download assignment");
    });
}


// =====================================================
// 📝 GRADE ASSIGNMENT
// =====================================================
function gradeAssignment() {

    const id =
        document.getElementById("assignment_id").value;

    const marks =
        document.getElementById("marks").value;

    const feedback =
        document.getElementById("feedback").value;

    if (!id || !marks) {
        alert("Assignment ID & marks required");
        return;
    }

    fetch(
        "http://127.0.0.1:5000/instructor/grade-assignment",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({
                assignment_id: id,
                marks: marks,
                feedback: feedback
            })
        }
    )
    .then(res => res.json())
    .then(data => alert(data.status));
}


// =====================================================
// 🚀 NAVIGATION (Dashboard → Pages)
// =====================================================
function goToQuizzes() {
    window.location.href =
        "instructor_quizzes.html";
}

function goToDoubts() {
    window.location.href =
        "instructor_doubts.html";
}

function goToAssignments() {
    window.location.href =
        "instructor_assignments.html";
}

function goToPosts() {
    window.location.href =
        "create_post.html";
}


// =====================================================
// 🔓 LOGOUT
// =====================================================
function logout() {
    localStorage.clear();
    window.location.href = "index.html";
}


// =====================================================
// 📌 AUTO LOAD (PAGE BASED)
// =====================================================
document.addEventListener("DOMContentLoaded", () => {

    // Quizzes page
    if (document.getElementById("quizList")) {
        loadQuizzes();
    }

    // Doubts page
    if (document.getElementById("doubtList")) {
        loadDoubts();
    }

    // Assignments page
    if (document.getElementById("assignments")) {
        viewAssignments();
    }
});


// 🔙 BACK TO DASHBOARD
function goBack() {
    window.location.href = "instructor.html";
}

