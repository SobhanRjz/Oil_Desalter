"""Nuitka build script for Desalter application."""
import subprocess
import sys
import os
from pathlib import Path

def build_nuitka_standalone():
    """Build with Nuitka standalone mode with antivirus-friendly settings."""
    project_root = Path(__file__).parent
    
    # Check if icon exists, if not, skip icon parameter
    icon_path = project_root / "frontend/assets/Logo.jpg"
    icon_args = []
    if icon_path.exists():
        icon_args = ["--windows-icon-from-ico=frontend/assets/Logo.jpg"]
        print(f"📱 Using icon: {icon_path}")
    else:
        print("⚠️ Icon file not found, building without icon")
    
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--output-dir=dist",
        "--output-filename=desalter.exe",
        "--include-data-dir=frontend=frontend",
        "--include-data-dir=backend=backend",
        # Antivirus-friendly flags
        "--windows-company-name=Desalter Solutions",
        "--windows-product-name=Desalter Oil Processing Tool",
        "--windows-file-version=1.0.0.0",
        "--windows-product-version=1.0.0",
        "--windows-file-description=Oil and Gas Desalter Optimization Tool",
        "--windows-icon-from-ico=frontend/assets/Logo.jpg",

        "--no-pyi-file",
        "--assume-yes-for-downloads",
        "--show-progress",
        "--show-scons",
        "launcher.py"
    ] + icon_args

    print("🚀 Building with Nuitka (Standalone + Onefile)...")
    print("Command:", " ".join(cmd))
    print("=" * 60)

    try:
        result = subprocess.run(cmd, cwd=str(project_root))
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\n❌ Build interrupted by user")
        return False

def build_nuitka_minimal():
    """Build with minimal Nuitka options."""
    project_root = Path(__file__).parent
    cmd = [
        sys.executable, "-m", "nuitka",
        "--onefile",
        "--output-dir=dist",
        "--output-filename=desalter.exe",
        "launcher.py"
    ]

    print("🔧 Building with Nuitka (Minimal)...")
    print("Command:", " ".join(cmd))
    print("=" * 60)

    try:
        result = subprocess.run(cmd, cwd=str(project_root))
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\n❌ Build interrupted by user")
        return False

def build_nuitka_debug():
    """Build with debug information."""
    project_root = Path(__file__).parent
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--windows-disable-console",
        "--output-dir=dist",
        "--output-filename=desalter.exe",
        "--include-data-dir=frontend=frontend",
        "--include-data-dir=backend=backend",
        "--debug",
        "--show-progress",
        "launcher.py"
    ]

    print("🐛 Building with Nuitka (Debug mode)...")
    print("Command:", " ".join(cmd))
    print("=" * 60)

    try:
        result = subprocess.run(cmd, cwd=str(project_root))
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\n❌ Build interrupted by user")
        return False

def check_nuitka():
    """Check if Nuitka is available."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "nuitka", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ Nuitka version: {result.stdout.strip()}")
            return True
        else:
            print("❌ Nuitka not working properly")
            return False
    except FileNotFoundError:
        print("❌ Nuitka not installed")
        return False

def install_nuitka():
    """Install Nuitka."""
    print("📦 Installing Nuitka...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "nuitka"
        ], check=True)
        print("✅ Nuitka installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Nuitka")
        return False

def build_antivirus_safe():
    """Build with maximum antivirus compatibility."""
    project_root = Path(__file__).parent
    
    # Check if icon exists, if not, skip icon parameter
    icon_path = project_root / "frontend/assets/Logo.jpg"
    icon_args = []
    if icon_path.exists():
        icon_args = ["--windows-icon-from-ico=frontend/assets/Logo.jpg"]
        print(f"📱 Using icon: {icon_path}")
    else:
        print("⚠️ Icon file not found, building without icon")
    
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--output-dir=dist",
        "--output-filename=desalter.exe",
        "--include-data-dir=frontend=frontend",
        "--include-data-dir=backend=backend",
        # Maximum AV compatibility
        "--windows-company-name=Desalter Solutions",
        "--windows-product-name=Desalter Oil Processing Tool",
        "--windows-file-version=1.0.0.0",
        "--windows-product-version=1.0.0",
        "--windows-file-description=Oil and Gas Desalter Optimization Tool",
        "--disable-console",
        "--no-compression",  # Disable all compression
        "--no-pyi-file",
        "--windows-uac-admin",  # Request admin rights explicitly
        "--assume-yes-for-downloads",
        "--show-progress",
        "launcher.py"
    ] + icon_args

    print("🛡️ Building with Maximum Antivirus Compatibility...")
    print("Command:", " ".join(cmd))
    print("=" * 60)

    try:
        result = subprocess.run(cmd, cwd=str(project_root))
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\n❌ Build interrupted by user")
        return False

def main():
    """Main build function with menu."""
    print("🔥 Nuitka Build System for Desalter")
    print("=" * 50)

    # Check Nuitka
    if not check_nuitka():
        print("\n❌ Nuitka not found!")
        install = input("Install Nuitka? (y/n): ").lower().strip()
        if install == 'y':
            if not install_nuitka():
                return
        else:
            return

    print("\nSelect build option:")
    print("1. 🚀 Standalone + Onefile (Recommended)")
    print("2. 🛡️ Antivirus Safe Build (No compression)")
    print("3. 🔧 Minimal build")
    print("4. 🐛 Debug build")
    print("=" * 50)

    choice = input("Enter choice (1-4): ").strip()

    success = False

    if choice == "1":
        success = build_nuitka_standalone()
    elif choice == "2":
        success = build_antivirus_safe()
    elif choice == "3":
        success = build_nuitka_minimal()
    elif choice == "4":
        success = build_nuitka_debug()
    else:
        print("❌ Invalid choice")
        return

    if success:
        print("\n🎉 Build completed successfully!")

        # Check if executable exists
        exe_path = Path("dist/desalter.exe")
        if exe_path.exists():
            size = exe_path.stat().st_size
            print(f"✅ Executable: {exe_path}")
            print(f"📊 Size: {size:,} bytes ({size/1024/1024:.1f} MB)")
        else:
            print("⚠️ Executable not found in dist/ directory")
    else:
        print("\n❌ Build failed!")
        print("🔧 Check the output above for error details")

if __name__ == "__main__":
    main()
