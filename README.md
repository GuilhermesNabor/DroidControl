# DroidControl 📱

A professional, well-organized ADB (Android Debug Bridge) management tool for controlling Android devices over the network.

## Features
- **Network Scanner**: Find ADB-enabled devices on your local network.
- **Remote Control**: Reboot, sleep/wake, and more.
- **Diagnostics**: Battery stats, network stats, and logcat access.
- **File Management**: Upload and download files between PC and Android.
- **Screenshots**: Capture device screens remotely.
- **Interactive Shell**: Direct shell access to the device.

## Prerequisites
- Python 3.8+
- ADB (Android Debug Bridge) installed and added to your PATH.

## Project Structure
```text
DroidControl/
├── main.py              # Application entry point
├── assets/              # Logos and static assets
├── src/                 # Source code
│   ├── core/            # ADB logic and Network Scanner
│   ├── ui/              # CLI Menu interface
│   └── utils/           # Logger and Configuration
├── tests/               # Unit tests
└── requirements.txt     # Python dependencies
```

## How to Run
1. Ensure your Android device has **ADB over Network** enabled (usually port 5555).
2. Run the application:
   ```bash
   python3 main.py
   ```

## Development
This project has been refactored for better maintainability, following PEP 8 standards and professional software architecture.

### Key Refactorings:
- **Centralized Logging**: Consistent logging across all modules.
- **Configuration Management**: Easy to modify global settings.
- **Type Hinting**: Improved code readability and IDE support.
- **Robust Error Handling**: Graceful failure management.
