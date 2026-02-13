"""
Fix sidebar styling issues - ensure styles have proper specificity and aren't overridden
"""

import re

def fix_sidebar_in_file(filepath):
    """Fix sidebar styling in a file"""
    print(f"Fixing {filepath}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if this file has our sidebar
    if 'class="sidebar"' not in content or 'Navigation Sidebar Styles' not in content:
        print(f"  No sidebar found, skipping...\n")
        return

    # Find and update the sidebar CSS to have more specific selectors and !important flags
    updated_sidebar_css = '''
        /* Navigation Sidebar Styles - High Priority */
        body {
            margin: 0 !important;
            padding: 0 !important;
        }

        .sidebar {
            position: fixed !important;
            left: 0 !important;
            top: 0 !important;
            width: 280px !important;
            height: 100vh !important;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
            padding: 2rem 0 !important;
            overflow-y: auto !important;
            z-index: 10000 !important;
            box-shadow: 4px 0 10px rgba(0,0,0,0.1) !important;
        }

        .sidebar * {
            color: white !important;
        }

        .sidebar-header {
            padding: 0 1.5rem 1.5rem !important;
            border-bottom: 1px solid rgba(255,255,255,0.2) !important;
            margin-bottom: 1.5rem !important;
        }

        .sidebar-header h2 {
            color: white !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            margin-bottom: 0.5rem !important;
        }

        .sidebar-header p {
            color: rgba(255,255,255,1) !important;
            font-size: 0.85rem !important;
        }

        .sidebar-nav {
            padding: 0 1rem !important;
        }

        .sidebar-section {
            margin-bottom: 2rem !important;
        }

        .sidebar-section-title {
            color: rgba(255,255,255,0.95) !important;
            font-size: 0.75rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
            font-weight: 600 !important;
            padding: 0 0.5rem !important;
            margin-bottom: 0.75rem !important;
        }

        .sidebar-link {
            display: flex !important;
            align-items: center !important;
            gap: 0.75rem !important;
            padding: 0.75rem 0.5rem !important;
            color: rgba(255,255,255,1) !important;
            text-decoration: none !important;
            border-radius: 0.5rem !important;
            transition: all 0.2s ease !important;
            font-size: 0.95rem !important;
        }

        .sidebar-link:hover {
            background: rgba(255,255,255,0.15) !important;
            color: white !important;
            transform: translateX(5px) !important;
        }

        .sidebar-link.active {
            background: rgba(255,255,255,0.2) !important;
            color: white !important;
            font-weight: 600 !important;
        }

        .sidebar-link .icon {
            font-size: 1.25rem !important;
            width: 24px !important;
            text-align: center !important;
            color: white !important;
        }

        .sidebar-link span {
            color: white !important;
        }

        .content-wrapper {
            margin-left: 280px !important;
            min-height: 100vh !important;
        }

        /* Sidebar Toggle Button for Mobile */
        .sidebar-toggle {
            display: none !important;
            position: fixed !important;
            bottom: 2rem !important;
            right: 2rem !important;
            width: 60px !important;
            height: 60px !important;
            background: #2563eb !important;
            color: white !important;
            border: none !important;
            border-radius: 50% !important;
            font-size: 1.5rem !important;
            cursor: pointer !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
            z-index: 9999 !important;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .sidebar {
                transform: translateX(-100%) !important;
                transition: transform 0.3s ease !important;
            }

            .sidebar.open {
                transform: translateX(0) !important;
            }

            .content-wrapper {
                margin-left: 0 !important;
            }

            .sidebar-toggle {
                display: block !important;
            }
        }

        /* Ensure sidebar headers stay white */
        .sidebar h1, .sidebar h2, .sidebar h3, .sidebar h4, .sidebar h5, .sidebar h6 {
            color: white !important;
        }
'''

    # Remove old sidebar CSS
    pattern = r'/\* Navigation Sidebar Styles.*?\*/\s*.*?(?=/\*|</style>)'
    content = re.sub(pattern, '', content, flags=re.DOTALL)

    # Add new CSS right before </style>
    style_end = content.rfind('</style>')
    if style_end != -1:
        content = content[:style_end] + updated_sidebar_css + '\n' + content[style_end:]
        print(f"  [OK] Updated sidebar CSS with !important flags\n")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

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
    print("Fixing Sidebar Styling")
    print("="*60)
    print()

    for filename in files:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            fix_sidebar_in_file(filepath)

    print("="*60)
    print("[SUCCESS] All sidebars fixed!")
    print("="*60)

if __name__ == '__main__':
    main()
