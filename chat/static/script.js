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

    // File input enhancement
    document.querySelector('input[type="file"]').addEventListener('change', function(e) {
      const fileName = e.target.files[0]?.name;
      if (fileName) {
        // Add visual feedback when file is selected
        this.style.borderColor = '#10b981';
        this.style.background = 'rgba(16, 185, 129, 0.1)';
        
        // Reset after a moment
        setTimeout(() => {
          this.style.borderColor = 'rgba(59, 130, 246, 0.5)';
          this.style.background = 'rgba(15, 15, 35, 0.4)';
        }, 2000);
      }
    });

    // Add loading state to upload button
    document.querySelector('.btn-primary-custom').addEventListener('click', function(e) {
      const fileInput = document.querySelector('input[type="file"]');
      if (fileInput.files.length === 0) {
        e.preventDefault();
        alert('Please select a file to upload.');
        return;
      }
      
      // Add loading state
      this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Uploading...';
      this.disabled = true;
    });

    // Enhanced hover effects
    document.querySelector('.upload-container').addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-2px)';
      this.style.boxShadow = '0 25px 50px rgba(0, 0, 0, 0.4)';
    });

    document.querySelector('.upload-container').addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
      this.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.3)';
    });