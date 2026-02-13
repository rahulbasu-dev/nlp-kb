#!/usr/bin/env python3
"""
Reorder sections: Mathematics should come after Visualization and before Simple Examples
New order: Intuition → Visualization → Mathematics → Simple Examples → Flowchart → Python → Variants → References
"""

import re

html_files = [
    'neural_networks_educational.html',
    'tfidf_educational.html',
    'word2vec_educational.html',
    'sgns_educational.html',
    'cbow_educational.html',
    'glove_educational.html',
]

def reorder_sections_in_file(filepath):
    """Reorder sections in a single HTML file"""
    print(f"Reordering sections in {filepath}...")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all major sections with their IDs and numbers
        # Pattern: <section id="..." class="section"> ... </section>
        section_pattern = r'(<section id="([^"]+)"[^>]*>.*?</section>)'

        # Extract all sections
        sections = {}
        for match in re.finditer(section_pattern, content, re.DOTALL):
            section_html = match.group(1)
            section_id = match.group(2)
            sections[section_id] = section_html

        # Define new order based on section IDs
        section_order = [
            'intuition',
            'visualization',
            'mathematics',      # MOVED HERE (was after simple-examples)
            'simple-examples',  # Moved after mathematics
            'flowchart',
            'python',
            'variants',
            'references'
        ]

        # Check which sections exist in this file
        existing_order = [sid for sid in section_order if sid in sections]

        if 'mathematics' not in sections or 'simple-examples' not in sections:
            print(f"  [SKIP] {filepath} - doesn't have both mathematics and simple-examples sections")
            return False

        # Find the mathematics section position
        math_match = re.search(r'<section id="mathematics"[^>]*>.*?</section>', content, re.DOTALL)
        simple_match = re.search(r'<section id="simple-examples"[^>]*>.*?</section>', content, re.DOTALL)

        if not math_match or not simple_match:
            print(f"  [SKIP] {filepath} - couldn't find sections")
            return False

        # Check if mathematics is already before simple-examples
        if math_match.start() < simple_match.start():
            print(f"  [OK] {filepath} - already in correct order")
            return True

        # Remove both sections from content
        content_without = content[:math_match.start()] + content[math_match.end():]

        # Find simple-examples in the modified content
        simple_match_new = re.search(r'<section id="simple-examples"[^>]*>.*?</section>', content_without, re.DOTALL)

        if not simple_match_new:
            print(f"  [ERROR] {filepath} - couldn't relocate simple-examples")
            return False

        # Insert mathematics before simple-examples
        new_content = (
            content_without[:simple_match_new.start()] +
            math_match.group(0) + '\n\n            ' +
            content_without[simple_match_new.start():]
        )

        # Update section numbers in headers
        # Find all <h2> tags with section numbers and update them
        def update_section_numbers(text):
            # This is a simplified approach - just renumber sequentially
            section_num = 1

            def replace_h2(match):
                nonlocal section_num
                old_num = match.group(1)
                new_h2 = match.group(0).replace(f"{old_num}.", f"{section_num}.")
                section_num += 1
                return new_h2

            # Pattern: <h2>1. Section Name</h2> or <h2>2. Method 1: Name</h2>
            return re.sub(r'<h2>(\d+)\.\s+', replace_h2, text)

        new_content = update_section_numbers(new_content)

        # Update navigation links order
        nav_pattern = r'(<div class="nav-links">.*?</div>)'
        nav_match = re.search(nav_pattern, new_content, re.DOTALL)

        if nav_match:
            old_nav = nav_match.group(0)
            # Reorder navigation links
            new_nav = old_nav

            # Find and reorder mathematics link to come before simple-examples
            math_link = re.search(r'<a href="#mathematics"[^>]*>.*?</a>', old_nav, re.DOTALL)
            examples_link = re.search(r'<a href="#simple-examples"[^>]*>.*?</a>', old_nav, re.DOTALL)

            if math_link and examples_link and math_link.start() > examples_link.start():
                # Remove math link
                new_nav = old_nav[:math_link.start()] + old_nav[math_link.end():]
                # Find examples link in new nav
                examples_link_new = re.search(r'<a href="#simple-examples"[^>]*>.*?</a>', new_nav, re.DOTALL)
                if examples_link_new:
                    # Insert math link before examples link
                    new_nav = (
                        new_nav[:examples_link_new.start()] +
                        math_link.group(0) + '\n                ' +
                        new_nav[examples_link_new.start():]
                    )
                    new_content = new_content.replace(old_nav, new_nav)

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  [OK] {filepath} - sections reordered successfully")
        return True

    except Exception as e:
        print(f"  [ERROR] {filepath}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 70)
    print("Reordering Sections: Mathematics -> Before Simple Examples")
    print("=" * 70)
    print()

    success = 0
    for html_file in html_files:
        if reorder_sections_in_file(html_file):
            success += 1
        print()

    print("=" * 70)
    print(f"Complete: {success}/{len(html_files)} files updated")
    print("=" * 70)

if __name__ == "__main__":
    main()
