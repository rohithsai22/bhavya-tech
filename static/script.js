document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    if (form) {
        form.addEventListener("submit", function () {
            alert("Thank you! Bhavya Tech will contact you soon.");
        });
    }

});