// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const themeIcon = themeToggle.querySelector('i');

// Check for saved theme preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
    themeIcon.classList.remove('far', 'fa-moon');
    themeIcon.classList.add('fas', 'fa-sun');
}

// Theme toggle functionality
themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    
    if (document.body.classList.contains('dark-mode')) {
        themeIcon.classList.remove('far', 'fa-moon');
        themeIcon.classList.add('fas', 'fa-sun');
        localStorage.setItem('darkMode', 'true');
    } else {
        themeIcon.classList.remove('fas', 'fa-sun');
        themeIcon.classList.add('far', 'fa-moon');
        localStorage.setItem('darkMode', 'false');
    }
});

// Language Toggle
const langToggle = document.getElementById('langToggle');

// Check for saved language preference
if (localStorage.getItem('language') === 'hi') {
    document.body.classList.add('lang-hi');
}

// Language toggle functionality
langToggle.addEventListener('click', () => {
    document.body.classList.toggle('lang-hi');
    
    if (document.body.classList.contains('lang-hi')) {
        localStorage.setItem('language', 'hi');
        updatePlaceholders('hi');
    } else {
        localStorage.setItem('language', 'en');
        updatePlaceholders('en');
    }
});

// Update input placeholders based on language
function updatePlaceholders(lang) {
    const inputs = document.querySelectorAll('input[data-placeholder-hi]');
    inputs.forEach(input => {
        // Store the original English placeholder if it hasn't been stored yet
        if (!input.getAttribute('data-placeholder-en')) {
            input.setAttribute('data-placeholder-en', input.placeholder);
        }
        
        if (lang === 'hi') {
            input.placeholder = input.getAttribute('data-placeholder-hi');
            input.style.fontFamily = "'Noto Sans Devanagari', sans-serif";
        } else {
            input.placeholder = input.getAttribute('data-placeholder-en');
            input.style.fontFamily = "inherit";
        }
    });
}

// Store original English placeholders on page load
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input[data-placeholder-hi]');
    inputs.forEach(input => {
        input.setAttribute('data-placeholder-en', input.placeholder);
    });
    
    // If the language is already set to Hindi, update placeholders accordingly
    if (localStorage.getItem('language') === 'hi') {
        updatePlaceholders('hi');
    }
});

// The initialization of placeholders is now handled in the DOMContentLoaded event above

// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const navMenu = document.getElementById('navMenu');

mobileMenuBtn.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    
    // Change icon based on menu state
    const icon = mobileMenuBtn.querySelector('i');
    if (navMenu.classList.contains('active')) {
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
    } else {
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    }
});
