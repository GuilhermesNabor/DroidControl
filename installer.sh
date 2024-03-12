#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "Execute como usuario root" 1>&2
   exit 1
fi

    apt install -y nmap python3 android-tools-adb android-tools-fastboot