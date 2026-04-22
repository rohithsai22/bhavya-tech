document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    if (form) {
        form.addEventListener("submit", function (e) {

            e.preventDefault(); // ⛔ stop instant reload

            // Create toast
            const toast = document.createElement("div");
            toast.innerText = "✅ Request submitted successfully!";
            toast.classList.add("toast");

            document.body.appendChild(toast);

            // Show animation
            setTimeout(() => {
                toast.classList.add("show");
            }, 100);

            // Submit form after delay
            setTimeout(() => {
                form.submit();
            }, 1500); // 1.5 seconds delay

        });
    }

});