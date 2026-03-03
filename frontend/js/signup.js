function signup() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const role = document.getElementById("role").value;

    document.getElementById("msg").innerText = "Signing up...";

    fetch("http://127.0.0.1:5000/auth/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password,
            role: role
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("SIGNUP RESPONSE:", data);

        // ✅ CORRECT CONDITION
        if (data.user_id) {
            document.getElementById("msg").innerText =
                "Signup successful! Your User ID is " + data.user_id +
                ". Please check your email for MFA key.";
        } else {
            document.getElementById("msg").innerText =
                data.error || "Signup failed";
        }
    })
    .catch(err => {
        console.error(err);
        document.getElementById("msg").innerText = "Server error";
    });
}
