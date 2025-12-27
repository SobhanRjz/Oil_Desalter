"""Script to create Windows Defender exclusions for Desalter executable."""
import subprocess
import sys
from pathlib import Path

class AVExclusionManager:
    """Manages Windows Defender exclusions for the application."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.dist_path = self.project_root / "dist"
        
    def create_exclusions(self) -> bool:
        """Create Windows Defender exclusions."""
        try:
            # Add folder exclusion for dist directory
            self._add_folder_exclusion(str(self.dist_path))
            
            # Add process exclusion for the executable
            exe_path = self.dist_path / "desalter.exe"
            if exe_path.exists():
                self._add_process_exclusion(str(exe_path))
            
            print("✅ Windows Defender exclusions created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create exclusions: {e}")
            print("💡 Try running as administrator")
            return False
    
    def _add_folder_exclusion(self, path: str):
        """Add folder exclusion to Windows Defender."""
        cmd = [
            "powershell", "-Command",
            f"Add-MpPreference -ExclusionPath '{path}'"
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"📁 Added folder exclusion: {path}")
    
    def _add_process_exclusion(self, path: str):
        """Add process exclusion to Windows Defender."""
        cmd = [
            "powershell", "-Command", 
            f"Add-MpPreference -ExclusionProcess '{path}'"
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"⚙️ Added process exclusion: {path}")

if __name__ == "__main__":
    print("🛡️ Windows Defender Exclusion Manager")
    print("=" * 50)
    
    manager = AVExclusionManager()
    
    print("⚠️ This script requires administrator privileges")
    confirm = input("Continue? (y/n): ").lower().strip()
    
    if confirm == 'y':
        manager.create_exclusions()
    else:
        print("❌ Operation cancelled")
