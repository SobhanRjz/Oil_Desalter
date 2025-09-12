import subprocess
import sys
import os
from pathlib import Path

def build_exe():
    """Build the executable using PyInstaller."""
    project_root = Path(__file__).parent

    print("Building executable...")

    # Run PyInstaller with the spec file
    cmd = [
        sys.executable, "-m", "pyinstaller",
        "--clean",
        "--noconfirm",
        "desalter.spec"
    ]

    try:
        result = subprocess.run(cmd, cwd=str(project_root), check=True)
        print("Build completed successfully!")
        print(f"Executable created at: {project_root / 'dist' / 'desalter.exe'}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error code {e.returncode}")
        return False

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)
