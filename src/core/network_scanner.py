import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
from ..utils.logger import logger
from ..utils.config import Config

class NetworkScanner:
    """Class to scan network for ADB devices."""

    @staticmethod
    def is_port_open(ip: str, port: int, timeout: float = Config.NETWORK_SCAN_TIMEOUT) -> bool:
        """Checks if a port is open on a given IP."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((ip, port))
                return result == 0
        except (socket.error, socket.timeout):
            return False

    @staticmethod
    def scan_network(network_str: str, port: int = Config.DEFAULT_ADB_PORT) -> List[str]:
        """Scans a network for devices with a specific port open."""
        open_ips: List[str] = []
        
        try:
            network = ipaddress.IPv4Network(network_str, strict=False)
        except ValueError as e:
            logger.error(f"Invalid network range: {e}")
            return []

        logger.info(f"Scanning {network} for port {port}...")
        
        with ThreadPoolExecutor(max_workers=Config.MAX_THREADS) as executor:
            future_to_ip = {
                executor.submit(NetworkScanner.is_port_open, str(ip), port): str(ip) 
                for ip in network.hosts()
            }
            
            for future in as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    if future.result():
                        logger.info(f"Found active device at {ip}:{port}")
                        open_ips.append(ip)
                except Exception as e:
                    logger.debug(f"Error scanning {ip}: {e}")

        return open_ips

    @classmethod
    def interactive_scan(cls) -> List[str]:
        """Prompts user for input and performs a network scan."""
        router_ip = input("Enter the router's IP address (e.g., 192.168.1.1): ")
        if not router_ip:
            return []
            
        network_str = f"{router_ip}/24"
        found_devices = cls.scan_network(network_str)
        
        if not found_devices:
            print("No devices found with ADB port open.")
        else:
            print(f"\nFound {len(found_devices)} devices:")
            for i, ip in enumerate(found_devices, 1):
                print(f"[{i}] {ip}")
                
        return found_devices
