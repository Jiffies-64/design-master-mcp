import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))

# Create necessary directories
dirs_to_create = [
    'templates',
    'prompts',
    'models',
    'storage',
    'mcp_tools'
]

for dir_name in dirs_to_create:
    dir_path = project_root / dir_name
    if not dir_path.exists():
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {dir_path}")

print("Project structure initialized successfully!")