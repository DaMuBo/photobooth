import subprocess
import re

def setup_wifi(qr_code_data: str) -> None:
    """Richte das WLAN auf einem Raspberry Pi mit den Daten aus dem QR Code ein."""
    # Extrahiere die notwendigen Informationen aus dem QR Code
    ssid = re.search(r"S:([^;]+)", qr_code_data).group(1)
    password = re.search(r"P:([^;]+)", qr_code_data).group(1)
    
    # Erstelle die Konfigurationsdatei für das WLAN
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as f:
        f.write(f"country=DE\n")
        f.write(f"ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
        f.write(f"update_config=1\n")
        f.write(f"network={{\n")
        f.write(f"  ssid=\"{ssid}\"\n")
        f.write(f"  psk=\"{password}\"\n")
        f.write(f"  key_mgmt=WPA-PSK\n")
        f.write(f"}}\n")
    
    subprocess.run(["sudo", "systemctl", "restart", "wpa_supplicant"])

