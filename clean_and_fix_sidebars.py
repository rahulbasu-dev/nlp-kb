"""
Clean remove all sidebar code and add fresh, working sidebar
"""

import re

CLEAN_SIDEBAR_HTML = '''    <!-- Navigation Sidebar -->
    <aside class="nlp-sidebar" id="nlpSidebar">
        <div class="nlp-sidebar-header">
            <h2>🧠 NLP Guide</h2>
            <p>Interactive Learning Resources</p>
        </div>

        <nav class="nlp-sidebar-nav">
            <div class="nlp-sidebar-section">
                <div class="nlp-sidebar-section-title">MAIN</div>
                <a href="nlp_guide_index.html" class="nlp-sidebar-link">
                    <span class="nlp-icon">🏠</span>
                    <span>Home</span>
                </a>
                <a href="methods_comparison.html" class="nlp-sidebar-link">
                    <span class="nlp-icon">🔬</span>
                    <span>Methods Comparison</span>
                </a>
            </div>

            <div class="nlp-sidebar-section">
                <div class="nlp-sidebar-section-title">FOUNDATIONS</div>
                <a href="neural_networks_educational.html" class="nlp-sidebar-link">
                    <span class="nlp-icon">🧠</span>
                    <span>Neural Networks</span>
                </a>
                <a href="tfidf_educational.html" class="nlp-sidebar-link">
                    <span class="nlp-icon">📊</span>
                    <span>TF-IDF</span>
                </a>
            </div>

            <div class="nlp-sidebar-section">
                <div class="nlp-sidebar-section-title">WORD EMBEDDINGS</div>
                <a href="word2vec_educational.html" class="nlp-sidebar-link">
                    <span class="nlp-icon">🎯</span>
                    <span>Word2Vec</span>
                </a>
                <a href="sgns_educational.html" class="nlp-sidebar-link">
                    <span class="nlp-icon">⚡</span>
                    <span>Skip-gram (SGNS)</span>
                </a>
                <a href="cbow_educational.html" class="nlp-sidebar-link">
                    <span class="nlp-icon">🎪</span>
                    <span>CBOW</span>
                </a>
                <a href="glove_educational.html" class="nlp-sidebar-link">
                    <span class="nlp-icon">🌍</span>
                    <span>GloVe</span>
                </a>
            </div>
        </nav>
    </aside>

    <!-- Mobile Sidebar Toggle -->
    <button class="nlp-sidebar-toggle" onclick="toggleNLPSidebar()" aria-label="Toggle Navigation">☰</button>

'''

CLEAN_SIDEBAR_CSS = '''
/* ============================================
   NLP Navigation Sidebar - Clean Implementation
   ============================================ */
.nlp-sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: 280px;
    height: 100vh;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    padding: 2rem 0;
    overflow-y: auto;
    z-index: 10000;
    box-shadow: 4px 0 10px rgba(0,0,0,0.1);
}

.nlp-sidebar-header {
    padding: 0 1.5rem 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.2);
    margin-bottom: 1.5rem;
}

.nlp-sidebar-header h2 {
    color: white;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
}

.nlp-sidebar-header p {
    color: white;
    font-size: 0.85rem;
    margin: 0;
    opacity: 0.9;
}

.nlp-sidebar-nav {
    padding: 0 1rem;
}

.nlp-sidebar-section {
    margin-bottom: 2rem;
}

.nlp-sidebar-section-title {
    color: rgba(255,255,255,0.7);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
    padding: 0 0.5rem;
    margin-bottom: 0.75rem;
}

.nlp-sidebar-link {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 0.5rem;
    color: white;
    text-decoration: none;
    border-radius: 0.5rem;
    transition: all 0.2s ease;
    font-size: 0.95rem;
}

.nlp-sidebar-link:hover {
    background: rgba(255,255,255,0.15);
    transform: translateX(5px);
}

.nlp-sidebar-link.active {
    background: rgba(255,255,255,0.2);
    font-weight: 600;
}

.nlp-icon {
    font-size: 1.25rem;
    width: 24px;
    text-align: center;
}

/* Adjust main content to account for sidebar */
body {
    margin-left: 280px;
}

/* Mobile toggle button */
.nlp-sidebar-toggle {
    display: none;
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    width: 60px;
    height: 60px;
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 50%;
    font-size: 1.5rem;
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    z-index: 9999;
}

/* Responsive */
@media (max-width: 768px) {
    .nlp-sidebar {
        transform: translateX(-100%);
        transition: transform 0.3s ease;
    }

    .nlp-sidebar.open {
        transform: translateX(0);
    }

    body {
        margin-left: 0;
    }

    .nlp-sidebar-toggle {
        display: block;
    }
}
'''

