#!/usr/bin/env python3
"""Fix app.py by removing duplicate function definitions and orphaned content."""

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line numbers of key markers
api_endpoints_lines = []
for i, line in enumerate(lines):
    if line.strip() == '# API ENDPOINTS' and i > 0 and lines[i-1].strip().startswith('# ==='):
        api_endpoints_lines.append(i)

print(f"Found {len(api_endpoints_lines)} '# API ENDPOINTS' headers at lines: {api_endpoints_lines}")

if len(api_endpoints_lines) >= 2:
    # Keep only the LAST occurrence (the clean one) and delete everything from first to second-1
    keep_from = api_endpoints_lines[-1] - 1  # Include the === line before it
    delete_from = api_endpoints_lines[0] - 1  # Include the === line before it
    delete_to = keep_from
    
    print(f"Deleting lines {delete_from} to {delete_to-1} (total: {delete_to - delete_from} lines)")
    
    # Create new content
    new_lines = lines[:delete_from] + lines[keep_from:]
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✓ Fixed! Reduced from {len(lines)} to {len(new_lines)} lines")
else:
    print("ERROR: Expected 2+ '# API ENDPOINTS' sections but found", len(api_endpoints_lines))
