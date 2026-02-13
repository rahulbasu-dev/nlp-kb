#!/usr/bin/env python3
"""
Reorder visualization sections in neural_networks_educational.html
"""

def reorder_visualizations():
    filepath = 'neural_networks_educational.html'

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Extract sections (line numbers are 1-indexed, convert to 0-indexed)
    sections = {
        'xor': lines[1987:2030],  # A. XOR (1988-2030)
        'forward_backward': lines[2032:2077],  # B. Complete Forward & Backward (2033-2077)
        'gradient': lines[2079:2117],  # C. Gradient Descent (2080-2117)
        'architecture': lines[2119:2132],  # D. Network Architecture (2120-2132)
        'forward_prop': lines[2134:2152],  # B. Forward Propagation (2135-2152)
        'activation': lines[2154:2169],  # C. Activation Function (2155-2169)
        'training_loss': lines[2171:2186],  # D. Training Loss (2172-2186)
    }

    # Update labels for new order
    # A. XOR - already correct
    sections['xor'][1] = sections['xor'][1].replace('>A. XOR', '>A. XOR')

    # B. Activation Function Explorer
    sections['activation'][1] = sections['activation'][1].replace('>C. Activation', '>B. Activation')

    # C. Network Architecture Visualizer
    sections['architecture'][1] = sections['architecture'][1].replace('>D. Network', '>C. Network')

    # D. Forward Propagation Simulator
    sections['forward_prop'][1] = sections['forward_prop'][1].replace('>B. Forward', '>D. Forward')

    # E. Gradient Descent on Loss Surface
    sections['gradient'][1] = sections['gradient'][1].replace('>C. Gradient', '>E. Gradient')

    # F. Training Loss Visualizer
    sections['training_loss'][1] = sections['training_loss'][1].replace('>D. Training', '>F. Training')

    # G. Complete Forward & Backward Pass
    sections['forward_backward'][1] = sections['forward_backward'][1].replace('>B. Complete', '>G. Complete')

    # Reconstruct file with new order
    new_order = [
        'xor',            # A
        'activation',      # B
        'architecture',    # C
        'forward_prop',    # D
        'gradient',        # E
        'training_loss',   # F
        'forward_backward' # G
    ]

    # Build new content
    new_content = []
    new_content.extend(lines[:1987])  # Everything before visualizations

    # Add reordered sections
    for key in new_order:
        new_content.extend(sections[key])
        new_content.append('\n')  # Add spacing between sections

    # Add everything after (starting from line 2187)
    new_content.extend(lines[2186:])

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_content)

    print("[OK] Visualization sections reordered successfully!")
    print("\nNew order:")
    print("A. XOR vs Linear Separability")
    print("B. Activation Function Explorer")
    print("C. Network Architecture Visualizer")
    print("D. Forward Propagation Simulator")
    print("E. Gradient Descent on Loss Surface")
    print("F. Training Loss Visualizer")
    print("G. Complete Forward & Backward Pass with Live Values")

if __name__ == "__main__":
    reorder_visualizations()
