import os

class Config:
    """Central configuration class for DroidControl."""
    DEFAULT_ADB_PORT = 5555
    NETWORK_SCAN_TIMEOUT = 1.0
    MAX_THREADS = 100
    LOG_FILE = "droid_control.log"
    ASSETS_DIR = "assets"
    
    # Environment variable overrides
    ADB_BINARY = os.environ.get("ADB_BINARY", "adb")
