async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value;
    if (message.trim() === '') return;
    
    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    });
    const data = await response.json();
    displayMessage('You: ' + message);
    displayMessage('Bot: ' + data.response);
    input.value = '';
}

function displayMessage(text) {
    const messages = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.textContent = text;
    messages.appendChild(messageElement);
}
