// Main JavaScript for SKL University Website

// Toggle mobile menu
const menuToggle = document.getElementById('menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');

if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', () => {
        mobileMenu.classList.toggle('show');
    });
}

// Toggle + / - icons in <details> elements
document.querySelectorAll('details').forEach(detail => {
    detail.addEventListener('toggle', () => {
        const icon = detail.querySelector('summary span');
        if (icon) {
            icon.textContent = detail.open ? '-' : '+';
        }
    });
});

// Chatbot functionality
const chatbotBtn = document.getElementById('chatbot') || document.querySelector('.chatbot-btn');
const chatbotBox = document.getElementById('chatbot-box') || document.querySelector('.chatbot-box');
const chatbotClose = document.getElementById('chatbot-close');
const chatbotInput = document.getElementById('chatbot-input-field');
const chatbotSend = document.getElementById('chatbot-send');
const chatbotMessages = document.getElementById('chatbot-messages');

// Initialize chatbot
if (chatbotBtn && chatbotBox) {
    // Ensure chatbot box is hidden by default
    if (chatbotBox.style.display === '' || chatbotBox.style.display === undefined) {
        chatbotBox.style.display = 'none';
    }

    // Toggle chatbot
    chatbotBtn.addEventListener('click', () => {
        const isVisible = chatbotBox.style.display === 'block' || chatbotBox.classList.contains('show');
        if (isVisible) {
            chatbotBox.style.display = 'none';
            chatbotBox.classList.remove('show');
        } else {
            chatbotBox.style.display = 'flex';
            chatbotBox.classList.add('show');
            chatbotInput?.focus();
        }
    });

    // Close chatbot
    if (chatbotClose) {
        chatbotClose.addEventListener('click', () => {
            chatbotBox.style.display = 'none';
            chatbotBox.classList.remove('show');
        });
    }

    // Send message
    function sendMessage() {
        const message = chatbotInput?.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage('user', message);
        chatbotInput.value = '';

        // Send to server
        fetch('/chatbot/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            addMessage('bot', data.response);
            
            // Add suggestions if available
            if (data.suggestions && data.suggestions.length > 0) {
                addSuggestions(data.suggestions);
            }
        })
        .catch(error => {
            addMessage('bot', 'Sorry, I encountered an error. Please try again.');
            console.error('Error:', error);
        });
    }

    // Add message to chat
    function addMessage(type, text) {
        if (!chatbotMessages) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message ${type}`;
        messageDiv.textContent = text;
        chatbotMessages.appendChild(messageDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Add suggestions
    function addSuggestions(suggestions) {
        if (!chatbotMessages) return;

        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.className = 'chatbot-suggestions mt-2';
        suggestionsDiv.innerHTML = suggestions.map(s => 
            `<button class="btn btn-sm btn-outline-primary me-1 mb-1 suggestion-btn">${s}</button>`
        ).join('');

        chatbotMessages.appendChild(suggestionsDiv);

        // Add click handlers
        suggestionsDiv.querySelectorAll('.suggestion-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                chatbotInput.value = btn.textContent;
                sendMessage();
            });
        });

        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Send button click
    if (chatbotSend) {
        chatbotSend.addEventListener('click', sendMessage);
    }

    // Enter key press
    if (chatbotInput) {
        chatbotInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Load chat history on open
    chatbotBtn.addEventListener('click', () => {
        if (chatbotBox.style.display === 'flex' || chatbotBox.classList.contains('show')) {
            loadChatHistory();
        }
    });
}

// Load chat history
function loadChatHistory() {
    fetch('/chatbot/history')
        .then(response => response.json())
        .then(data => {
            if (data.messages && data.messages.length > 0 && chatbotMessages) {
                chatbotMessages.innerHTML = '';
                data.messages.forEach(msg => {
                    const type = msg.sender_type.toLowerCase();
                    addMessage(type === 'user' ? 'user' : 'bot', msg.message_text);
                });
            }
        })
        .catch(error => console.error('Error loading history:', error));
}

// Global function to open chatbot
function openChatbot() {
    if (chatbotBox) {
        chatbotBox.style.display = 'flex';
        chatbotBox.classList.add('show');
        if (chatbotInput) {
            chatbotInput.focus();
        }
        loadChatHistory();
    }
}


