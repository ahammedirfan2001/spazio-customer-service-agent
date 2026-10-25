const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const chatMessages = document.getElementById("chat-messages");

chatForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const message = userInput.value.trim();

    if (message === "") {
        return;
    }

    addMessage(message, "user-message");

    userInput.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        if (!response.ok) {
            throw new Error("The server could not process your message.");
        }

        const data = await response.json();

        addMessage(data.reply, "bot-message");

    } catch (error) {
        addMessage(
            "Sorry, something went wrong. Please try again.",
            "bot-message"
        );

        console.error("Chat error:", error);
    }
});

function addMessage(text, className) {
    const messageElement = document.createElement("div");

    messageElement.classList.add("message", className);

    messageElement.textContent = text;

    chatMessages.appendChild(messageElement);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}