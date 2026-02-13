"""
Add consistent navigation sidebar to all educational pages
"""

import re
import os

# Sidebar HTML template
SIDEBAR_HTML = '''    <!-- Navigation Sidebar -->
    <div class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <h2>🧠 NLP Guide</h2>
            <p>Interactive Learning Resources</p>
        </div>

        <nav class="sidebar-nav">
            <div class="sidebar-section">
                <div class="sidebar-section-title">MAIN</div>
                <a href="nlp_guide_index.html" class="sidebar-link">
                    <span class="icon">🏠</span>
                    <span>Home</span>
                </a>
                <a href="methods_comparison.html" class="sidebar-link">
                    <span class="icon">🔬</span>
                    <span>Methods Comparison</span>
                </a>
            </div>

            <div class="sidebar-section">
                <div class="sidebar-section-title">FOUNDATIONS</div>
                <a href="neural_networks_educational.html" class="sidebar-link">
                    <span class="icon">🧠</span>
                    <span>Neural Networks</span>
                </a>
                <a href="tfidf_educational.html" class="sidebar-link">
                    <span class="icon">📊</span>
                    <span>TF-IDF</span>
                </a>
            </div>

            <div class="sidebar-section">
                <div class="sidebar-section-title">WORD EMBEDDINGS</div>
                <a href="word2vec_educational.html" class="sidebar-link">
                    <span class="icon">🎯</span>
                    <span>Word2Vec</span>
                </a>
                <a href="sgns_educational.html" class="sidebar-link">
                    <span class="icon">⚡</span>
                    <span>Skip-gram (SGNS)</span>
                </a>
                <a href="cbow_educational.html" class="sidebar-link">
                    <span class="icon">🎪</span>
                    <span>CBOW</span>
                </a>
                <a href="glove_educational.html" class="sidebar-link">
                    <span class="icon">🌍</span>
                    <span>GloVe</span>
                </a>
            </div>
        </nav>
    </div>

    <!-- Mobile Toggle Button -->
    <button class="sidebar-toggle" onclick="toggleSidebar()" aria-label="Toggle Sidebar">
        ☰
    </button>

    <!-- Main Content Wrapper -->
    <div class="content-wrapper">
'''

# Sidebar CSS
SIDEBAR_CSS = '''
        /* Navigation Sidebar Styles */
        body {
            margin: 0;
            padding: 0;
        }

        .sidebar {
            position: fixed;
            left: 0;
            top: 0;
            width: 280px;
            height: 100vh;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            padding: 2rem 0;
            overflow-y: auto;
            z-index: 1000;
            box-shadow: 4px 0 10px rgba(0,0,0,0.1);
        }

        .sidebar-header {
            padding: 0 1.5rem 1.5rem;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            margin-bottom: 1.5rem;
        }

        .sidebar-header h2 {
            color: white !important;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .sidebar-header p {
            color: rgba(255,255,255,1);
            font-size: 0.85rem;
        }

        .sidebar-nav {
            padding: 0 1rem;
        }

        .sidebar-section {
            margin-bottom: 2rem;
        }

        .sidebar-section-title {
            color: rgba(255,255,255,0.95);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
            padding: 0 0.5rem;
            margin-bottom: 0.75rem;
        }

        .sidebar-link {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 0.5rem;
            color: rgba(255,255,255,1);
            text-decoration: none;
            border-radius: 0.5rem;
            transition: all 0.2s ease;
            font-size: 0.95rem;
        }

        .sidebar-link:hover {
            background: rgba(255,255,255,0.15);
            color: white;
            transform: translateX(5px);
        }

        .sidebar-link.active {
            background: rgba(255,255,255,0.2);
            color: white;
            font-weight: 600;
        }

        .sidebar-link .icon {
            font-size: 1.25rem;
            width: 24px;
            text-align: center;
        }

        .content-wrapper {
            margin-left: 280px;
            min-height: 100vh;
        }

        /* Sidebar Toggle Button for Mobile */
        .sidebar-toggle {
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
            z-index: 999;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .sidebar {
                transform: translateX(-100%);
                transition: transform 0.3s ease;
            }

            .sidebar.open {
                transform: translateX(0);
            }

            .content-wrapper {
                margin-left: 0;
            }

            .sidebar-toggle {
                display: block;
            }
        }

        /* Ensure sidebar headers stay white */
        .sidebar h1, .sidebar h2, .sidebar h3, .sidebar h4, .sidebar h5, .sidebar h6 {
            color: white !important;
        }
'''

# Sidebar JavaScript
SIDEBAR_JS = '''
    <script>
        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            sidebar.classList.toggle('open');
        }

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', function(event) {
            const sidebar = document.getElementById('sidebar');
            const toggle = document.querySelector('.sidebar-toggle');

            if (window.innerWidth <= 768 &&
                sidebar && sidebar.classList.contains('open') &&
                !sidebar.contains(event.target) &&
                toggle && !toggle.contains(event.target)) {
                sidebar.classList.remove('open');
            }
        });

        // Highlight active page in sidebar
        document.addEventListener('DOMContentLoaded', function() {
            const currentPage = window.location.pathname.split('/').pop();
            const links = document.querySelectorAll('.sidebar-link');
            links.forEach(link => {
                const href = link.getAttribute('href');
                if (href === currentPage) {
                    link.classList.add('active');
                }
            });
        });
    </script>
'''

def add_sidebar_to_file(filepath):
    """Add sidebar to a single HTML file"""
    print(f"Processing {filepath}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if sidebar already exists
    if 'class="sidebar"' in content:
        print(f"  Sidebar already exists in {filepath}, skipping...")
        return

    # Add sidebar CSS to the <style> section
    style_end = content.find('</style>')
    if style_end != -1:
        content = content[:style_end] + SIDEBAR_CSS + '\n' + content[style_end:]
        print(f"  [OK] Added sidebar CSS")

    # Add sidebar HTML after <body> tag
    body_start = content.find('<body>')
    if body_start != -1:
        insert_pos = body_start + len('<body>')
        content = content[:insert_pos] + '\n' + SIDEBAR_HTML + content[insert_pos:]
        print(f"  [OK] Added sidebar HTML")

        # Now we need to close the content-wrapper div before </body>
        body_end = content.rfind('</body>')
        if body_end != -1:
            content = content[:body_end] + '\n    </div><!-- end content-wrapper -->\n' + content[body_end:]

    # Add sidebar JavaScript before </body>
    body_end = content.rfind('</body>')
    if body_end != -1:
        content = content[:body_end] + SIDEBAR_JS + '\n' + content[body_end:]
        print(f"  [OK] Added sidebar JavaScript")

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  [OK] {filepath} updated successfully!\n")

def main():
    """Add sidebar to all educational pages"""
    base_dir = r'C:\GitHub\me\nlp\kb'

    # List of files to update (exclude index page as it already has sidebar)
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
    print("Adding Navigation Sidebar to All Educational Pages")
    print("="*60)
    print()

    for filename in files:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            add_sidebar_to_file(filepath)
        else:
            print(f"  [WARNING] File not found: {filepath}")

    print("="*60)
    print("[SUCCESS] All pages updated with navigation sidebar!")
    print("="*60)
    print("\nFeatures added:")
    print("  - Left sidebar with navigation links")
    print("  - Home link to return to index")
    print("  - Active page highlighting")
    print("  - Mobile-responsive with toggle button")
    print("  - Consistent styling across all pages")

if __name__ == '__main__':
    main()
