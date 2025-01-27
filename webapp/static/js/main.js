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

    document.querySelectorAll(".like-btn").forEach((button) => {
        button.addEventListener("click", async (event) => {
            event.preventDefault();
            const url = button.dataset.url;
            const isLiked = button.classList.contains("liked");
            const method = isLiked ? "DELETE" : "POST";

            const data = await makeRequest(url, method);
            if (data) {
                button.querySelector(".counter").textContent = data.likes_count;
                button.classList.toggle("liked", !isLiked);
            }
        });
    });
});
