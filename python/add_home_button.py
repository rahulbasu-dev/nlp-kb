"""
Add home button to all educational pages that don't have it
"""
import re

# CSS for home button
HOME_BUTTON_CSS = """
        /* Home Button */
        .home-btn {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 56px;
            height: 56px;
            background: var(--primary-color);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            box-shadow: var(--shadow-lg);
            transition: all 0.3s ease;
            z-index: 999;
            text-decoration: none;
        }

        .home-btn:hover {
            transform: scale(1.1);
            background: var(--primary-dark);
        }
"""

# HTML for home button
HOME_BUTTON_HTML = """
    <!-- Home Button -->
    <a href="nlp_guide_index.html" class="home-btn" title="Back to Home">🏠</a>
"""

def add_home_button_to_file(filepath):
    """Add home button CSS and HTML to a file"""
    print(f"Processing {filepath}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has home button
    if 'home-btn' in content:
        print(f"  [SKIP] {filepath} already has home button")
        return False

    # Add CSS before closing </style> tag
    if '</style>' in content:
        content = content.replace('</style>', HOME_BUTTON_CSS + '    </style>')
        print(f"  [OK] Added home button CSS")
    else:
        print(f"  [WARNING] No </style> tag found")

    # Add HTML before closing </body> tag
    if '</body>' in content:
        content = content.replace('</body>', HOME_BUTTON_HTML + '</body>')
        print(f"  [OK] Added home button HTML")
    else:
        print(f"  [WARNING] No </body> tag found")

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  [SUCCESS] Updated {filepath}")
    return True

def main():
    import os
    os.chdir(r'C:\GitHub\me\nlp\kb')

    files_to_update = [
        'cbow_educational.html',
        'glove_educational.html',
        'sgns_educational.html',
        'tfidf_educational.html',
        'word2vec_educational.html'
    ]

    print("=" * 60)
    print("Adding Home Button to Educational Pages")
    print("=" * 60)
    print()

    updated_count = 0
    for filename in files_to_update:
        if os.path.exists(filename):
            if add_home_button_to_file(filename):
                updated_count += 1
            print()
        else:
            print(f"[WARNING] File not found: {filename}\n")

    print("=" * 60)
    print(f"[SUCCESS] Updated {updated_count} files")
    print("=" * 60)
    print("\nHome button (🏠) will now appear on all educational pages!")
    print("Test by opening any educational HTML file in your browser.")

if __name__ == '__main__':
    main()
