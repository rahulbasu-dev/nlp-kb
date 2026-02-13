"""
Restore proper styling to neural_networks_educational.html
by using CSS from a working educational page
"""

def restore_styling():
    print("Restoring neural_networks_educational.html styling...")

    # Read working CSS from sgns_educational.html
    with open('sgns_educational.html', 'r', encoding='utf-8') as f:
        sgns_content = f.read()

    # Extract CSS from sgns file
    import re
    css_match = re.search(r'<style>(.*?)</style>', sgns_content, re.DOTALL)
    if not css_match:
        print("  [ERROR] Could not extract CSS from sgns_educational.html")
        return

    working_css = css_match.group(1)
    print(f"  [OK] Extracted {len(working_css)} characters of CSS")

    # Read current neural networks file
    with open('neural_networks_educational.html', 'r', encoding='utf-8') as f:
        nn_content = f.read()

    # Check if it has a style section
    if '<style>' not in nn_content:
        print("  [ERROR] No style tag found in neural_networks_educational.html")
        return

    # Replace the content between <style> and </style>
    nn_content = re.sub(
        r'<style>.*?</style>',
        f'<style>{working_css}</style>',
        nn_content,
        flags=re.DOTALL
    )

    # Write back
    with open('neural_networks_educational.html', 'w', encoding='utf-8') as f:
        f.write(nn_content)

    print("  [OK] Restored CSS to neural_networks_educational.html")
    print("\n[SUCCESS] File should now have proper styling!")

if __name__ == '__main__':
    import os
    os.chdir(r'C:\GitHub\me\nlp\kb')
    restore_styling()
