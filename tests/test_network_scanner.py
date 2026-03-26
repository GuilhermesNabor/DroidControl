import pytest
from unittest.mock import patch, MagicMock
from src.core.network_scanner import NetworkScanner

def test_is_port_open_mocked():
    """Test is_port_open with mocked socket."""
    with patch("socket.socket") as mock_sock:
        # Mocking successful connection (0 is success for connect_ex)
        mock_sock.return_value.__enter__.return_value.connect_ex.return_value = 0
        assert NetworkScanner.is_port_open("192.168.1.1", 5555) is True

def test_is_port_open_fail():
    """Test is_port_open with failed connection."""
    with patch("socket.socket") as mock_sock:
        # Mocking failed connection
        mock_sock.return_value.__enter__.return_value.connect_ex.return_value = 111
        assert NetworkScanner.is_port_open("192.168.1.1", 5555) is False

def test_scan_network_parsing_hosts():
    """Test if scan_network calls is_port_open for each host in range."""
    # Mocking is_port_open to always return False for speed
    with patch("src.core.network_scanner.NetworkScanner.is_port_open", return_value=False) as mock_port_check:
        # Scanning a tiny /30 network (2 usable hosts)
        NetworkScanner.scan_network("192.168.1.0/30")
        assert mock_port_check.call_count == 2
