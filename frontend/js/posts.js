const token = localStorage.getItem("token");

// -----------------------------
// LOAD POSTS
// -----------------------------
function loadPosts() {

    fetch("http://127.0.0.1:5000/student/posts", {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {

        const box = document.getElementById("posts");
        box.innerHTML = "";

        if (!data.length) {
            box.innerHTML = "<p>No study posts available</p>";
            return;
        }

        data.forEach(p => {

            box.innerHTML += `
                <div class="quiz-card">

                    <h3>${p.title}</h3>

                    <p><b>Description:</b> 
                        ${p.description || "—"}
                    </p>

                    <p><b>Content:</b><br>
                        ${p.content || "—"}
                    </p>

                    ${
                        p.video_url
                        ? `
                        <a href="${p.video_url}" 
                           target="_blank"
                           class="video-btn">
                           ▶ Watch Lecture
                        </a>
                        `
                        : ""
                    }

                    ${
                        p.pdf_filename
                        ? `
                        <div class="pdf-box">

                            <span class="pdf-label">
                                🔐 Password Protected PDF
                            </span>

                            <button 
                                onclick="downloadPDF('${p.pdf_filename}')">
                                📄 Download PDF
                            </button>

                        </div>
                        `
                        : ""
                    }

                </div>
            `;
        });

    })
    .catch(() => {
        document.getElementById("posts")
            .innerText = "Error loading posts";
    });
}

// Auto load
document.addEventListener("DOMContentLoaded", loadPosts);

// -----------------------------
// DOWNLOAD PDF
// -----------------------------
function downloadPDF(filename) {

    fetch(
        "http://127.0.0.1:5000/student/download-post-pdf/" + filename,
        {
            headers: {
                "Authorization":
                    "Bearer " + localStorage.getItem("token")
            }
        }
    )
    .then(res => res.blob())
    .then(blob => {

        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;

        // Remove encryption extension
        a.download = filename.replace(".enc", "");

        a.click();
    })
    .catch(() => {
        alert("Unable to download PDF");
    });
}

// -----------------------------
// BACK
// -----------------------------
function back() {
    window.location.href = "student.html";
}
