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
    # Create new repository entry
    repo_entry = f'''\n  "{repo_name}" = {{
    description = "{description}"
    visibility  = "{visibility}"
    topics      = ["service"]
    teams = {{
      "{team}" = "push"
    }}
  }}'''

    # Find the closing brace and insert before it
    if content.rstrip().endswith('}'):
        content = content.rstrip()[:-1] + ',' + repo_entry + '\n}'
    else:
        content = content + repo_entry

elif operation == 'delete':
    # Remove repository entry
    pattern = f'\n\s*"{repo_name}"\s*=\s*\{{[^}}]*?teams\s*=\s*\{{[^}}]*?\}}\s*}},?'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    # Clean up any trailing comma before closing brace
    content = re.sub(r',(\s*\n\s*\})', r'\1', content)

with open(tfvars_path, 'w') as f:
    f.write(content)

print(f"Modified repositories/example.tfvars for {operation}: {repo_name}")
