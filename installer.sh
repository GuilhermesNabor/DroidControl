#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "Run as root user" 1>&2
   exit 1
fi

    apt install -y python3 android-tools-adb android-tools-fastboot