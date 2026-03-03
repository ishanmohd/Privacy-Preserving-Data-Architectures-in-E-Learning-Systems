const token = localStorage.getItem("token");

function createPost() {

    const formData = new FormData();

    formData.append(
        "title",
        document.getElementById("title").value
    );

    formData.append(
        "description",
        document.getElementById("description").value
    );

    formData.append(
        "content",
        document.getElementById("content").value
    );

    formData.append(
        "video_url",
        document.getElementById("video_url").value
    );

    // 📄 PDF file
    const pdf = document.getElementById("pdf").files[0];
    if (pdf) {
        formData.append("pdf", pdf);
    }

    // 🔐 NEW → PDF PASSWORD
    const pdfPassword =
        document.getElementById("pdf_password").value;

    if (pdfPassword) {
        formData.append("pdf_password", pdfPassword);
    }

    fetch(
        "http://127.0.0.1:5000/instructor/create-post",
        {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + token
            },
            body: formData
        }
    )
    .then(res => res.json())
    .then(data => {
        document.getElementById("msg").innerText =
            data.status || data.error;
    })
    .catch(() => {
        document.getElementById("msg").innerText =
            "Failed to create post";
    });
}

function back() {
    window.location.href = "instructor.html";
}
