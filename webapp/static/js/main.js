document.addEventListener("DOMContentLoaded", function () {
    async function makeRequest(url, method = "POST") {
        try {
            const response = await fetch(url, {
                method: method,
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({}), // Коррекция: API требует тело запроса
            });

            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("Request failed:", error);
            return null;
        }
    }

    function handleButton(button, stateKey, counterKey) {
        button.addEventListener("click", async (event) => {
            event.preventDefault();
            const url = button.dataset.url;

            const data = await makeRequest(url);
            if (data) {
                button.querySelector(".counter").textContent = data[counterKey];
                button.classList.toggle(stateKey, data[stateKey]); // Коррекция: теперь корректно обновляет UI
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
