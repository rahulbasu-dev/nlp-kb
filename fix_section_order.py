#!/usr/bin/env python3
"""
Fix physical order of visualization sections to match labels A-G
"""

def fix_section_order():
    filepath = 'neural_networks_educational.html'

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define section markers with their labels
    # Format: (label, start_marker, approximate_line)
    sections_info = [
        ('A', 'A. XOR vs Linear Separability', 1989),
        ('B', 'B. Activation Function Explorer', 2162),
        ('C', 'C. Network Architecture Visualizer', 2178),
        ('D', 'D. Forward Propagation Simulator', 2192),
        ('E', 'E. Gradient Descent on Loss Surface', 2109),
        ('F', 'F. Training Loss Visualizer', 2049),
        ('G', 'G. Complete Forward & Backward Pass with Live Values', 2064),
    ]

    # Find the start of the visualization section
    viz_start = content.find('<h2>2. Visualizations</h2>')
    if viz_start == -1:
        print("[ERROR] Could not find Visualizations section")
        return False

    # Find where visualization sections end (start of next major section)
    math_section_start = content.find('<h2>3. Mathematical Foundations</h2>', viz_start)
    if math_section_start == -1:
        print("[ERROR] Could not find Mathematical Foundations section")
        return False

    # Extract the content before, during, and after visualization sections
    before_viz = content[:viz_start]
    viz_header = '<h2>2. Visualizations</h2>\n\n'
    after_sections = content[math_section_start:]

    # Extract each section by finding the div.interactive-section blocks
    import re

    # Find all interactive-section divs with their content
    pattern = r'(<div class="interactive-section">.*?</div>\n\n)'
    viz_content = content[viz_start:math_section_start]

    # More robust: split by the comment markers and section divs
    sections = {}

    # Manual extraction based on known structure
    # Each section is: <!-- comment --> <div class="interactive-section">...</div>

    # Find A. XOR section
    a_start = viz_content.find('<!-- XOR vs Linear Separability -->')
    a_end = viz_content.find('<!-- ', a_start + 10)
    if a_end == -1:  # Last section case
        a_end = len(viz_content)
    sections['A'] = viz_content[a_start:a_end]

    # Find B. Activation (look for the comment or the heading)
    b_marker = viz_content.find('B. Activation Function Explorer')
    if b_marker > -1:
        # Find the start of this section's div
        b_start = viz_content.rfind('<div class="interactive-section">', 0, b_marker)
        # Find the end
        b_end_search = viz_content.find('</div>\n\n', b_marker)
        if b_end_search > -1:
            b_end = b_end_search + 8  # Include </div>\n\n
        else:
            b_end = viz_content.find('<div class="interactive-section">', b_marker + 10)
        sections['B'] = viz_content[b_start:b_end]

    # Find C. Network Architecture
    c_marker = viz_content.find('C. Network Architecture Visualizer')
    if c_marker > -1:
        c_start = viz_content.rfind('<div class="interactive-section">', 0, c_marker)
        c_end_search = viz_content.find('</div>\n\n', c_marker)
        if c_end_search > -1:
            c_end = c_end_search + 8
        else:
            c_end = viz_content.find('<div class="interactive-section">', c_marker + 10)
        sections['C'] = viz_content[c_start:c_end]

    # Find D. Forward Propagation
    d_marker = viz_content.find('D. Forward Propagation Simulator')
    if d_marker > -1:
        d_start = viz_content.rfind('<div class="interactive-section">', 0, d_marker)
        d_end_search = viz_content.find('</div>\n\n', d_marker)
        if d_end_search > -1:
            d_end = d_end_search + 8
        else:
            d_end = len(viz_content)
        sections['D'] = viz_content[d_start:d_end]

    # Find E. Gradient Descent
    e_marker = viz_content.find('E. Gradient Descent on Loss Surface')
    if e_marker > -1:
        e_start = viz_content.rfind('<div class="interactive-section">', 0, e_marker)
        e_end_search = viz_content.find('</div>\n\n', e_marker)
        if e_end_search > -1:
            e_end = e_end_search + 8
        else:
            e_end = viz_content.find('<div class="interactive-section">', e_marker + 10)
        sections['E'] = viz_content[e_start:e_end]

    # Find F. Training Loss
    f_marker = viz_content.find('F. Training Loss Visualizer')
    if f_marker > -1:
        f_start = viz_content.rfind('<div class="interactive-section">', 0, f_marker)
        f_end_search = viz_content.find('</div>\n\n', f_marker)
        if f_end_search > -1:
            f_end = f_end_search + 8
        else:
            f_end = viz_content.find('<div class="interactive-section">', f_marker + 10)
        sections['F'] = viz_content[f_start:f_end]

    # Find G. Complete Forward & Backward
    g_marker = viz_content.find('G. Complete Forward & Backward Pass')
    if g_marker > -1:
        g_start = viz_content.rfind('<div class="interactive-section">', 0, g_marker)
        g_end_search = viz_content.find('</div>\n\n', g_marker)
        if g_end_search > -1:
            g_end = g_end_search + 8
        else:
            g_end = viz_content.find('<div class="interactive-section">', g_marker + 10)
        sections['G'] = viz_content[g_start:g_end]

    # Verify we found all sections
    print("[INFO] Extracted sections:")
    for label in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        if label in sections:
            print(f"  {label}: {len(sections[label])} characters")
        else:
            print(f"  {label}: [ERROR] NOT FOUND")
            return False

    # Reconstruct in correct order
    new_viz_content = viz_header
    for label in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        new_viz_content += sections[label]
        if not sections[label].endswith('\n\n'):
            new_viz_content += '\n'

    # Reconstruct full file
    new_content = before_viz + new_viz_content + after_sections

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("\n[OK] Sections reordered successfully!")
    print("\nNew order:")
    print("A. XOR vs Linear Separability")
    print("B. Activation Function Explorer")
    print("C. Network Architecture Visualizer")
    print("D. Forward Propagation Simulator")
    print("E. Gradient Descent on Loss Surface")
    print("F. Training Loss Visualizer")
    print("G. Complete Forward & Backward Pass with Live Values")
    return True

if __name__ == "__main__":
    fix_section_order()
