#!/usr/bin/env python3
import os
import re

operation = os.environ.get('OPERATION')
repo_name = os.environ.get('REPO_NAME')
visibility = os.environ.get('VISIBILITY', 'private')
team = os.environ.get('TEAM', 'platform-team')
description = os.environ.get('DESCRIPTION', f'Repository: {repo_name}')

tfvars_path = 'repositories/example.tfvars'

with open(tfvars_path, 'r') as f:
    content = f.read()

if operation == 'create':
    # Create new repository entry with proper indentation
    repo_block = f'''  "{repo_name}" = {{
    description = "{description}"
    visibility  = "{visibility}"
    topics      = ["service"]
  }}'''

    # Check if repositories block is empty
    empty_pattern = r'repositories\s*=\s*\{\s*\n\}'
    if re.search(empty_pattern, content):
        # Replace empty block with new repo
        content = re.sub(empty_pattern, f'repositories = {{\n{repo_block}\n}}', content, flags=re.DOTALL)
    else:
        # Find last entry's closing brace and add new entry
        pattern = r'(  "[^"]+"\s*=\s*\{[^}]*\}\s*)(\n\})'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            last_entry = match.group(1)
            closing = match.group(2)
            # Add comma to last entry if it doesn't have one
            if not last_entry.rstrip().endswith(','):
                last_entry_with_comma = last_entry + ','
            else:
                last_entry_with_comma = last_entry
            # Replace with new entry added
            replacement = last_entry_with_comma + '\n' + repo_block + closing
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)

elif operation == 'delete':
    # Remove repository entry
    pattern = f'  "{repo_name}"\s*=\s*\{{[^}}]*?\}},?'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    # Clean up double commas or trailing commas before closing brace
    content = re.sub(r',(\s*\n\})', r'\1', content)

with open(tfvars_path, 'w') as f:
    f.write(content)

print(f"Modified repositories/example.tfvars for {operation}: {repo_name}")
