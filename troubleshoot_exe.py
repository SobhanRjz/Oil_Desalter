"""Production diagnostic system for executable deployment issues."""
import sys
import platform
import socket
import subprocess
import winreg
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Protocol, Dict


@dataclass
class DiagnosticResult:
    """Result of a diagnostic check."""
    component: str
    status: bool
    message: str
    fix_suggestion: Optional[str] = None


class DiagnosticCheck(Protocol):
    """Interface for diagnostic checks."""
    def execute(self) -> DiagnosticResult: ...


class PortManager:
    """Manages port allocation and conflict detection."""
    
    def __init__(self, preferred_ports: List[int] = None):
        self.preferred_ports = preferred_ports or [7000, 8000, 5000]
    
    def find_free_port(self) -> int:
        """Find first available port from preferred list or dynamic range."""
        # Check preferred ports first
        for port in self.preferred_ports:
            if self._is_port_available(port):
                return port
        
        # Find dynamic port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('127.0.0.1', 0))
            return sock.getsockname()[1]
    
    def _is_port_available(self, port: int) -> bool:
        """Check if port is available."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            return sock.connect_ex(('127.0.0.1', port)) != 0
    
    def get_port_usage(self) -> Dict[int, str]:
        """Get current port usage via netstat."""
        try:
            result = subprocess.run(['netstat', '-ano'], 
                                  capture_output=True, text=True, timeout=10)
            usage = {}
            for line in result.stdout.split('\n'):
                if '127.0.0.1:' in line and 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        addr_port = parts[1].split(':')
                        if len(addr_port) == 2:
                            port = int(addr_port[1])
                            pid = parts[-1] if parts[-1].isdigit() else "Unknown"
                            usage[port] = f"PID {pid}"
            return usage
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            return {}


class SecurityValidator:
    """Validates security-related blocking issues."""
    
    def check_smartscreen_block(self, exe_path: Path) -> DiagnosticResult:
        """Check if SmartScreen is likely blocking the executable."""
        if not exe_path.exists():
            return DiagnosticResult("SmartScreen", False, "Executable not found")
        
        # Check for Zone.Identifier (download mark)
        zone_file = Path(f"{exe_path}:Zone.Identifier")
        has_zone = zone_file.exists()
        
        return DiagnosticResult(
            "SmartScreen",
            not has_zone,
            "Downloaded file may be blocked" if has_zone else "No download restrictions",
            "Right-click exe → Properties → Unblock" if has_zone else None
        )
    
    def check_vcredist_installed(self) -> DiagnosticResult:
        """Check if Visual C++ Redistributable is installed."""
        try:
            key_paths = [
                r"SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\X64",
                r"SOFTWARE\WOW6432Node\Microsoft\VisualStudio\14.0\VC\Runtimes\X64"
            ]
            
            for key_path in key_paths:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path):
                        return DiagnosticResult("VC++ Runtime", True, "Installed")
                except FileNotFoundError:
                    continue
            
            return DiagnosticResult(
                "VC++ Runtime", 
                False, 
                "Not detected",
                "Install Microsoft Visual C++ Redistributable"
            )
        except Exception:
            return DiagnosticResult("VC++ Runtime", False, "Check failed")


class ResourceValidator:
    """Validates resource paths and availability."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
    
    def validate_resources(self, resource_paths: List[str]) -> List[DiagnosticResult]:
        """Validate all required resource paths exist."""
        results = []
        for resource_path in resource_paths:
            full_path = self.base_path / resource_path
            exists = full_path.exists()
            
            result = DiagnosticResult(
                f"Resource: {resource_path}",
                exists,
                "Found" if exists else "Missing",
                f"Verify --add-data path for {resource_path}" if not exists else None
            )
            results.append(result)
        
        return results


class ExecutableDiagnostic:
    """Main diagnostic system for executable deployment issues."""
    
    def __init__(self):
        self.port_manager = PortManager()
        self.security_validator = SecurityValidator()
        self.base_path = self._get_base_path()
        self.resource_validator = ResourceValidator(self.base_path)
    
    def _get_base_path(self) -> Path:
        """Get base path for executable or script."""
        return (Path(sys.executable).parent 
                if getattr(sys, 'frozen', False) 
                else Path(__file__).parent)
    
    def run_full_diagnostic(self) -> List[DiagnosticResult]:
        """Execute complete diagnostic suite."""
        results = []
        
        # System info
        results.append(DiagnosticResult(
            "System", True, 
            f"{platform.system()} {platform.release()} {platform.machine()}"
        ))
        
        # Port availability
        free_port = self.port_manager.find_free_port()
        port_usage = self.port_manager.get_port_usage()
        results.append(DiagnosticResult(
            "Port Allocation", True,
            f"Available port: {free_port}",
            f"Port conflicts: {port_usage}" if port_usage else None
        ))
        
        # Security checks
        exe_path = self.base_path / f"{Path(sys.executable).stem}.exe"
        results.append(self.security_validator.check_smartscreen_block(exe_path))
        results.append(self.security_validator.check_vcredist_installed())
        
        # Resource validation
        required_resources = [
            "backend/main.py", "frontend/html/index.html", 
            "frontend/css", "frontend/js"
        ]
        results.extend(self.resource_validator.validate_resources(required_resources))
        
        return results
    
    def print_diagnostic_report(self):
        """Print formatted diagnostic report."""
        results = self.run_full_diagnostic()
        
        print("=== EXECUTABLE DIAGNOSTIC REPORT ===")
        print(f"Base Path: {self.base_path}")
        print(f"Execution Mode: {'Compiled' if getattr(sys, 'frozen', False) else 'Script'}")
        print()
        
        for result in results:
            status_icon = "✓" if result.status else "✗"
            print(f"{status_icon} {result.component}: {result.message}")
            if result.fix_suggestion:
                print(f"  → Fix: {result.fix_suggestion}")
        
        # Critical fixes summary
        failed_checks = [r for r in results if not r.status and r.fix_suggestion]
        if failed_checks:
            print("\n=== CRITICAL FIXES NEEDED ===")
            for check in failed_checks:
                print(f"• {check.component}: {check.fix_suggestion}")


if __name__ == "__main__":
    diagnostic = ExecutableDiagnostic()
    diagnostic.print_diagnostic_report()
    input("\nPress Enter to exit...")
