window.addEventListener("load", () => {
document.querySelectorAll(".input-group input").forEach(input => {
    if (input.value) {
    input.classList.add("has-value");
    }

    input.addEventListener("input", () => {
    if (input.value) {
        input.classList.add("has-value");
    } else {
        input.classList.remove("has-value");
    }
    });
});
});
