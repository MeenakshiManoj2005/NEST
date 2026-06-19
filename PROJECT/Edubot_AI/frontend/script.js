const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

async function sendMessage() {

    let message = userInput.value.trim();

    if (message === "") return;

    // User message
    chatBox.innerHTML += `
        <div class="user-message">${message}</div>
    `;

    userInput.value = "";

    try {

        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        chatBox.innerHTML += `
            <div class="bot-message">${data.response}</div>
        `;

    } catch (error) {

        chatBox.innerHTML += `
            <div class="bot-message">
                Server connection error!
            </div>
        `;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}