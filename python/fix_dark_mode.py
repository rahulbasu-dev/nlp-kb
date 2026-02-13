#!/usr/bin/env python3
"""
Fix dark mode by replacing hardcoded colors with CSS variables
"""

import re
import os

html_files = [
    'neural_networks_educational.html',
    'methods_comparison.html',
    'tfidf_educational.html',
    'word2vec_educational.html',
    'sgns_educational.html',
    'cbow_educational.html',
    'glove_educational.html',
]

# Patterns to replace hardcoded colors with CSS variables
replacements = [
    # Background colors
    (r'background:\s*white\s*;', 'background: var(--bg-elevated);'),
    (r'background:\s*#fff(?:fff)?\s*;', 'background: var(--bg-elevated);'),
    (r'background:\s*#f[0-9a-f]{5}\s*;', 'background: var(--bg-secondary);'),
    (r'background-color:\s*white\s*;', 'background-color: var(--bg-elevated);'),
    (r'background-color:\s*#fff(?:fff)?\s*;', 'background-color: var(--bg-elevated);'),

    # Text colors in page-specific sections
    (r'color:\s*#333\s*;', 'color: var(--text-primary);'),
    (r'color:\s*#666\s*;', 'color: var(--text-secondary);'),
    (r'color:\s*#1f2937\s*;', 'color: var(--text-primary);'),

    # Container backgrounds
    (r'\.container\s*\{[^}]*background:\s*white\s*;', lambda m: m.group(0).replace('background: white;', 'background: var(--bg-primary);')),
]

def fix_dark_mode_in_file(filepath):
    """Fix dark mode colors in a single file"""
    print(f"Fixing dark mode in {filepath}...")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the PAGE-SPECIFIC STYLES section
        specific_styles_pattern = r'(/\* ===== PAGE-SPECIFIC STYLES ===== \*/.*?)</style>'

        def fix_specific_styles(match):
            section = match.group(1)

            # Replace hardcoded colors with variables
            section = re.sub(r'\bbackground:\s*white\b', 'background: var(--bg-elevated)', section)
            section = re.sub(r'\bbackground:\s*#fff(?:fff)?\b', 'background: var(--bg-elevated)', section)
            section = re.sub(r'\bbackground-color:\s*white\b', 'background-color: var(--bg-elevated)', section)
            section = re.sub(r'\bbackground-color:\s*#fff(?:fff)?\b', 'background-color: var(--bg-elevated)', section)
            section = re.sub(r'\bcolor:\s*#333\b', 'color: var(--text-primary)', section)
            section = re.sub(r'\bcolor:\s*#666\b', 'color: var(--text-secondary)', section)
            section = re.sub(r'\bcolor:\s*white\b(?![^{]*gradient)', 'color: var(--text-primary)', section)

            return section + '</style>'

        content = re.sub(specific_styles_pattern, fix_specific_styles, content, flags=re.DOTALL)

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[OK] Fixed dark mode in {filepath}")
        return True

    except Exception as e:
        print(f"[ERROR] {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("Fixing Dark Mode Across All Pages")
    print("=" * 60)
    print()

    success = 0
    for html_file in html_files:
        if fix_dark_mode_in_file(html_file):
            success += 1

    print()
    print("=" * 60)
    print(f"Complete: {success}/{len(html_files)} files fixed")
    print("=" * 60)

if __name__ == "__main__":
    main()
