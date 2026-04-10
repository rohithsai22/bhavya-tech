document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    if (form) {
        form.addEventListener("submit", function () {

            // Create toast
            const toast = document.createElement("div");
            toast.innerText = "✅ Request submitted successfully!";
            toast.classList.add("toast");

            document.body.appendChild(toast);

            // Show animation
            setTimeout(() => {
                toast.classList.add("show");
            }, 100);

            // Remove after 3 seconds
            setTimeout(() => {
                toast.remove();
            }, 3000);
        });
    }

});