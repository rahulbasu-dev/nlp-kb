"""
Fix neural_networks_educational.html and methods_comparison.html
Remove all sidebar code and ensure they work standalone
"""

import re

def fix_standalone_page(filepath):
    """Remove sidebar code and fix styling"""
    print(f"Fixing {filepath}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove any sidebar HTML
    content = re.sub(r'<aside[^>]*class="[^"]*sidebar[^"]*"[^>]*>.*?</aside>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<div[^>]*class="[^"]*sidebar[^"]*"[^>]*>.*?</div>\s*(?=<div|<nav|<header|<main|<section|<script)', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<nav[^>]*class="[^"]*sidebar[^"]*"[^>]*>.*?</nav>', '', content, flags=re.DOTALL | re.IGNORECASE)

    # Remove sidebar toggle button
    content = re.sub(r'<button[^>]*sidebar-toggle[^>]*>.*?</button>', '', content, flags=re.DOTALL | re.IGNORECASE)

    # Remove content-wrapper divs
    content = re.sub(r'<div[^>]*class="[^"]*content-wrapper[^"]*"[^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'</div>\s*<!--.*?end content-wrapper.*?-->', '', content, flags=re.IGNORECASE)

    # Remove sidebar CSS (all variations)
    content = re.sub(r'/\*[^*]*Navigation Sidebar[^*]*\*/.*?(?=/\*|\n\s*</style>)', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'\.nlp-sidebar[^{]*\{[^}]*\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\.sidebar[^{]*\{[^}]*\}', '', content, flags=re.DOTALL)

    # Remove sidebar JavaScript
    content = re.sub(r'<script>.*?toggleSidebar.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<script>.*?toggleNLPSidebar.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)

    # Fix body margin that was added for sidebar
    content = re.sub(r'body\s*\{\s*margin-left:\s*280px;', 'body {', content, flags=re.IGNORECASE)
    content = re.sub(r'body\s*\{\s*margin:\s*0\s*!important;\s*padding:\s*0\s*!important;', 'body {', content, flags=re.IGNORECASE)

    # Clean up empty style blocks
    content = re.sub(r'<style>\s*\n\s*body\s*\{\s*margin:\s*0\s*!important;\s*padding:\s*0\s*!important;\s*\}\s*\n\s*</style>', '', content, flags=re.DOTALL)

    # Ensure we have proper body styling
    if '<style>' in content and 'body {' not in content:
        # Add basic body styling after <style>
        style_start = content.find('<style>') + len('<style>')
        body_css = '''
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.7;
            color: #1f2937;
            background-color: #f8fafc;
            margin: 0;
            padding: 0;
        }
        '''
        content = content[:style_start] + body_css + content[style_start:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  [OK] Cleaned up {filepath}\n")

def main():
    import os
    base_dir = r'C:\GitHub\me\nlp\kb'

    files = [
        'neural_networks_educational.html',
        'methods_comparison.html'
    ]

    print("="*60)
    print("Fixing Standalone Pages")
    print("="*60)
    print()

    for filename in files:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            fix_standalone_page(filepath)
        else:
            print(f"[WARNING] File not found: {filepath}")

    print("="*60)
    print("[SUCCESS] Pages fixed as standalone!")
    print("="*60)
    print("\nThese pages now work independently without sidebars.")
    print("Use nlp_guide_index.html for navigation between pages.")

if __name__ == '__main__':
    main()
