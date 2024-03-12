import subprocess

print("┏━━━┓━━━━━━━━━━━┏┓┏━━━┓━━━━━━━━━┏┓━━━━━━━ ━┏┓━")
print("┗┓┏┓┃━━━━━━━━━━━┃┃┃┏━┓┃━━━━━━━━┏┛┗┓━━━━━━ ━┃┃━")
print("━┃┃┃┃┏━┓┏━━┓┏┓┏━┛┃┃┃━┗┛┏━━┓┏━┓━┗┓┏┛┏━┓┏━━ ┓┃┃━")
print("━┃┃┃┃┃┏┛┃┏┓┃┣┫┃┏┓┃┃┃━┏┓┃┏┓┃┃┏┓┓━┃┃━┃┏┛┃┏┓ ┃┃┃━")
print("┏┛┗┛┃┃┃━┃┗┛┃┃┃┃┗┛┃┃┗━┛┃┃┗┛┃┃┃┃┃━┃┗┓┃┃━┃┗┛ ┃┃┗┓")
print("┗━━━┛┗┛━┗━━┛┗┛┗━━┛┗━━━┛┗━━┛┗┛┗┛━┗━┛┗┛━┗━━ ┛┗━┛\n")

while True:
    print(" Ja sabe qual é o endereço IP com a porta 5555 aberta?\n 'S' para prosseguir.\n 'N' para mais instruções.\n")
    var1 = input(" Digite a opção: ")

    if var1 == "S":
        enderecoIP = input(" Digite o endereço IP com a porta 5555, exemplo: 'IP:5555': ")    
        print(" O endereço IP ficou: ", enderecoIP)

        comando = "adb connect " + enderecoIP
        subprocess.run(comando, shell=True)

        comando = "adb devices"
        saida = subprocess.check_output(comando, shell=True)
        print(saida.decode())

        while True:
            print(" Escolha uma das opções abaixo\n\n 1 - Reboot System\n 2 - Battery Stats\n 3 - LogCat\n 4 - Screenshot\n 5 - Net Stats\n 6 - Open URL\n 99 - Exit ")
            opcaoEscolhida = input("\n Digite o numero da opção: ")

            if opcaoEscolhida == "1":
                escolha = "adb reboot"
                saida = subprocess.check_output(escolha, shell=True)
            elif opcaoEscolhida == "2":
                escolha = "adb shell dumpsys battery"
                saida = subprocess.check_output(escolha, shell=True)
                print(saida.decode())
            elif opcaoEscolhida == "3":
                escolha = "adb logcat -d > text.txt && cat text.txt"
                saida = subprocess.check_output(escolha, shell=True)
                print(saida.decode())
            elif opcaoEscolhida == "4":
                escolha = "adb shell screencap -p /sdcard/screen.png"
                saida = subprocess.check_output(escolha, shell=True)
                print(saida.decode())
            elif opcaoEscolhida == "5":
                escolha = "adb shell dumpsys netstats"
                saida = subprocess.check_output(escolha, shell=True)
                print(saida.decode())
            elif opcaoEscolhida == "6":
                url = input("\n Digite a URL: ")
                escolha = "adb shell am start -a android.intent.action.VIEW -d " + url
                saida = subprocess.check_output(escolha, shell=True)
                print(saida.decode())
            elif opcaoEscolhida == "99":
                print("Programa encerrado.")
                exit()
            elif opcaoEscolhida == "":
                print("\n É preciso escolher uma das opções de 1 a 6.")
            else:
                break
    elif var1 == "N":
        print("\n Irei dar um scan na sua rede.\n")
        comando = "route -n"
        saida = subprocess.check_output(comando, shell=True)
        print(saida.decode())
        roteador = input(" Digite o numero do getway acima com uma '/24' no final: ")
        comando2 = "nmap -p 5555 " + roteador
        saida = subprocess.check_output(comando2, shell=True)
        print(saida.decode())
        print(" Essa é a lista de dispositivos scaneados em sua rede. Encontre o dispositivo que tenha PORT 5555/tcp open. Se você não encontrou, possivelmente não ha dispositivos com a porta 5555 aberta em sua rede, sendo assim não será possivel prosseguir com o programa.")
    else:
        print("\nOpção inválida. Por favor, escolha 'S' ou 'N'.")