#!/usr/bin/env python3
"""
UI/UX Update Script for NLP Knowledge Base
Adds dark mode support, toggleable solutions, and consistent design system
"""

import re
import os
from pathlib import Path

# Read the shared CSS
with open('shared-styles.css', 'r', encoding='utf-8') as f:
    shared_css = f.read()

# Read the shared JavaScript
with open('shared-scripts.js', 'r', encoding='utf-8') as f:
    shared_js = f.read()

# List of HTML files to update
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

def inject_theme_toggle_html(content):
    """Inject theme toggle button HTML if not present"""
    if 'class="theme-toggle"' in content:
        return content

    # Find </body> tag and inject before it
    body_end = content.rfind('</body>')
    if body_end != -1:
        toggle_html = '''
    <!-- Theme Toggle Button -->
    <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode">🌙</button>
'''
        content = content[:body_end] + toggle_html + content[body_end:]

    return content

def inject_shared_css(content):
    """Inject or replace page-specific CSS with shared design system"""
    # Find the <style> tag
    style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)

    if style_match:
        # Keep page-specific styles but add shared CSS first
        new_style = f"<style>\n/* ===== SHARED DESIGN SYSTEM ===== */\n{shared_css}\n\n/* ===== PAGE-SPECIFIC STYLES ===== */\n{style_match.group(1)}\n</style>"
        content = content[:style_match.start()] + new_style + content[style_match.end():]

    return content

def inject_shared_js(content):
    """Inject shared JavaScript before </body>"""
    if 'initThemeToggle' in content:
        return content  # Already injected

    body_end = content.rfind('</body>')
    if body_end != -1:
        js_block = f'''
    <script>
    /* ===== SHARED JAVASCRIPT ===== */
    {shared_js}
    </script>
'''
        content = content[:body_end] + js_block + content[body_end:]

    return content

def make_solutions_toggleable(content):
    """Find all solution boxes and ensure they have toggle buttons"""
    # Pattern: find divs with class="solution" or id containing "solution"
    # Add data attributes for toggleability

    # Find solution divs
    solution_pattern = r'(<div[^>]*(?:class="[^"]*solution[^"]*"|id="[^"]*solution[^"]*")[^>]*>)'

    def add_toggle_class(match):
        div_tag = match.group(1)
        if 'data-toggle="solution"' not in div_tag:
            # Add before the closing >
            div_tag = div_tag.rstrip('>') + ' data-toggle="solution">'
        return div_tag

    content = re.sub(solution_pattern, add_toggle_class, content)

    # Find "Show Solution" or similar buttons and ensure they have proper onclick
    button_pattern = r'<button[^>]*class="[^"]*solution-toggle[^"]*"[^>]*onclick="toggleSolution\([\'"]([^\'"]+)[\'"]\)"[^>]*>(.*?)</button>'

    def fix_button(match):
        solution_id = match.group(1)
        button_text = match.group(2)
        return f'<button class="solution-toggle" data-solution-id="{solution_id}">{button_text}</button>'

    content = re.sub(button_pattern, fix_button, content)

    return content

def process_file(filepath):
    """Process a single HTML file"""
    print(f"Processing {filepath}...")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Apply transformations
        content = inject_shared_css(content)
        content = inject_shared_js(content)
        content = inject_theme_toggle_html(content)
        content = make_solutions_toggleable(content)

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[OK] Successfully updated {filepath}")
        return True

    except Exception as e:
        print(f"[ERROR] Error processing {filepath}: {e}")
        return False

def main():
    """Main execution"""
    print("=" * 60)
    print("NLP Knowledge Base UI/UX Update Script")
    print("=" * 60)
    print()

    success_count = 0
    total_count = len(html_files)

    for html_file in html_files:
        if process_file(html_file):
            success_count += 1
        print()

    print("=" * 60)
    print(f"Update Complete: {success_count}/{total_count} files updated successfully")
    print("=" * 60)

if __name__ == "__main__":
    main()
