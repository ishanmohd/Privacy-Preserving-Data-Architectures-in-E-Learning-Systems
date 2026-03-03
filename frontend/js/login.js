function login() {
    const userId = document.getElementById("user_id").value;
    const password = document.getElementById("password").value;
    const otp = document.getElementById("otp").value;

    document.getElementById("msg").innerText = "Logging in...";

    fetch("http://127.0.0.1:5000/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: userId,
            password: password,
            otp: otp
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("LOGIN RESPONSE:", data);

        if (data.access_token && data.role) {
            localStorage.setItem("token", data.access_token);
            localStorage.setItem("role", data.role);

            if (data.role === "student") {
                window.location.href = "student.html";
            } 
            else if (data.role === "instructor") {
                window.location.href = "instructor.html";
            } 
            else if (data.role === "admin") {
                window.location.href = "admin.html";
            }
        } else {
            document.getElementById("msg").innerText =
                data.error || "Login failed";
        }
    })
    .catch(err => {
        console.error(err);
        document.getElementById("msg").innerText = "Server error";
    });
}
