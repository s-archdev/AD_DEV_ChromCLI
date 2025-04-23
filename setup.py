#!/usr/bin/env python3
"""
Setup script for AD_DEV_ChronCLI
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def main():
    """Main installation function"""
    print("╔════════════════════════════════════════════════════╗")
    print("║     AD_DEV_ChronCLI Installer                      ║")
    print("╚════════════════════════════════════════════════════╝")
    
    # Check if Python 3.6+ is installed
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        print("Error: AD_DEV_ChronCLI requires Python 3.6 or higher")
        sys.exit(1)
    
    # Create installation directory
    install_dir = os.path.expanduser("~/ad_dev_chroncli")
    config_dir = os.path.expanduser("~/.ad_dev_chroncli")
    
    print(f"Installing AD_DEV_ChronCLI to {install_dir}")
    
    # Create directories
    os.makedirs(install_dir, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)
    
    # Copy the main script
    source_script = "chroncli.py"
    dest_script = os.path.join(install_dir, "chroncli.py")
    
    if not os.path.exists(source_script):
        print(f"Error: Could not find {source_script}")
        sys.exit(1)
    
    shutil.copy2(source_script, dest_script)
    os.chmod(dest_script, 0o755)  # Make executable
    
    # Create symlink
    bin_dir = os.path.expanduser("~/bin")
    os.makedirs(bin_dir, exist_ok=True)
    
    symlink_path = os.path.join(bin_dir, "chroncli")
    
    # Remove existing symlink if it exists
    if os.path.exists(symlink_path):
        os.remove(symlink_path)
    
    os.symlink(dest_script, symlink_path)
    
    # Update PATH if needed
    shell_profile = None
    if 'SHELL' in os.environ:
        if 'bash' in os.environ['SHELL']:
            shell_profile = os.path.expanduser("~/.bash_profile")
        elif 'zsh' in os.environ['SHELL']:
            shell_profile = os.path.expanduser("~/.zshrc")
    
    if shell_profile:
        with open(shell_profile, 'a+') as f:
            f.seek(0)
            content = f.read()
            if f'export PATH="$PATH:{bin_dir}"' not in content:
                f.write(f'\n# Added by AD_DEV_ChronCLI installer\nexport PATH="$PATH:{bin_dir}"\n')
                print(f"Added {bin_dir} to PATH in {shell_profile}")
                print("Please restart your terminal or run:")
                print(f"    source {shell_profile}")
    
    print("\nInstallation complete!")
    print("\nTo start AD_DEV_ChronCLI, run:")
    print("    chroncli")
    print("\nOr if you haven't updated your PATH:")
    print(f"    {dest_script}")


if __name__ == "__main__":
    main()
