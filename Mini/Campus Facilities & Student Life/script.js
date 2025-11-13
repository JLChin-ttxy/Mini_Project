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