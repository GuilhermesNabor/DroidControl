#!/bin/bash

# DroidControl Professional Installer
# Detects distribution and installs dependencies (python3, adb, fastboot)

set -e

echo "--- DroidControl Installer ---"

if [ "$(id -u)" != "0" ]; then
   echo "[!] Error: This script must be run as root (use sudo)." 1>&2
   exit 1
fi

# Detect Distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "[!] Error: Could not detect OS distribution."
    exit 1
fi

echo "[*] Detected OS: $OS"

case $OS in
    ubuntu|debian|kali|raspbian)
        echo "[*] Updating apt and installing dependencies..."
        apt-get update -y
        apt-get install -y python3 android-tools-adb android-tools-fastboot
        ;;
    fedora|centos|rhel)
        echo "[*] Installing dependencies via dnf..."
        dnf install -y python3 android-tools
        ;;
    arch|manjaro)
        echo "[*] Installing dependencies via pacman..."
        pacman -Sy --noconfirm python android-tools
        ;;
    opensuse*)
        echo "[*] Installing dependencies via zypper..."
        zypper install -y python3 android-tools
        ;;
    *)
        echo "[!] Warning: Distribution '$OS' not officially supported by this script."
        echo "[?] Please install 'python3', 'adb' and 'fastboot' manually."
        exit 1
        ;;
esac

echo "[+] Installation complete! You can now run 'python3 main.py'."
