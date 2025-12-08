// Original script.js - kept for compatibility
const menuToggle = document.getElementById('menu-toggle')
const mobileMenu = document.getElementById('mobile-menu')

if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', () => {
        mobileMenu.classList.toggle('show');
    })
}

document.querySelectorAll('details').forEach(detail => {
    detail.addEventListener('toggle', () => {
        const icon = detail.querySelector('summary span');
        if (icon) {
            icon.textContent = detail.open ? '-' : '+';
        }
    })
})

const chatbotIcon = document.getElementById('chatbot');
const chatbotBox = document.getElementById('chatbot-box');

if (chatbotBox && (chatbotBox.style.display === '' || chatbotBox.style.display === undefined)) {
    chatbotBox.style.display = 'none';
}

if (chatbotIcon && chatbotBox) {
    chatbotIcon.addEventListener('click', () => {
        chatbotBox.style.display = chatbotBox.style.display === 'none' ? 'block' : 'none';
    });
}


