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
const savedLanguage = localStorage.getItem('language');
if (savedLanguage) {
    if (savedLanguage === 'hi') {
        document.body.classList.add('lang-hi');
    } else if (savedLanguage === 'bn') {
        document.body.classList.add('lang-bn');
    }
}

// Language toggle functionality
langToggle.addEventListener('click', () => {
    // Determine the current language and cycle to the next one
    if (document.body.classList.contains('lang-hi')) {
        // Currently Hindi, switch to Bengali
        document.body.classList.remove('lang-hi');
        document.body.classList.add('lang-bn');
        localStorage.setItem('language', 'bn');
        updatePlaceholders('bn');
    } else if (document.body.classList.contains('lang-bn')) {
        // Currently Bengali, switch to English
        document.body.classList.remove('lang-bn');
        localStorage.setItem('language', 'en');
        updatePlaceholders('en');
    } else {
        // Currently English, switch to Hindi
        document.body.classList.add('lang-hi');
        localStorage.setItem('language', 'hi');
        updatePlaceholders('hi');
    }
});

// Update input placeholders based on language
function updatePlaceholders(lang) {
    const inputs = document.querySelectorAll('input[data-placeholder-hi], input[data-placeholder-bn]');
    inputs.forEach(input => {
        // Store the original English placeholder if it hasn't been stored yet
        if (!input.getAttribute('data-placeholder-en')) {
            input.setAttribute('data-placeholder-en', input.placeholder);
        }
        
        if (lang === 'hi') {
            input.placeholder = input.getAttribute('data-placeholder-hi');
            input.style.fontFamily = "'Noto Sans Devanagari', sans-serif";
        } else if (lang === 'bn') {
            input.placeholder = input.getAttribute('data-placeholder-bn');
            input.style.fontFamily = "'Noto Sans Bengali', sans-serif";
        } else {
            input.placeholder = input.getAttribute('data-placeholder-en');
            input.style.fontFamily = "inherit";
        }
    });
}

// Store original English placeholders on page load
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input[data-placeholder-hi], input[data-placeholder-bn]');
    inputs.forEach(input => {
        input.setAttribute('data-placeholder-en', input.placeholder);
    });
    
    // Check saved language and update placeholders accordingly
    const savedLanguage = localStorage.getItem('language');
    if (savedLanguage) {
        updatePlaceholders(savedLanguage);
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
