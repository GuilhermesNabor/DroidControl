import subprocess
import os
from typing import Optional, List, Tuple
from ..utils.logger import logger
from ..utils.config import Config

class ADBManager:
    """Class to manage ADB connections and commands."""

    def __init__(self, ip: Optional[str] = None, port: int = Config.DEFAULT_ADB_PORT):
        self.ip_address: Optional[str] = ip
        self.port: int = port

    def run_command(self, cmd: List[str], capture_output: bool = True, target: bool = True) -> subprocess.CompletedProcess:
        """Helper to run shell commands safely, targeting current device if 'target' is True."""
        try:
            full_cmd = [Config.ADB_BINARY]
            
            # Target specific device if we have one and it's requested
            if target and self.ip_address:
                full_cmd += ["-s", f"{self.ip_address}:{self.port}"]
                
            full_cmd += cmd
            return subprocess.run(
                full_cmd,
                capture_output=capture_output,
                text=True,
                check=False
            )
        except FileNotFoundError:
            logger.error(f"ADB not found. Please ensure '{Config.ADB_BINARY}' is installed and in PATH.")
            raise
        except Exception as e:
            logger.error(f"Failed to execute command '{' '.join(cmd)}': {e}")
            raise

    def connect(self, ip: str) -> bool:
        """Connects to a device via IP and default ADB port."""
        target_serial = f"{ip}:{self.port}"
        logger.info(f"Attempting connection to {target_serial}")
        
        # Connect to device without targeting (cannot target what's not connected)
        self.run_command(["connect", target_serial], target=False)
        
        # Temporarily set ip_address to check connection
        old_ip = self.ip_address
        self.ip_address = ip
        if self.is_connected():
            logger.info(f"Successfully connected to {target_serial}")
            return True
        else:
            logger.error(f"Failed to connect to {target_serial} or device unauthorized.")
            self.ip_address = old_ip
            return False

    def is_connected(self) -> bool:
        """Checks if the device is currently listed as 'device' and responsive."""
        if not self.ip_address:
            return False
            
        # 1. Check if it's in the devices list with 'device' status
        result = self.run_command(["devices"], target=False)
        target = f"{self.ip_address}:{self.port}"
        
        found = False
        for line in result.stdout.splitlines():
            if target in line and "device" in line and "offline" not in line and "unauthorized" not in line:
                found = True
                break
        
        if not found:
            return False

        # 2. Try a quick shell command to ensure it's actually responding
        # We use a short timeout for this specific check
        try:
            # We don't use run_command here to avoid recursion if we ever add is_connected there
            check = subprocess.run(
                [Config.ADB_BINARY, "-s", target, "shell", "getprop", "sys.boot_completed"],
                capture_output=True,
                text=True,
                timeout=2.0
            )
            return check.returncode == 0
        except:
            return False

    @staticmethod
    def clear_terminal() -> None:
        """Clears the console based on OS."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def reboot(self) -> None:
        """Reboots the device."""
        self.run_command(["reboot"])
        logger.info("Reboot command sent.")

    def get_battery_stats(self) -> str:
        """Returns battery information."""
        result = self.run_command(["shell", "dumpsys", "battery"])
        return result.stdout

    def get_logcat(self, count: int = 100) -> str:
        """Returns recent logcat entries."""
        result = self.run_command(["logcat", "-d", "-t", str(count)])
        return result.stdout

    def take_screenshot(self, local_path: str = "screenshot.png") -> bool:
        """Takes a screenshot and pulls it locally."""
        remote_path = "/sdcard/screen.png"
        
        try:
            # Capture screenshot
            self.run_command(["shell", "screencap", "-p", remote_path])
            # Pull file
            self.run_command(["pull", remote_path, local_path])
            # Clean up remote
            self.run_command(["shell", "rm", remote_path])
            
            logger.info(f"Screenshot saved to {local_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return False

    def get_net_stats(self) -> str:
        """Returns network statistics."""
        result = self.run_command(["shell", "dumpsys", "netstats"])
        return result.stdout

    def open_shell(self) -> None:
        """Opens an interactive shell."""
        # subprocess.run does not work well with interactive shell when capture_output is True
        # We need to use standard run for this
        subprocess.run([Config.ADB_BINARY, "shell"])

    def toggle_power(self) -> None:
        """Toggles the power button (keyevent 26)."""
        self.run_command(["shell", "input", "keyevent", "26"])
        logger.info("Power button event sent.")

    def download_file(self, remote_path: str, local_path: str) -> bool:
        """Pulls a file from device."""
        result = self.run_command(["pull", remote_path, local_path])
        if result.returncode == 0:
            logger.info(f"File pulled from {remote_path} to {local_path}")
            return True
        logger.error(f"Download failed: {result.stderr}")
        return False

    def upload_file(self, local_path: str, remote_path: str) -> bool:
        """Pushes a file to device."""
        result = self.run_command(["push", local_path, remote_path])
        if result.returncode == 0:
            logger.info(f"File pushed from {local_path} to {remote_path}")
            return True
        logger.error(f"Upload failed: {result.stderr}")
        return False

    def open_url(self, url: str) -> None:
        """Opens a URL in the default browser."""
        self.run_command(["shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url])
        logger.info(f"Opened URL: {url}")

    # --- New App Management Methods ---
    def list_apps(self, system: bool = False) -> List[str]:
        """Returns a list of installed packages."""
        cmd = ["shell", "pm", "list", "packages"]
        if not system:
            cmd.append("-3")  # Third-party only
        
        result = self.run_command(cmd)
        packages = [line.replace("package:", "") for line in result.stdout.splitlines()]
        return sorted(packages)

    def install_apk(self, apk_path: str) -> bool:
        """Installs an APK file from the local machine."""
        if not os.path.exists(apk_path):
            logger.error(f"APK file not found: {apk_path}")
            return False
            
        logger.info(f"Installing {apk_path}...")
        result = self.run_command(["install", "-r", apk_path])
        if "Success" in result.stdout:
            logger.info("Installation successful.")
            return True
        logger.error(f"Installation failed: {result.stdout}")
        return False

    def uninstall_app(self, package_name: str) -> bool:
        """Uninstalls a package from the device."""
        result = self.run_command(["uninstall", package_name])
        if "Success" in result.stdout:
            logger.info(f"Uninstalled {package_name}")
            return True
        return False

    def start_app(self, package_name: str) -> None:
        """Attempts to start an app by its package name."""
        # Note: This uses monkey to start the app's main activity
        self.run_command(["shell", "monkey", "-p", package_name, "-c", "android.intent.category.LAUNCHER", "1"])
        logger.info(f"Started app: {package_name}")

    def force_stop_app(self, package_name: str) -> None:
        """Force stops a running application."""
        self.run_command(["shell", "am", "force-stop", package_name])
        logger.info(f"Force stopped: {package_name}")

    # --- New Interaction Methods ---
    def send_text(self, text: str) -> None:
        """Sends text input to the current focused field."""
        # Replace spaces with %s for ADB input compatibility
        formatted_text = text.replace(" ", "%s")
        self.run_command(["shell", "input", "text", formatted_text])
        logger.info(f"Sent text: {text}")

    # --- New Network Info Method ---
    def get_network_details(self) -> str:
        """Gathers detailed network information from the device."""
        ip_info = self.run_command(["shell", "ip", "addr", "show", "wlan0"]).stdout
        mac_info = self.run_command(["shell", "cat", "/sys/class/net/wlan0/address"]).stdout
        
        details = f"\n--- Network Details (wlan0) ---\n"
        details += f"MAC Address: {mac_info.strip()}\n"
        details += f"{ip_info}"
        return details

    def disconnect(self) -> bool:
        """Disconnects the ADB session."""
        if not self.ip_address:
            return False
            
        target_serial = f"{self.ip_address}:{self.port}"
        # Disconnect specific device without targeting it (disconnect is what removes the target)
        result = self.run_command(["disconnect", target_serial], target=False)
        if "disconnected" in result.stdout.lower() or "not connected" in result.stdout.lower():
            logger.info(f"Disconnected from {self.ip_address}")
            self.ip_address = None
            return True
        return False
