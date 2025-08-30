document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("chat-form");
    const messages = document.querySelector(".messages");

    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            const input = document.getElementById("user-input");
            const text = input.value.trim();
            if (!text) return;

            // Append user message
            const userMsg = document.createElement("div");
            userMsg.className = "message user-msg";
            userMsg.textContent = text;
            messages.appendChild(userMsg);

            // Append loading bot message
            const botMsg = document.createElement("div");
            botMsg.className = "message bot-msg";
            botMsg.textContent = "Bot is Thinking...";
            messages.appendChild(botMsg);

            messages.scrollTop = messages.scrollHeight;
            input.value = "";

            try {
                // Send query to Django backend
                const response = await fetch(window.location.href, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                        "X-Requested-With": "XMLHttpRequest",
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: new URLSearchParams({ query: text })
                });

                const data = await response.json();

                
                botMsg.textContent = "Bot says " + data.answer;
            } catch (err) {
                botMsg.textContent = "⚠️ Error talking to server.";
                console.error(err);
            }

            messages.scrollTop = messages.scrollHeight;
        });
    }
});


function getCSRFToken() {
    let cookieValue = null;
    const cookies = document.cookie ? document.cookie.split(";") : [];
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, 10) === "csrftoken=") {
            cookieValue = decodeURIComponent(cookie.substring(10));
            break;
        }
    }
    return cookieValue;
}
