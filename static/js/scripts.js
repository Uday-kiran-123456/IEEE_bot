async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value;
    if (message.trim() === '') return;

    // Display the user's message
    input.value = '';
    displayMessage('You: ' + message, 'sent');

    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    });
    const data = await response.json();

    // Display the bot's response
    displayMessage('Bot: ' + data.response, 'bot');
}

function displayMessage(text, type) {
    const messages = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.textContent = text;
    messageElement.classList.add('message');
    messageElement.classList.add(type); // Add 'sent' or 'bot' class

    messages.appendChild(messageElement);

    // Scroll to the bottom after new message
    messages.scrollTop = messages.scrollHeight;
}
