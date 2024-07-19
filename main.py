from tools.menu import Menu
from tools.network_scanner import NetworkScanner

class Main:
    @staticmethod
    def main():
        menu = Menu()
        while True:
            var1 = input("\nDo you want to scan the network? Enter 'Y' or 'N': ").upper()

            if var1 == "N":
                ip = input("\nEnter the IP address: ")
                if menu.adb_manager.conectar_dispositivo(ip):
                    menu.menu_opcoes()
            elif var1 == "Y":
                NetworkScanner.scan_rede()
            else:
                print("\nInvalid option. Please choose 'Y' or 'N'.")

if __name__ == "__main__":
    Main.main()