#!/usr/bin/env python3
"""
Fix text visibility by ensuring all text has sufficient contrast
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

def fix_text_visibility_in_file(filepath):
    """Add explicit text colors to ensure visibility"""
    print(f"Fixing text visibility in {filepath}...")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the PAGE-SPECIFIC STYLES section
        specific_styles_pattern = r'(/\* ===== PAGE-SPECIFIC STYLES ===== \*/.*?)(</style>)'

        def add_text_colors(match):
            section = match.group(1)
            closing = match.group(2)

            # Check if text color rules already exist
            if 'color: #1f2937' in section and '.content-block p' in section:
                print(f"  [SKIP] {filepath} - text colors already fixed")
                return match.group(0)

            # Add explicit text color rules at the end of page-specific styles
            text_color_css = '''

        /* Ensure text visibility */
        .content-block,
        .content-block p,
        .content-block li,
        .content-block ul,
        .content-block ol,
        .content-block div {
            color: #1f2937 !important;
        }

        .corpus-box,
        .corpus-box .document {
            color: #1f2937 !important;
        }

        .section p,
        .section li,
        .section ul,
        .section ol {
            color: #1f2937 !important;
        }

        body, p, li, div, span {
            color: #1f2937 !important;
        }
        '''

            return section + text_color_css + '\n\n        ' + closing

        content = re.sub(specific_styles_pattern, add_text_colors, content, flags=re.DOTALL)

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  [OK] Fixed text visibility in {filepath}")
        return True

    except Exception as e:
        print(f"  [ERROR] {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("Fixing Text Visibility Across All Pages")
    print("=" * 60)
    print()

    success = 0
    for html_file in html_files:
        if fix_text_visibility_in_file(html_file):
            success += 1

    print()
    print("=" * 60)
    print(f"Complete: {success}/{len(html_files)} files fixed")
    print("=" * 60)

if __name__ == "__main__":
    main()
