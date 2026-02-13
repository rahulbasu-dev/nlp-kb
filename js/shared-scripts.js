/* ============================================
   SHARED JAVASCRIPT - NLP Knowledge Base
   ============================================ */

// Section Toggle Functionality
function initSectionToggles() {
    // Find all section elements
    const sections = document.querySelectorAll('.section, section');

    sections.forEach(section => {
        // Find the section heading (h2)
        const heading = section.querySelector('h2');
        if (!heading) return;

        // Skip if toggle already added
        if (heading.querySelector('.section-toggle-btn')) return;

        // Create toggle button
        const toggleBtn = document.createElement('span');
        toggleBtn.className = 'section-toggle-btn';
        toggleBtn.innerHTML = '▼';
        toggleBtn.style.cssText = `
            float: right;
            cursor: pointer;
            font-size: 0.8em;
            transition: transform 0.3s ease;
            margin-left: 10px;
        `;

        // Add button to heading
        heading.style.cursor = 'pointer';
        heading.style.userSelect = 'none';
        heading.appendChild(toggleBtn);

        // Get section content (everything except the h2)
        const content = Array.from(section.children).filter(child => child !== heading);

        // Wrap content in a container for toggling
        const contentWrapper = document.createElement('div');
        contentWrapper.className = 'section-content-wrapper';
        contentWrapper.style.cssText = `
            overflow: hidden;
            transition: max-height 0.4s ease, opacity 0.3s ease;
        `;

        // Move all content into wrapper
        content.forEach(child => contentWrapper.appendChild(child));
        section.appendChild(contentWrapper);

        // Toggle function
        const toggleSection = () => {
            const isCollapsed = contentWrapper.classList.contains('collapsed');

            if (isCollapsed) {
                // Expand
                contentWrapper.classList.remove('collapsed');
                contentWrapper.style.maxHeight = contentWrapper.scrollHeight + 'px';
                contentWrapper.style.opacity = '1';
                toggleBtn.style.transform = 'rotate(0deg)';
            } else {
                // Collapse
                contentWrapper.classList.add('collapsed');
                contentWrapper.style.maxHeight = '0';
                contentWrapper.style.opacity = '0';
                toggleBtn.style.transform = 'rotate(-90deg)';
            }
        };

        // Add click listener to heading
        heading.addEventListener('click', toggleSection);
    });
}

// Solution Toggle Functionality
function initSolutionToggles() {
    // Find all solution toggle buttons
    const toggleButtons = document.querySelectorAll('.solution-toggle');

    toggleButtons.forEach(button => {
        // Ensure solutions are hidden by default
        const solutionId = button.getAttribute('data-solution-id') || button.getAttribute('onclick')?.match(/toggleSolution\(['"]([^'"]+)['"]\)/)?.[1];

        if (solutionId) {
            const solution = document.getElementById(solutionId);
            if (solution && !solution.classList.contains('show')) {
                solution.style.maxHeight = '0';
                solution.style.opacity = '0';
                solution.style.padding = '0';
            }
        }

        // Add click event listener
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const id = this.getAttribute('data-solution-id') || this.getAttribute('onclick')?.match(/toggleSolution\(['"]([^'"]+)['"]\)/)?.[1];
            if (id) {
                toggleSolution(id);
                this.classList.toggle('active');
            }
        });
    });

    // Also handle buttons with onclick="toggleSolution(...)"
    document.querySelectorAll('button[onclick*="toggleSolution"]').forEach(button => {
        const match = button.getAttribute('onclick').match(/toggleSolution\(['"]([^'"]+)['"]\)/);
        if (match) {
            const solutionId = match[1];
            button.setAttribute('data-solution-id', solutionId);
            button.removeAttribute('onclick');

            button.addEventListener('click', function(e) {
                e.preventDefault();
                toggleSolution(solutionId);
                this.classList.toggle('active');
            });
        }
    });
}

function toggleSolution(id) {
    const solution = document.getElementById(id);
    if (!solution) return;

    const isShowing = solution.classList.contains('show');

    if (isShowing) {
        // Hide
        solution.style.maxHeight = '0';
        solution.style.opacity = '0';
        solution.style.padding = '0';
        solution.classList.remove('show');
    } else {
        // Show
        solution.classList.add('show');
        solution.style.maxHeight = solution.scrollHeight + 'px';
        solution.style.opacity = '1';

        // Scroll to solution after a brief delay
        setTimeout(() => {
            solution.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
    }
}

// Smooth scroll for anchor links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                const navHeight = document.querySelector('nav')?.offsetHeight || 0;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight - 20;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Add fade-in animation to sections as they come into view
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    document.querySelectorAll('.section, .content-block').forEach(el => {
        observer.observe(el);
    });
}

// Initialize all functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initSectionToggles();
    initSolutionToggles();
    initSmoothScroll();
    initScrollAnimations();

    // Log initialization
    console.log('✅ NLP Knowledge Base UI initialized');
});

// Expose functions globally for inline onclick handlers (backwards compatibility)
window.toggleSolution = toggleSolution;