CLEAN_SIDEBAR_JS = '''
<script>
function toggleNLPSidebar() {
    document.getElementById('nlpSidebar').classList.toggle('open');
}

// Close sidebar when clicking outside on mobile
document.addEventListener('click', function(event) {
    const sidebar = document.getElementById('nlpSidebar');
    const toggle = document.querySelector('.nlp-sidebar-toggle');
    if (window.innerWidth <= 768 && sidebar && sidebar.classList.contains('open') &&
        !sidebar.contains(event.target) && (!toggle || !toggle.contains(event.target))) {
        sidebar.classList.remove('open');
    }
});

// Highlight active page
document.addEventListener('DOMContentLoaded', function() {
    const currentPage = window.location.pathname.split('/').pop();
    document.querySelectorAll('.nlp-sidebar-link').forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
});
</script>
'''

def clean_and_add_sidebar(filepath):
    """Remove all old sidebar code and add clean new sidebar"""
    print(f"Processing {filepath}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove ALL old sidebar-related content
    content = re.sub(r'<!--.*?Navigation Sidebar.*?-->.*?(?=<!--|\<nav|\<header|\<main|\<section)', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<div class="sidebar".*?</div>.*?(?=<\w+)', '', content, flags=re.DOTALL)
    content = re.sub(r'<aside class=".*?sidebar.*?</aside>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<button class=".*?sidebar-toggle.*?</button>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<div class="content-wrapper">.*?(?=<\w+)', '<div class="content-wrapper">', content, flags=re.DOTALL)
    content = re.sub(r'</div><!--.*?end content-wrapper.*?-->', '', content, flags=re.IGNORECASE)
    content = re.sub(r'/\*.*?Navigation Sidebar.*?\*/', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'\.sidebar.*?\{.*?\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\.nlp-sidebar.*?\{.*?\}', '', content, flags=re.DOTALL)

    # Remove old sidebar JavaScript
    content = re.sub(r'<script>.*?function toggleSidebar.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<script>.*?toggleNLPSidebar.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)

    # Add clean CSS before </style>
    style_end = content.rfind('</style>')
    if style_end != -1:
        content = content[:style_end] + '\n' + CLEAN_SIDEBAR_CSS + '\n' + content[style_end:]
        print(f"  [OK] Added clean sidebar CSS")

    # Add sidebar HTML right after <body>
    body_start = content.find('<body>')
    if body_start != -1:
        insert_pos = body_start + len('<body>')
        content = content[:insert_pos] + '\n' + CLEAN_SIDEBAR_HTML + content[insert_pos:]
        print(f"  [OK] Added clean sidebar HTML")

    # Add JavaScript before </body>
    body_end = content.rfind('</body>')
    if body_end != -1:
        content = content[:body_end] + CLEAN_SIDEBAR_JS + '\n' + content[body_end:]
        print(f"  [OK] Added sidebar JavaScript")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  [SUCCESS] {filepath} updated!\n")

def main():
    import os
    base_dir = r'C:\GitHub\me\nlp\kb'

    files = [
        'neural_networks_educational.html',
        'cbow_educational.html',
        'glove_educational.html',
        'methods_comparison.html',
        'sgns_educational.html',
        'tfidf_educational.html',
        'word2vec_educational.html'
    ]

    print("="*60)
    print("Clean Sidebar Implementation")
    print("="*60)
    print()

    for filename in files:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            clean_and_add_sidebar(filepath)

    print("="*60)
    print("[COMPLETE] All pages updated with clean sidebars!")
    print("="*60)

if __name__ == '__main__':
    main()
