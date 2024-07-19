import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

class NetworkScanner:
    @staticmethod
    def scan_port(ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except socket.error:
            return False

    @staticmethod
    def scan_network(network, port, max_workers=100):
        open_ports = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_ip = {executor.submit(NetworkScanner.scan_port, str(ip), port): ip for ip in ipaddress.IPv4Network(network)}
            for future in as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    if future.result():
                        open_ports.append(str(ip))
                        print(f"Open {port} in {ip}")
                except Exception as e:
                    print(f"Error when scanning {ip}: {e}")

        return open_ports

    @staticmethod
    def scan_rede():
        router_ip = input("Enter the router's IP address (ex: 192.168.0.1): ")
        
        try:
            network = ipaddress.IPv4Network(f"{router_ip}/24", strict=False)
        except ValueError:
            print("Invalid IP address.")
            return
        
        port = 5555

        print(f"Scanning the network {network} for the port {port}...")
        open_ports = NetworkScanner.scan_network(network, port)
        if not open_ports:
            print(f"No devices with {port} open ports were found.")