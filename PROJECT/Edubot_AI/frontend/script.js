const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

async function sendMessage() {

    const message = userInput.value.trim();

    if (!message) return;

    chatBox.innerHTML += `
        <div class="user-message">${message}</div>
    `;

    userInput.value = "";

    const loading = document.createElement("div");
    loading.className = "bot-message";
    loading.innerText = "Typing...";
    chatBox.appendChild(loading);

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/chat",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message: message
                })
            }
        );

        const data = await response.json();

        loading.remove();

        chatBox.innerHTML += `
            <div class="bot-message">
                ${data.response || data.detail || "No response"}
            </div>
        `;

    } catch (error) {

        loading.remove();

        chatBox.innerHTML += `
            <div class="bot-message">
                Error connecting to backend.
            </div>
        `;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});
