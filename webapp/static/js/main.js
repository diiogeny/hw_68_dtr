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
            alert("Произошла ошибка. Попробуйте снова.");
        }
    }

    function toggleButtonState(button, data, stateKey, counterKey) {
        const isActive = button.dataset.state === stateKey;
        const newState = isActive ? `not_${stateKey}` : stateKey;
        button.dataset.state = newState;
        button.querySelector(".counter").textContent = data[counterKey];
        button.classList.toggle(stateKey, !isActive);
    }

    document.querySelectorAll(".like-btn").forEach((button) => {
        button.addEventListener("click", async () => {
            const url = button.dataset.url;
            const method = button.dataset.state === "liked" ? "DELETE" : "POST";
            const data = await makeRequest(url, method);
            if (data) {
                toggleButtonState(button, data, "liked", "likes_count");
            }
        });
    });

    document.querySelectorAll(".dislike-btn").forEach((button) => {
        button.addEventListener("click", async () => {
            const url = button.dataset.url;
            const method = button.dataset.state === "disliked" ? "DELETE" : "POST";
            const data = await makeRequest(url, method);
            if (data) {
                toggleButtonState(button, data, "disliked", "dislikes_count");
            }
        });
    });
});
