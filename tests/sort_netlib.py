#!/usr/bin/env python3

import os
import subprocess
import shutil
from pathlib import Path

# Create directories if they don't exist
netlib_dir = Path("netlib")
large_dir = netlib_dir / "large"
small_dir = netlib_dir / "small"

for directory in [netlib_dir, large_dir, small_dir]:
    directory.mkdir(exist_ok=True)

# Process each file in netlib directory
for file_path in netlib_dir.glob("*"):
    if file_path.is_file() and not file_path.is_symlink():
        print(f"Testing {file_path.name}...")
        
        try:
            # Run the command with a timeout of 10 seconds
            with open(file_path, 'r') as f:
                result = subprocess.run(
                    ["vine", "run", "test_mps.vi"],
                    stdin=f,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
            
            # If we get here, the command completed within 10 seconds
            target_dir = small_dir
            print(f"✓ {file_path.name} completed in time")
            
        except subprocess.TimeoutExpired:
            # Command took longer than 10 seconds
            target_dir = large_dir
            print(f"⚠ {file_path.name} took too long")
            
        except Exception as e:
            print(f"✗ Error processing {file_path.name}: {str(e)}")
            continue
        
        # Move the file to the appropriate directory
        try:
            shutil.move(str(file_path), str(target_dir / file_path.name))
        except Exception as e:
            print(f"Error moving {file_path.name}: {str(e)}")

print("\nSorting complete!")
