#!/usr/bin/env python3
"""
Comprehensive color fix: White text on blue/dark backgrounds, dark text on light backgrounds
"""

import re

html_files = [
    'neural_networks_educational.html',
    'methods_comparison.html',
    'tfidf_educational.html',
    'word2vec_educational.html',
    'sgns_educational.html',
    'cbow_educational.html',
    'glove_educational.html',
    'nlp_guide_index.html',
]

def fix_colors_in_file(filepath):
    """Fix all color issues in a file"""
    print(f"Fixing colors in {filepath}...")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix nav styling - white text on blue gradient
        content = re.sub(
            r'(nav\s*\{[^}]*?)color:\s*var\(--text-primary\)',
            r'\1color: white',
            content
        )
        content = re.sub(
            r'(nav\s+\.logo\s*\{[^}]*?)color:\s*var\(--text-primary\)',
            r'\1color: white',
            content
        )
        content = re.sub(
            r'(nav\s+a\s*\{[^}]*?)color:\s*var\(--text-primary\)',
            r'\1color: white',
            content
        )

        # Fix header styling - white text on blue gradient
        content = re.sub(
            r'(header\s*\{[^}]*?)color:\s*var\(--text-primary\)',
            r'\1color: white',
            content
        )

        # Add explicit white color to header h1 and p if not present
        if 'header h1 {' in content and 'header h1' in content:
            content = re.sub(
                r'(header\s+h1\s*\{[^}]*?)(\})',
                lambda m: m.group(1) + '\n            color: white;\n        }' if 'color:' not in m.group(1) else m.group(0),
                content
            )
        if 'header p {' in content:
            content = re.sub(
                r'(header\s+p\s*\{[^}]*?)(\})',
                lambda m: m.group(1) + '\n            color: white;\n        }' if 'color:' not in m.group(1) else m.group(0),
                content
            )

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  [OK] Fixed colors in {filepath}")
        return True

    except Exception as e:
        print(f"  [ERROR] {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("Comprehensive Color Fix")
    print("=" * 60)
    print()

    success = 0
    for html_file in html_files:
        if fix_colors_in_file(html_file):
            success += 1

    print()
    print("=" * 60)
    print(f"Complete: {success}/{len(html_files)} files fixed")
    print("=" * 60)

if __name__ == "__main__":
    main()
