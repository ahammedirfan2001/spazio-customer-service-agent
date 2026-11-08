
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const chatMessages = document.getElementById("chat-messages");
const sendButton = chatForm.querySelector("button");

// Handle sending messages
chatForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const message = userInput.value.trim();

    if (!message) return;

    // Display the user's message
    addMessage(message, "user-message");

    userInput.value = "";
    userInput.disabled = true;
    sendButton.disabled = true;
    sendButton.textContent = "Sending...";

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
            throw new Error("Server error");
        }

        const data = await response.json();

        addMessage(data.reply, "bot-message");

    } catch (error) {
        console.error("Chat error:", error);

        addMessage(
            "Sorry, something went wrong. Please try again.",
            "bot-message"
        );

    } finally {
        userInput.disabled = false;
        sendButton.disabled = false;
        sendButton.textContent = "Send ↗";
        userInput.focus();
    }
});


// Handle suggested questions
const suggestionButtons = document.querySelectorAll(".suggestion");

suggestionButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        userInput.value = button.dataset.prompt;
        userInput.focus();
    });
});


// Add a message to the chat
function addMessage(text, className) {
    const messageElement = document.createElement("div");

    messageElement.classList.add("message", className);
    messageElement.textContent = text;

    chatMessages.appendChild(messageElement);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}
