const faqItems = document.querySelectorAll(".faq-question");

    faqItems.forEach(item => {
        item.addEventListener("click", () => {
            const parent = item.parentElement;
            parent.classList.toggle("active");

            const icon = item.querySelector(".icon");
            icon.textContent = parent.classList.contains("active") ? "-" : "+";
        });
    });