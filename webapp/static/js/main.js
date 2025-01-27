document.addEventListener("DOMContentLoaded", function () {
    async function makeRequest(url, method = "POST") {
        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    "Content-Type": "application/json",
                },
            });
            if (response.ok) {
                return await response.json();
            } else {
                throw new Error(`HTTP Error: ${response.status}`);
            }
        } catch (error) {
            console.error("Request failed:", error);
        }
    }

    function handleButton(button, stateKey, counterKey) {
        button.addEventListener("click", async (event) => {
            event.preventDefault();
            const url = button.dataset.url;
            const isActive = button.classList.contains(stateKey);
            const method = isActive ? "DELETE" : "POST";

            const data = await makeRequest(url, method);
            if (data) {
                button.querySelector(".counter").textContent = data[counterKey];
                button.classList.toggle(stateKey, !isActive);
            }
        });
    }

    document.querySelectorAll(".like-btn").forEach((button) => {
        handleButton(button, "liked", "likes_count");
    });

    document.querySelectorAll(".dislike-btn").forEach((button) => {
        handleButton(button, "disliked", "dislikes_count");
    });
});
