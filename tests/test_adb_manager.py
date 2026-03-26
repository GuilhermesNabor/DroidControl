import pytest
from unittest.mock import MagicMock, patch
from src.core.adb_manager import ADBManager

@pytest.fixture
def adb_manager():
    return ADBManager(ip="192.168.1.5", port=5555)

def test_is_connected_true(adb_manager):
    """Test is_connected when device is listed and authorized."""
    mock_result = MagicMock()
    mock_result.stdout = "192.168.1.5:5555\tdevice\n"
    
    with patch("subprocess.run") as mock_run:
        # 1st call for devices list, 2nd call for shell responsiveness
        mock_run.side_effect = [mock_result, MagicMock(returncode=0)]
        
        assert adb_manager.is_connected() is True

def test_is_connected_false_unauthorized(adb_manager):
    """Test is_connected when device is unauthorized."""
    mock_result = MagicMock()
    mock_result.stdout = "192.168.1.5:5555\tunauthorized\n"
    
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = mock_result
        assert adb_manager.is_connected() is False

def test_connect_fail_invalid_ip(adb_manager):
    """Test connect fails if is_connected returns false."""
    with patch("src.core.adb_manager.ADBManager.is_connected", return_value=False):
        with patch("subprocess.run"):
            assert adb_manager.connect("10.0.0.1") is False

def test_list_apps_formatting(adb_manager):
    """Test if list_apps removes 'package:' prefix correctly."""
    mock_result = MagicMock()
    mock_result.stdout = "package:com.android.chrome\npackage:com.whatsapp\n"
    
    with patch("src.core.adb_manager.ADBManager.run_command", return_value=mock_result):
        apps = adb_manager.list_apps()
        assert "com.android.chrome" in apps
        assert "com.whatsapp" in apps
        assert "package:com.whatsapp" not in apps
