// ============================================================================
// University Admission Chatbot - Frontend JavaScript
// ============================================================================

// Toggle mobile menu 
const menuToggle = document.getElementById('menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');

if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', () => {
        mobileMenu.classList.toggle('show');
        
        // Animate hamburger icon
        const spans = menuToggle.querySelectorAll('span');
        if (mobileMenu.classList.contains('show')) {
            spans[0].style.transform = 'rotate(45deg) translateY(8px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translateY(-8px)';
        } else {
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });
}

// Close mobile menu when clicking a link
if (mobileMenu) {
    const mobileLinks = mobileMenu.querySelectorAll('a');
    mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.remove('show');
            const spans = menuToggle.querySelectorAll('span');
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        });
    });
}

// ============================================================================
// FAQ Toggle Functionality
// ============================================================================
document.querySelectorAll('details').forEach(detail => {
    detail.addEventListener('toggle', () => {
        const icon = detail.querySelector('summary span');
        if (icon) {
            icon.textContent = detail.open ? '-' : '+';
        }
    });
});

// ============================================================================
// Smooth Scrolling for Anchor Links
// ============================================================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// ============================================================================
// Scroll Animation Observer
// ============================================================================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards and sections for animation
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.card, .info-card, .program-card, .contact-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// ============================================================================
// Header Scroll Effect
// ============================================================================
let lastScroll = 0;
const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll <= 0) {
        header.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';
    } else {
        header.style.boxShadow = '0 4px 20px rgba(0,0,0,0.3)';
    }
    
    lastScroll = currentScroll;
});

// ============================================================================
// API Integration Functions (Optional - for direct backend queries)
// ============================================================================

const API_BASE_URL = 'http://localhost:3000/api';

/**
 * Fetch programs from backend
 */
async function fetchPrograms(params = {}) {
    try {
        const queryString = new URLSearchParams(params).toString();
        const response = await fetch(`${API_BASE_URL}/search/programs?${queryString}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching programs:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Fetch program details
 */
async function fetchProgramDetails(programId) {
    try {
        const response = await fetch(`${API_BASE_URL}/programs/${programId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching program details:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Fetch scholarships
 */
async function fetchScholarships(params = {}) {
    try {
        const queryString = new URLSearchParams(params).toString();
        const response = await fetch(`${API_BASE_URL}/scholarships?${queryString}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching scholarships:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Fetch facilities
 */
async function fetchFacilities(type = '') {
    try {
        const queryString = type ? `?type=${encodeURIComponent(type)}` : '';
        const response = await fetch(`${API_BASE_URL}/facilities${queryString}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching facilities:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Fetch student clubs
 */
async function fetchClubs(category = '') {
    try {
        const queryString = category ? `?category=${encodeURIComponent(category)}` : '';
        const response = await fetch(`${API_BASE_URL}/clubs${queryString}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching clubs:', error);
        return { success: false, error: error.message };
    }
}

// ============================================================================
// Dialogflow Messenger Interaction Helpers
// ============================================================================

/**
 * Send a message to the chatbot programmatically
 */
function askChatbot(message) {
    const dfMessenger = document.querySelector('df-messenger');
    if (dfMessenger) {
        // Open the chat
        dfMessenger.renderCustomText(message);
        
        // Ensure the chat is opened
        setTimeout(() => {
            const chatBubble = dfMessenger.shadowRoot?.querySelector('df-messenger-chat-bubble');
            if (chatBubble) {
                chatBubble.openChat();
            }
        }, 100);
    } else {
        console.warn('Dialogflow Messenger not found');
    }
}

/**
 * Handle Dialogflow Messenger events
 */
window.addEventListener('df-messenger-loaded', () => {
    console.log('✅ Dialogflow Messenger loaded successfully');
    
    const dfMessenger = document.querySelector('df-messenger');
    
    // Listen for response events
    if (dfMessenger) {
        dfMessenger.addEventListener('df-response-received', (event) => {
            console.log('Received response from chatbot:', event.detail);
        });
        
        dfMessenger.addEventListener('df-user-input-entered', (event) => {
            console.log('User input:', event.detail);
        });
    }
});

// ============================================================================
// Loading Indicator
// ============================================================================
function showLoading() {
    // Add your loading indicator logic here
    console.log('Loading...');
}

function hideLoading() {
    // Hide loading indicator
    console.log('Loading complete');
}

// ============================================================================
// Welcome Message
// ============================================================================
window.addEventListener('load', () => {
    console.log('🎓 Welcome to UTAR Admission Portal');
    console.log('💬 Chat with our AI assistant for any questions!');
});

// ============================================================================
// Error Handling
// ============================================================================
window.addEventListener('error', (event) => {
    console.error('JavaScript Error:', event.error);
});

// ============================================================================
// Service Worker Registration (Optional - for PWA)
// ============================================================================
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment if you want to add PWA functionality
        // navigator.serviceWorker.register('/sw.js')
        //     .then(registration => console.log('SW registered:', registration))
        //     .catch(error => console.log('SW registration failed:', error));
    });
}

// ============================================================================
// Export functions for use in other scripts if needed
// ============================================================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        fetchPrograms,
        fetchProgramDetails,
        fetchScholarships,
        fetchFacilities,
        fetchClubs,
        askChatbot
    };
}
