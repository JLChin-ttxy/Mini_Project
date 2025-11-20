// Toggle mobile menu 
const menuToggle = document.getElementById('menu-toggle')
const mobileMenu = document.getElementById('mobile-menu')

if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', () => {
        mobileMenu.classList.toggle('show');
    })
}

// Toggle + / - icons in <details> elements
document.querySelectorAll('details').forEach(detail => {
    detail.addEventListener('toggle', () => {
        const icon = detail.querySelector('summary span');
        if (icon) {
            icon.textContent = detail.open ? '-' : '+';
        }
    })

})

// Chatbot button & box: select elements and add a safe toggle handler
const chatbotIcon = document.getElementById('chatbot');
const chatbotBox = document.getElementById('chatbot-box');

// Ensure chatbot box is hidden by default (unless CSS already hides it)
if (chatbotBox && (chatbotBox.style.display === '' || chatbotBox.style.display === undefined)) {
    chatbotBox.style.display = 'none';
}

if (chatbotIcon && chatbotBox) {
    chatbotIcon.addEventListener('click', () => {
        chatbotBox.style.display = chatbotBox.style.display === 'none' ? 'block' : 'none';
    });
}
