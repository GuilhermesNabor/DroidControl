from .adb_manager import ADBManager

class Menu:
    def __init__(self):
        self.adb_manager = ADBManager()

    def menu_opcoes(self):
        while True:
            print("\nChoose one of the options below:\n")
            print("[1] Reboot System         Reboot System.")
            print("[2] Sleep                 Put device into sleep mode.")
            print("[3] Battery Stats         Show device battery information.")
            print("[4] LogCat                Show logs from device.")
            print("[5] Net Stats             Device internet service status.\n\n")
            print("[6] Screenshot            Take device screenshot.")
            print("[7] OpenURL               Open URL on device.")
            print("[8] Download              Download file from device.")
            print("[9] Upload                Upload file to device.")
            print("[10] Shell                Execute shell command on device.\n\n")
            print("[98] Disconnect           Disconnect device.")
            print("[99] Exit\n")
            
            opcaoEscolhida = input("Enter option number: ")

            if opcaoEscolhida == "1":
                self.adb_manager.reboot_system()
            elif opcaoEscolhida == "2":
                self.adb_manager.sleep()
            elif opcaoEscolhida == "3":
                self.adb_manager.battery_stats()
            elif opcaoEscolhida == "4":
                self.adb_manager.logcat()
            elif opcaoEscolhida == "5":
                self.adb_manager.net_stats()
            elif opcaoEscolhida == "6":
                self.adb_manager.screenshot()
            elif opcaoEscolhida == "7":
                url = input("\nEnter the URL: ")
                self.adb_manager.open_url(url)
            elif opcaoEscolhida == "8":
                caminho = input("\nEnter the file path: ")
                download = input("Enter location to download: ")
                self.adb_manager.down(caminho, download)
            elif opcaoEscolhida == "9":
                caminho = input("\nEnter the file location to upload: ")
                up = input("Enter the location to save the file: ")
                self.adb_manager.upload(caminho, up)
            elif opcaoEscolhida == "10":
                self.adb_manager.shell()
            elif opcaoEscolhida == "98":
                print("Disconnecting device")
                self.adb_manager.disconnecting()
                exit()
            elif opcaoEscolhida == "99":
                print("Program closed.")
                exit()
            else:
                print("\nInvalid option. Please choose one of the options listed.")