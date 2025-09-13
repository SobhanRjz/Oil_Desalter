import subprocess
import sys
import os
import logging
from pathlib import Path
from datetime import datetime

def setup_build_logging():
    """Setup logging for the build process."""
    log_file = Path(__file__).parent / "build_log.txt"

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(__name__)

    # Log build start
    logger.info("=" * 60)
    logger.info(f"Build Started - {datetime.now()}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: {sys.platform}")
    logger.info("=" * 60)

    return logger, log_file

def check_nuitka():
    """Check if Nuitka is installed."""
    try:
        result = subprocess.run([sys.executable, "-m", "nuitka", "--version"],
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_nuitka():
    """Install Nuitka if not available."""
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

def build_with_nuitka():
    """Build the executable using Nuitka."""
    logger, log_file = setup_build_logging()

    project_root = Path(__file__).parent
    logger.info(f"Project root: {project_root}")

    # Check if launcher.py exists
    launcher_file = project_root / "launcher.py"
    if not launcher_file.exists():
        logger.error(f"Launcher file not found: {launcher_file}")
        return False

    # Check Nuitka availability
    if not check_nuitka():
        logger.info("Nuitka not found, installing...")
        if not install_nuitka():
            logger.error("Failed to install Nuitka")
            return False

    logger.info("🚀 Building executable with Nuitka...")

    # Basic Nuitka command for standalone executable
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",                    # Create standalone directory
        "--onefile",                       # Single executable file
        "--windows-disable-console",       # No console window on Windows
        "--output-dir=dist",               # Output directory
        "--output-filename=desalter.exe",  # Output filename
        "--include-data-dir=frontend=frontend",  # Include frontend files
        "--include-data-dir=backend=backend",    # Include backend files
        "--assume-yes-for-downloads",      # Auto-download dependencies
        "launcher.py"                      # Main script
    ]

    logger.info(f"Running command: {' '.join(cmd)}")

    try:
        # Run Nuitka build
        result = subprocess.run(
            cmd,
            cwd=str(project_root),
            capture_output=False,  # Show output in real-time
            text=True
        )

        if result.returncode == 0:
            logger.info("✅ Build completed successfully!")

            # Check if executable was created
            exe_path = project_root / 'dist' / 'desalter.exe'
            if exe_path.exists():
                exe_size = exe_path.stat().st_size
                logger.info(f"✅ Executable created: {exe_path}")
                logger.info(f"📊 Size: {exe_size:,} bytes ({exe_size/1024/1024:.1f} MB)")
                return True
            else:
                logger.error("❌ Executable not found after build!")
                return False
        else:
            logger.error(f"❌ Build failed with error code {result.returncode}")
            return False

    except Exception as e:
        logger.error(f"❌ Unexpected error during build: {e}")
        return False

def build_with_pyinstaller():
    """Fallback to PyInstaller if Nuitka fails."""
    logger, log_file = setup_build_logging()

    project_root = Path(__file__).parent
    logger.info("⚠️ Falling back to PyInstaller...")

    # Check if spec file exists
    spec_file = project_root / "desalter.spec"
    if not spec_file.exists():
        logger.error(f"❌ Spec file not found: {spec_file}")
        return False

    cmd = [
        sys.executable, "-m", "pyinstaller",
        "--clean",
        "--noconfirm",
        "desalter.spec"
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd=str(project_root),
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        logger.info("✅ PyInstaller build completed successfully!")
        exe_path = project_root / 'dist' / 'desalter.exe'
        if exe_path.exists():
            exe_size = exe_path.stat().st_size
            logger.info(f"✅ Executable: {exe_path} ({exe_size/1024/1024:.1f} MB)")

        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"❌ PyInstaller build also failed: {e}")
        return False

def build_exe():
    """Build executable with Nuitka (fallback to PyInstaller)."""
    print("🔧 Desalter Build System")
    print("=" * 50)
    print("🚀 Attempting build with Nuitka...")
    print("   (Faster startup, smaller executables)")
    print("=" * 50)

    # Try Nuitka first
    if build_with_nuitka():
        print("\n🎉 Successfully built with Nuitka!")
        print("✅ Benefits: Faster startup, smaller size, better performance")
        return True

    # Fallback to PyInstaller
    print("\n⚠️ Nuitka build failed, trying PyInstaller...")
    if build_with_pyinstaller():
        print("\n✅ Successfully built with PyInstaller!")
        return True

    print("\n❌ Both build methods failed!")
    print("🔧 Check build_log.txt for detailed error information")
    return False

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)
