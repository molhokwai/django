
// JavaScript to handle sending messages and displaying responses
document.getElementById('send-button').addEventListener('click', function() {
    const promptInput = document.getElementById('prompt-input');
    const chatContainer = document.getElementById('chat-container');

    // Get the user's message
    const userMessage = promptInput.value.trim();
    if (userMessage === '') return;

    // Display the user's message
    const userMessageElement = document.createElement('div');
    userMessageElement.className = 'message user-message';
    userMessageElement.textContent = `You: ${userMessage}`;
    chatContainer.appendChild(userMessageElement);

    // Clear the input
    promptInput.value = '';

    // Simulate a bot response (replace with actual API call)
    setTimeout(() => {
        const botMessage = `Bot: You said "${userMessage}"`;
        const botMessageElement = document.createElement('div');
        botMessageElement.className = 'message bot-message';
        botMessageElement.textContent = botMessage;
        chatContainer.appendChild(botMessageElement);

        // Scroll to the bottom of the chat container
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }, 1000);
});

// Allow pressing Enter to send the message
document.getElementById('prompt-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        document.getElementById('send-button').click();
    }
});
