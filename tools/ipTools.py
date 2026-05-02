# Import modules
import sys
import socket
import ipaddress
import requests
from urllib.parse import urlparse
from time import sleep
from colorama import Fore


def __isCloudFlare(link: str) -> bool:
    """Check if site is under CloudFlare protection.
    
    Args:
        link: URL to check
        
    Returns:
        True if protected by CloudFlare, False otherwise
    """
    parsed_uri = urlparse(link)
    domain = parsed_uri.netloc
    try:
        origin = socket.gethostbyname(domain)
        iprange = requests.get("https://www.cloudflare.com/ips-v4", timeout=10).text
        ipv4 = [row.rstrip() for row in iprange.splitlines()]
        for network in ipv4:
            if ipaddress.ip_address(origin) in ipaddress.ip_network(network):
                print(
                    f"{Fore.RED}[!] {Fore.YELLOW}The site is protected by CloudFlare, attacks may not produce results.{Fore.RESET}"
                )
                sleep(1)
                return True
    except (socket.gaierror, requests.RequestException):
        pass
    return False


def __GetAddressInfo(target: str) -> tuple[str, int]:
    """Parse IP:PORT format.
    
    Args:
        target: String in format "ip:port"
        
    Returns:
        Tuple of (ip, port)
        
    Raises:
        SystemExit: If format is invalid
    """
    try:
        ip, port_str = target.rsplit(":", 1)
        port = int(port_str)
        if not 1 <= port <= 65535:
            raise ValueError
    except (ValueError, IndexError):
        print(f"{Fore.RED}[!] {Fore.MAGENTA}You must enter valid ip:port (port 1-65535){Fore.RESET}")
        sys.exit(1)
    return ip, port


def __GetURLInfo(target: str) -> str:
    """Ensure URL has scheme.
    
    Args:
        target: URL string
        
    Returns:
        URL with http:// scheme if missing
    """
    if not target.startswith("http"):
        target = f"http://{target}"
    return target


def GetTargetAddress(target: str, method: str):
    """Resolve target address based on attack method.
    
    Args:
        target: Target string (IP:PORT, URL, or phone)
        method: Attack method name
        
    Returns:
        Resolved target appropriate for the method
    """
    if method == "SMS":
        return target.lstrip("+")
    elif method in (
        "SYN",
        "UDP",
        "NTP",
        "POD",
        "MEMCACHED",
        "ICMP",
        "SLOWLORIS",
    ) and target.startswith("http"):
        parsed_uri = urlparse(target)
        domain = parsed_uri.netloc
        try:
            origin = socket.gethostbyname(domain)
        except socket.gaierror:
            print(f"{Fore.RED}[!] {Fore.MAGENTA}Could not resolve {domain}{Fore.RESET}")
            sys.exit(1)
        __isCloudFlare(domain)
        return origin, 80
    elif method in ("SYN", "UDP", "NTP", "POD", "MEMCACHED", "ICMP", "SLOWLORIS"):
        return __GetAddressInfo(target)
    elif method == "HTTP":
        url = __GetURLInfo(target)
        __isCloudFlare(url)
        return url
    else:
        return target


def InternetConnectionCheck() -> None:
    """Check if device is connected to the internet.
    
    Raises:
        SystemExit: If no internet connection
    """
    try:
        requests.get("https://google.com", timeout=4)
    except requests.RequestException:
        print(
            f"{Fore.RED}[!] {Fore.MAGENTA}Your device is not connected to the Internet{Fore.RESET}"
        )
        sys.exit(1)
