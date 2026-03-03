if (!localStorage.getItem("token")) {
    window.location.href = "index.html";
}

function loadAnalytics() {

    fetch("http://127.0.0.1:5000/admin/analytics", {
        headers: {
            "Authorization": "Bearer " +
                localStorage.getItem("token")
        }
    })
    .then(res => {
        if (!res.ok) {
            throw new Error("Failed to load analytics");
        }
        return res.json();
    })
    .then(data => {

        console.log("ANALYTICS:", data);

        const box =
            document.getElementById("analytics");

        box.innerHTML = "";

        // -----------------------------
        // SAFE VALUE HELPER
        // -----------------------------
        const safe = (v) => v ?? 0;

        // -----------------------------
        // SUMMARY CARDS
        // -----------------------------
        box.innerHTML += `
            <div class="analytics-card">
                <h3>Total Quizzes</h3>
                <span>${safe(data.total_quizzes)}</span>
            </div>

            <div class="analytics-card">
                <h3>Total Doubts</h3>
                <span>${safe(data.total_doubts)}</span>
            </div>

            <div class="analytics-card">
                <h3>Study Posts</h3>
                <span>${safe(data.total_posts)}</span>
            </div>

            <div class="analytics-card">
                <h3>Video Lectures</h3>
                <span>${safe(data.total_videos)}</span>
            </div>

            <div class="analytics-card">
                <h3>Assignments Uploaded</h3>
                <span>${safe(data.assignments_uploaded)}</span>
            </div>

            <div class="analytics-card">
                <h3>Assignments Graded</h3>
                <span>${safe(data.assignments_graded)}</span>
            </div>

            <div class="analytics-card">
                <h3>Active Learners</h3>
                <span>${safe(data.active_users)}</span>
            </div>
        `;

        // -----------------------------
        // COURSE ENGAGEMENT
        // -----------------------------
        if (data.course_engagement) {
            data.course_engagement.forEach(item => {

                box.innerHTML += `
                    <div class="analytics-card">
                        <h3>${item.course}</h3>
                        <p>Engaged Learners</p>
                        <span>${item.learners}</span>
                    </div>
                `;
            });
        }

        // -----------------------------
        // RENDER GRAPH SAFELY
        // -----------------------------
        if (data.average_scores) {
            renderAverageScoreChart(
                data.average_scores
            );
        }
    })
    .catch(err => {

        console.error("Analytics Error:", err);

        document.getElementById("analytics")
            .innerText = "Error loading analytics";
    });
}


// ----------------------------------
// GRAPH RENDER
// ----------------------------------
let avgChart = null;

function renderAverageScoreChart(avgScores) {

    const canvas =
        document.getElementById("avgScoreChart");

    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    const labels = Object.keys(avgScores || {});
    const values = Object.values(avgScores || {});

    if (avgChart) {
        avgChart.destroy();
    }

    avgChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Average Score (Privacy-Safe)",
                data: values,
                backgroundColor: [
                    "#5f2eea",
                    "#ff6fd8",
                    "#1d2671",
                    "#c33764"
                ]
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}


// ----------------------------------
// LOGOUT
// ----------------------------------
function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}
