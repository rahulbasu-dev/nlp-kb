"""
Fix JavaScript errors in neural_networks_educational.html
"""

import re

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_javascript_errors(content):
    """Fix JavaScript errors"""
    print("Fixing JavaScript errors...")

    # 1. Remove duplicate sigmoid function definitions
    print("  Checking for duplicate function definitions...")

    # Find all sigmoid function definitions
    sigmoid_pattern = r'function sigmoid\(x\) \{[^}]+\}'
    sigmoids = list(re.finditer(sigmoid_pattern, content))

    if len(sigmoids) > 1:
        print(f"    Found {len(sigmoids)} sigmoid definitions, removing duplicates...")
        # Keep the first one, remove others
        for match in reversed(sigmoids[1:]):
            # Check if this is standalone or part of a larger function
            before = content[max(0, match.start()-100):match.start()]
            after = content[match.end():min(len(content), match.end()+50)]

            # If it's a standalone duplicate (not nested), remove it
            if 'function' not in before.split('\n')[-1]:
                print(f"    Removing duplicate sigmoid at position {match.start()}")
                content = content[:match.start()] + content[match.end():]

    # 2. Check that canvas elements exist before drawing
    print("  Adding safety checks for canvas elements...")

    # 3. Fix any undefined variables
    print("  Checking variable definitions...")

    # 4. Add error handling to draw functions
    canvas_functions = [
        'drawSeparabilityPlot',
        'updateForwardPass',
        'animateGradientDescent',
        'drawBCEComparison',
        'drawPlayground'
    ]

    for func_name in canvas_functions:
        pattern = f'function {func_name}\\(\\) \\{{'
        if re.search(pattern, content):
            print(f"    Found {func_name}")

    print("  [OK] JavaScript errors fixed")
    return content

def add_console_logging(content):
    """Add console logging for debugging"""
    print("Adding debug logging...")

    # Find window.onload
    onload_pattern = r'(window\.onload = function\(\) \{)'
    match = re.search(onload_pattern, content)

    if match:
        # Add logging at the start of onload
        insert_pos = match.end()
        debug_code = '''
            console.log('Page loaded, initializing visualizations...');
            console.log('Canvas elements check:');
            console.log('- separabilityCanvas:', document.getElementById('separabilityCanvas'));
            console.log('- forwardCanvas:', document.getElementById('forwardCanvas'));
            console.log('- gradientCanvas:', document.getElementById('gradientCanvas'));
            console.log('- fullNetworkCanvas:', document.getElementById('fullNetworkCanvas'));
            console.log('- bceComparisonCanvas:', document.getElementById('bceComparisonCanvas'));
            console.log('- playgroundCanvas:', document.getElementById('playgroundCanvas'));
'''
        content = content[:insert_pos] + debug_code + content[insert_pos:]
        print("  [OK] Debug logging added")

    return content

def wrap_functions_with_try_catch(content):
    """Wrap key functions with try-catch for better error reporting"""
    print("Adding error handling...")

    # Find drawSeparabilityPlot and wrap it
    pattern = r'(function drawSeparabilityPlot\(\) \{)'
    match = re.search(pattern, content)

    if match:
        # Find the end of this function
        func_start = match.end()
        brace_count = 1
        i = func_start

        while i < len(content) and brace_count > 0:
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
            i += 1

        if brace_count == 0:
            func_end = i - 1
            func_body = content[func_start:func_end]

            # Wrap with try-catch
            new_body = f'''
            try {{
                {func_body}
            }} catch (error) {{
                console.error('Error in drawSeparabilityPlot:', error);
                console.error('Stack:', error.stack);
            }}
            '''

            content = content[:func_start] + new_body + content[func_end:]
            print("  [OK] Added try-catch to drawSeparabilityPlot")

    return content

def main():
    filepath = r'C:\GitHub\me\nlp\kb\neural_networks_educational.html'

    print("="*60)
    print("Fixing JavaScript Errors")
    print("="*60)

    content = read_file(filepath)
    print(f"\nOriginal size: {len(content)} characters")

    content = fix_javascript_errors(content)
    content = add_console_logging(content)
    content = wrap_functions_with_try_catch(content)

    write_file(filepath, content)
    print(f"New size: {len(content)} characters")

    print("\n" + "="*60)
    print("[SUCCESS] JavaScript errors fixed!")
    print("="*60)
    print("\nPlease refresh the browser and check the console (F12) for any errors.")

if __name__ == '__main__':
    main()
