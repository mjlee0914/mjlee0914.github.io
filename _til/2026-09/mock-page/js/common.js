window.addEventListener("DOMContentLoaded", function() {
    window.addEventListener("scroll", function() {
        const header = document.querySelector("header")
        const classList = header.classList;
        if (pageYOffset >= 40) {
            classList.add("fixed");
        } else {
            classList.remove("fixed");
        }
    });
});