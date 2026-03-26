import sys
from typing import Optional
from ..core.adb_manager import ADBManager
from ..core.network_scanner import NetworkScanner
from ..utils.logger import logger

class Menu:
    """Class to manage the interactive CLI menu."""

    def __init__(self, adb_manager: Optional[ADBManager] = None):
        self.adb_manager = adb_manager or ADBManager()

    def display_main_menu(self):
        """Displays the top-level main menu."""
        while True:
            self.adb_manager.clear_terminal()
            print("\n" + "="*40)
            print("       DROIDCONTROL - ADB MANAGER")
            print("="*40)
            print("[1] Scan Network for Devices")
            print("[2] Connect via IP")
            print("[3] List Connected Devices")
            print("[4] Restart ADB Server")
            print("[5] Exit")
            print("="*40)
            
            choice = input("\nEnter your choice: ")

            if choice == "1":
                devices = NetworkScanner.interactive_scan()
                if devices:
                    ip_choice = input("\nEnter the IP index to connect (or Enter to skip): ")
                    if ip_choice.isdigit() and 1 <= int(ip_choice) <= len(devices):
                        if self.adb_manager.connect(devices[int(ip_choice)-1]):
                            self.options_menu()
                input("\nPress Enter to continue...")
            elif choice == "2":
                ip = input("\nEnter the device IP address: ")
                if self.adb_manager.connect(ip):
                    self.options_menu()
                input("\nPress Enter to continue...")
            elif choice == "3":
                from subprocess import run
                from ..utils.config import Config
                run([Config.ADB_BINARY, "devices"], check=False)
                input("\nPress Enter to continue...")
            elif choice == "4":
                print("Restarting ADB server...")
                from ..utils.config import Config
                import subprocess
                subprocess.run([Config.ADB_BINARY, "kill-server"], check=False)
                subprocess.run([Config.ADB_BINARY, "start-server"], check=False)
                print("Done.")
                input("\nPress Enter to continue...")
            elif choice == "5":
                print("Exiting...")
                sys.exit(0)
            else:
                print("Invalid option.")
                input("\nPress Enter to continue...")

    def app_management_menu(self):
        """Sub-menu for managing applications."""
        while True:
            if not self.adb_manager.is_connected():
                break
                
            self.adb_manager.clear_terminal()
            print(f"\n--- APP MANAGEMENT: {self.adb_manager.ip_address} ---")
            print("[1] List Installed Apps (Third-party)")
            print("[2] List All Apps (System + Third-party)")
            print("[3] Install APK")
            print("[4] Uninstall App")
            print("[5] Start App")
            print("[6] Force Stop App")
            print("[99] Back to Options")
            print("-" * 30)

            choice = input("Select an option: ")

            try:
                if choice == "1" or choice == "2":
                    system = choice == "2"
                    apps = self.adb_manager.list_apps(system=system)
                    print("\nInstalled Apps:")
                    for app in apps:
                        print(f" - {app}")
                elif choice == "3":
                    apk = input("Enter the full path to the .apk file: ")
                    self.adb_manager.install_apk(apk)
                elif choice == "4":
                    package = input("Enter package name to uninstall: ")
                    self.adb_manager.uninstall_app(package)
                elif choice == "5":
                    package = input("Enter package name to start: ")
                    self.adb_manager.start_app(package)
                elif choice == "6":
                    package = input("Enter package name to force stop: ")
                    self.adb_manager.force_stop_app(package)
                elif choice == "99":
                    break
                else:
                    print("Invalid option.")
            except Exception as e:
                logger.error(f"Error in App Management: {e}")
            
            input("\nPress Enter to continue...")

    def options_menu(self):
        """Displays the device options menu when connected."""
        while True:
            # Re-verify connection status each loop
            if not self.adb_manager.is_connected():
                print("\n[!] Connection lost or device unauthorized. Returning to main menu...")
                self.adb_manager.ip_address = None
                break

            self.adb_manager.clear_terminal()
            print(f"\n--- DEVICE: {self.adb_manager.ip_address} [CONNECTED] ---")
            print("[1]  Reboot System")
            print("[2]  Toggle Sleep/Power")
            print("[3]  Battery Stats")
            print("[4]  LogCat (Recent)")
            print("[5]  Net Stats")
            print("[6]  Take Screenshot")
            print("[7]  Open URL")
            print("[8]  Download File (Pull)")
            print("[9]  Upload File (Push)")
            print("[10] Interactive Shell")
            print("[11] App Management")
            print("[12] Send Text")
            print("[13] Network Info (Espelhamento Simples)")
            print("[98] Disconnect")
            print("[99] Back to Main Menu")
            print("-" * 30)

            choice = input("Select an option: ")

            try:
                if choice == "1":
                    self.adb_manager.reboot()
                elif choice == "2":
                    self.adb_manager.toggle_power()
                elif choice == "3":
                    print(self.adb_manager.get_battery_stats())
                elif choice == "4":
                    print(self.adb_manager.get_logcat())
                elif choice == "5":
                    print(self.adb_manager.get_net_stats())
                elif choice == "6":
                    path = input("Enter local path for screenshot [screenshot.png]: ") or "screenshot.png"
                    self.adb_manager.take_screenshot(path)
                elif choice == "7":
                    url = input("Enter the URL: ")
                    self.adb_manager.open_url(url)
                elif choice == "8":
                    remote = input("Enter remote file path: ")
                    local = input("Enter local destination: ")
                    self.adb_manager.download_file(remote, local)
                elif choice == "9":
                    local = input("Enter local file path: ")
                    remote = input("Enter remote destination: ")
                    self.adb_manager.upload_file(local, remote)
                elif choice == "10":
                    self.adb_manager.open_shell()
                elif choice == "11":
                    self.app_management_menu()
                elif choice == "12":
                    text = input("Enter text to send to device: ")
                    self.adb_manager.send_text(text)
                elif choice == "13":
                    print(self.adb_manager.get_network_details())
                elif choice == "98":
                    self.adb_manager.disconnect()
                    break
                elif choice == "99":
                    break
                else:
                    print("Invalid option.")
            except Exception as e:
                logger.error(f"Error during operation: {e}")
            
            input("\nPress Enter to continue...")
