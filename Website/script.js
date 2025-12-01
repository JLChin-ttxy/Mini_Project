// Toggle mobile menu 
const menuToggle = document.getElementById('menu-toggle')
const mobileMenu = document.getElementById('mobile-menu')

menuToggle?.addEventListener('click', () => {
    mobileMenu.classList.toggle('show');
});

// Toggle + / - icons in <details> elements
document.querySelectorAll('details').forEach(detail => {
    detail.addEventListener('toggle', () => {
        const icon = detail.querySelector('summary span');
        if (icon) {
            icon.textContent = detail.open ? '-' : '+';
        }
    })

})

// ================= FACILITY FILTER + SEARCH =================
// script.js (improved filter + search, robust & animated)
document.addEventListener('DOMContentLoaded', () => {
  // Select elements
  const filterButtons = document.querySelectorAll('.filter-btn');
  const searchBox = document.getElementById('facilitySearch');
  const cards = Array.from(document.querySelectorAll('.card'));

  // Safety: if no cards, nothing to do
  if (!cards.length) return;

  let currentFilter = 'all';
  const FADE_MS = 250; // must match CSS transition duration

  // Helper: show a card with fade-in
  function showCard(card) {
    // ensure visible for measuring and transition
    card.style.display = ''; // remove explicit display (fallback to CSS)
    // force reflow to allow transition
    requestAnimationFrame(() => {
      card.classList.remove('hide');
      card.classList.add('show');
    });
  }

  // Helper: hide a card with fade-out then set display none
  function hideCard(card) {
    // start fade-out
    card.classList.remove('show');
    card.classList.add('hide');

    // after transition, hide from layout
    setTimeout(() => {
      // only set display none if still hidden
      if (card.classList.contains('hide')) {
        card.style.display = 'none';
      }
    }, FADE_MS + 20);
  }

  // Apply combined filter + search logic
  function applyFilters() {
    const query = (searchBox?.value || '').toLowerCase().trim();

    cards.forEach(card => {
      const cat = (card.dataset.category || '').toLowerCase();
      const text = card.textContent.toLowerCase();

      const matchesCategory = (currentFilter === 'all') || (cat === currentFilter);
      const matchesSearch = query === '' || text.includes(query);

      if (matchesCategory && matchesSearch) {
        showCard(card);
      } else {
        hideCard(card);
      }
    });
  }

  // Initialize: ensure cards have show/hide baseline classes
  cards.forEach(card => {
    // remove inline display none if present, then compute initial state via classes
    if (!card.classList.contains('show') && !card.classList.contains('hide')) {
      card.classList.add('show');
    }
  });

  // Wire up filter buttons (if present)
  if (filterButtons.length) {
    filterButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        // update current filter
        currentFilter = btn.dataset.filter || 'all';

        // update active state
        filterButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        applyFilters();
      });
    });
  }

  // Wire up search box (if present)
  if (searchBox) {
    searchBox.addEventListener('input', () => {
      applyFilters();
    });
  }

  // Initial run
  applyFilters();
});

// ================= STUDENT CLUBS =================
function showClubInfo(club) {
    alert(`You selected: ${club}\n\nRegistration via Student Affairs.`);
}

// ================= VIRTUAL TOUR =================
function loadTour(area) {
    alert("Loading virtual tour for: " + area);
}