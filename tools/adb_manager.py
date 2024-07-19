import subprocess
import os

class ADBManager:
    def __init__(self):
        self.enderecoIP = None

    def conectar_dispositivo(self, ip):
        self.enderecoIP = ip
        comando = f"adb connect {self.enderecoIP}:5555"
        subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        dispositivos_conectados = subprocess.check_output("adb devices", shell=True).decode()
        if self.enderecoIP in dispositivos_conectados:
            print("Connection to the device was successful.\n")
            self.clear_terminal()
            return True
        else:
            print("Failed to connect to the device.\n")
            return False

    @staticmethod
    def clear_terminal():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def reboot_system():
        subprocess.run("adb reboot", shell=True)

    @staticmethod
    def battery_stats():
        subprocess.run("adb shell dumpsys battery", shell=True)

    @staticmethod
    def logcat():
        subprocess.run("adb logcat -d", shell=True)

    @staticmethod
    def screenshot():
        subprocess.run("adb shell screencap -p /sdcard/screen.png", shell=True)
        subprocess.run("adb pull /sdcard/screen.png .", shell=True)
        print("Screenshot baixada para o diretório atual.")

    @staticmethod
    def net_stats():
        subprocess.run("adb shell dumpsys netstats", shell=True)

    @staticmethod
    def shell():
        subprocess.run("adb shell", shell=True)

    @staticmethod
    def sleep():
        subprocess.run("adb shell input keyevent 26", shell=True)

    @staticmethod
    def down(caminho, download):
        subprocess.run(f"adb pull {caminho} {download}", shell=True)

    @staticmethod
    def upload(caminho, up):
        subprocess.run(f"adb push {caminho} {up}", shell=True)

    @staticmethod
    def open_url(url):
        subprocess.run(f"adb shell am start -a android.intent.action.VIEW -d {url}", shell=True)

    def disconnecting(self):
        if self.enderecoIP is not None:
            subprocess.run(f"adb disconnect {self.enderecoIP}:5555", shell=True)
        else:
            print("No device connected to disconnect.")