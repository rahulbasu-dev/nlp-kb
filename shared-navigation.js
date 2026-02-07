/* ============================================
   SLIDE NAVIGATION SYSTEM - NLP Knowledge Base
   Keyboard navigation, progress tracking, and TOC
   ============================================ */

// ===== CONFIGURATION =====
const NAV_CONFIG = {
    enableKeyboardNav: true,
    enableProgressBar: true,
    enableSlideCounter: true,
    enableTOC: true,
    showKeyboardHints: true,
    keyboardHintTimeout: 5000, // ms
    scrollBehavior: 'smooth'
};

// ===== STATE =====
let currentSlideIndex = 0;
let totalSlides = 0;
let slides = [];
let isPresentationMode = false; // Default to scroll mode for better compatibility

// ===== INITIALIZATION =====
function initSlideNavigation() {
    slides = document.querySelectorAll('.slide');
    totalSlides = slides.length;

    if (totalSlides === 0) {
        console.log('No slides found, skipping navigation initialization');
        return;
    }

    // Create navigation UI
    createProgressBar();
    createSlideNav();
    createTOCOverlay();
    createPresentationModeToggle();

    // Initialize keyboard navigation
    if (NAV_CONFIG.enableKeyboardNav) {
        initKeyboardNavigation();
    }

    // Initialize scroll-based tracking
    initScrollTracking();

    // Show keyboard hints on first load
    if (NAV_CONFIG.showKeyboardHints) {
        showKeyboardHints();
    }

    // Set initial state
    updateSlideCounter();
    updateProgressBar();

    console.log(`Slide navigation initialized: ${totalSlides} slides found`);
}

// ===== PROGRESS BAR =====
function createProgressBar() {
    if (!NAV_CONFIG.enableProgressBar) return;

    const container = document.createElement('div');
    container.className = 'progress-container';
    container.innerHTML = '<div id="progressBar"></div>';
    document.body.appendChild(container);
}

function updateProgressBar() {
    const progressBar = document.getElementById('progressBar');
    if (!progressBar || totalSlides <= 1) return;

    const progress = (currentSlideIndex / (totalSlides - 1)) * 100;
    progressBar.style.width = `${progress}%`;
}

// ===== SLIDE NAVIGATION UI =====
function createSlideNav() {
    if (!NAV_CONFIG.enableSlideCounter) return;

    const nav = document.createElement('nav');
    nav.className = 'slide-nav';
    nav.setAttribute('aria-label', 'Slide navigation');
    nav.innerHTML = `
        <button id="prevSlide" aria-label="Previous slide" title="Previous (Arrow Up/Left)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
        </button>
        <span id="slideCounter" aria-live="polite">1 / ${totalSlides}</span>
        <button id="nextSlide" aria-label="Next slide" title="Next (Arrow Down/Right/Space)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
        </button>
        <button id="tocToggle" aria-label="Table of contents" title="Table of Contents (T)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <line x1="3" y1="12" x2="21" y2="12"></line>
                <line x1="3" y1="18" x2="21" y2="18"></line>
            </svg>
        </button>
    `;

    document.body.appendChild(nav);

    // Add event listeners
    document.getElementById('prevSlide').addEventListener('click', () => navigateToSlide(currentSlideIndex - 1));
    document.getElementById('nextSlide').addEventListener('click', () => navigateToSlide(currentSlideIndex + 1));
    document.getElementById('tocToggle').addEventListener('click', toggleTOC);
}

function updateSlideCounter() {
    const counter = document.getElementById('slideCounter');
    if (!counter) return;

    counter.textContent = `${currentSlideIndex + 1} / ${totalSlides}`;

    // Update button states
    const prevBtn = document.getElementById('prevSlide');
    const nextBtn = document.getElementById('nextSlide');

    if (prevBtn) prevBtn.disabled = currentSlideIndex === 0;
    if (nextBtn) nextBtn.disabled = currentSlideIndex === totalSlides - 1;
}

// ===== TABLE OF CONTENTS =====
function createTOCOverlay() {
    if (!NAV_CONFIG.enableTOC) return;

    const overlay = document.createElement('div');
    overlay.className = 'toc-overlay';
    overlay.id = 'tocOverlay';

    let tocItems = '';
    slides.forEach((slide, index) => {
        const heading = slide.querySelector('h1, h2');
        const title = heading ? heading.textContent : `Slide ${index + 1}`;
        tocItems += `<li data-slide="${index}" class="${index === currentSlideIndex ? 'current' : ''}">${title}</li>`;
    });

    overlay.innerHTML = `
        <div class="toc-content">
            <h3>Table of Contents</h3>
            <ol>${tocItems}</ol>
            <p style="text-align: center; margin-top: 1.5rem; color: var(--text-tertiary);">
                Press <kbd>T</kbd> or <kbd>Esc</kbd> to close
            </p>
        </div>
    `;

    document.body.appendChild(overlay);

    // Add click handlers for TOC items
    overlay.querySelectorAll('li[data-slide]').forEach(item => {
        item.addEventListener('click', () => {
            const slideIndex = parseInt(item.getAttribute('data-slide'));
            navigateToSlide(slideIndex);
            toggleTOC();
        });
    });

    // Close on backdrop click
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) toggleTOC();
    });
}

function toggleTOC() {
    const overlay = document.getElementById('tocOverlay');
    if (!overlay) return;

    overlay.classList.toggle('show');

    // Update current slide highlight
    overlay.querySelectorAll('li[data-slide]').forEach((item, index) => {
        item.classList.toggle('current', index === currentSlideIndex);
    });
}

// ===== PRESENTATION MODE TOGGLE =====
function createPresentationModeToggle() {
    const toggle = document.createElement('button');
    toggle.className = 'presentation-mode-toggle';
    toggle.id = 'presentationModeToggle';
    toggle.setAttribute('aria-label', 'Toggle snap mode');
    // Default is scroll mode (isPresentationMode = false), so show snap icon
    toggle.title = 'Switch to Snap Mode (P)';
    toggle.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>';

    toggle.addEventListener('click', togglePresentationMode);
    document.body.appendChild(toggle);
}

function togglePresentationMode() {
    isPresentationMode = !isPresentationMode;
    const presentation = document.querySelector('.presentation');
    const toggle = document.getElementById('presentationModeToggle');

    if (presentation) {
        // Toggle between snap-mode (presentation) and scroll-mode
        presentation.classList.toggle('snap-mode', isPresentationMode);
        presentation.classList.toggle('scroll-mode', !isPresentationMode);
    }

    if (toggle) {
        toggle.innerHTML = isPresentationMode ?
            '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>' :
            '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>';
        toggle.title = isPresentationMode ? 'Switch to Scroll Mode (P)' : 'Switch to Snap Mode (P)';
    }
}

// ===== KEYBOARD NAVIGATION =====
function initKeyboardNavigation() {
    document.addEventListener('keydown', (e) => {
        // Don't navigate if user is typing in an input
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable) {
            return;
        }

        // Check for TOC visibility
        const tocVisible = document.getElementById('tocOverlay')?.classList.contains('show');

        switch (e.key) {
            case 'ArrowDown':
            case 'ArrowRight':
                if (!tocVisible) {
                    e.preventDefault();
                    navigateToSlide(currentSlideIndex + 1);
                }
                break;

            case 'ArrowUp':
            case 'ArrowLeft':
                if (!tocVisible) {
                    e.preventDefault();
                    navigateToSlide(currentSlideIndex - 1);
                }
                break;

            case ' ': // Spacebar
                if (!tocVisible) {
                    e.preventDefault();
                    navigateToSlide(currentSlideIndex + 1);
                }
                break;

            case 'Home':
                if (!tocVisible) {
                    e.preventDefault();
                    navigateToSlide(0);
                }
                break;

            case 'End':
                if (!tocVisible) {
                    e.preventDefault();
                    navigateToSlide(totalSlides - 1);
                }
                break;

            case 't':
            case 'T':
                e.preventDefault();
                toggleTOC();
                break;

            case 'Escape':
                if (tocVisible) {
                    e.preventDefault();
                    toggleTOC();
                }
                break;

            case 'p':
            case 'P':
                e.preventDefault();
                togglePresentationMode();
                break;

            case 'f':
            case 'F':
                e.preventDefault();
                toggleFullscreen();
                break;
        }
    });
}

// ===== SLIDE NAVIGATION =====
function navigateToSlide(index) {
    // Bounds checking
    if (index < 0 || index >= totalSlides) return;

    currentSlideIndex = index;
    const targetSlide = slides[index];

    // Always use scroll with offset for nav (works in both modes)
    const navHeight = document.querySelector('nav:not(.slide-nav)')?.offsetHeight || 0;
    const targetPosition = targetSlide.offsetTop - navHeight - 20;

    window.scrollTo({
        top: targetPosition,
        behavior: NAV_CONFIG.scrollBehavior
    });

    updateSlideCounter();
    updateProgressBar();
}

function getCurrentSlideIndex() {
    return currentSlideIndex;
}

// ===== SCROLL TRACKING =====
function initScrollTracking() {
    // Use Intersection Observer for better performance
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && entry.intersectionRatio > 0.3) {
                const index = Array.from(slides).indexOf(entry.target);
                if (index !== -1 && index !== currentSlideIndex) {
                    currentSlideIndex = index;
                    updateSlideCounter();
                    updateProgressBar();
                }
            }
        });
    }, {
        threshold: [0.3, 0.5, 0.7],
        rootMargin: '-10% 0px -10% 0px'
    });

    slides.forEach(slide => observer.observe(slide));
}

// ===== FULLSCREEN =====
function toggleFullscreen() {
    const presentation = document.querySelector('.presentation') || document.documentElement;

    if (!document.fullscreenElement) {
        presentation.requestFullscreen().catch(err => {
            console.log(`Error attempting to enable fullscreen: ${err.message}`);
        });
    } else {
        document.exitFullscreen();
    }
}

// ===== KEYBOARD HINTS =====
function showKeyboardHints() {
    const hints = document.createElement('div');
    hints.className = 'keyboard-hints show';
    hints.innerHTML = `
        <kbd>↑</kbd><kbd>↓</kbd> or <kbd>←</kbd><kbd>→</kbd> Navigate sections &nbsp;
        <kbd>T</kbd> Contents &nbsp;
        <kbd>F</kbd> Fullscreen
    `;
    document.body.appendChild(hints);

    // Hide after timeout
    setTimeout(() => {
        hints.classList.remove('show');
        setTimeout(() => hints.remove(), 300);
    }, NAV_CONFIG.keyboardHintTimeout);
}

// ===== UTILITY: Get slide by ID or index =====
function getSlide(identifier) {
    if (typeof identifier === 'number') {
        return slides[identifier] || null;
    }
    return document.getElementById(identifier) || document.querySelector(identifier);
}

// ===== INITIALIZATION ON DOM READY =====
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if we have slides
    if (document.querySelector('.slide')) {
        initSlideNavigation();
    }
});

// ===== EXPORTS FOR EXTERNAL USE =====
window.SlideNav = {
    navigateToSlide,
    getCurrentSlideIndex,
    toggleTOC,
    togglePresentationMode,
    toggleFullscreen,
    getSlide,
    getTotalSlides: () => totalSlides
};
