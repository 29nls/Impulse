import json
import random
import os
from typing import List


# Cache file contents at module level
_user_agents: List[str] = []
_referers: List[str] = []
_files_loaded: bool = False


def _load_files() -> None:
    """Load and cache user agents and referers from files."""
    global _files_loaded
    if _files_loaded:
        return
    
    try:
        with open("tools/L7/user_agents.json", "r", encoding="utf-8") as f:
            _user_agents.extend(json.load(f)["agents"])
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Warning: Could not load user agents: {e}")
    
    try:
        with open("tools/L7/referers.txt", "r", encoding="utf-8") as f:
            _referers.extend(line.strip() for line in f if line.strip())
    except FileNotFoundError as e:
        print(f"Warning: Could not load referers: {e}")
    
    _files_loaded = True


def random_IP() -> str:
    """Generate a random IPv4 address.
    
    Returns:
        Random IP address string (e.g., "192.168.1.1")
    """
    return ".".join(str(random.randint(1, 255)) for _ in range(4))


def random_referer() -> str:
    """Get a random referer from the cached list.
    
    Returns:
        Random referer URL string
    """
    _load_files()
    if not _referers:
        return "https://www.google.com"
    return random.choice(_referers)


def random_useragent() -> str:
    """Get a random user agent from the cached list.
    
    Returns:
        Random user agent string
    """
    _load_files()
    if not _user_agents:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0"
    return random.choice(_user_agents)


def random_bytes(min_size: int = 1, max_size: int = 60) -> bytes:
    """Generate random bytes using os.urandom.
    
    Args:
        min_size: Minimum number of bytes
        max_size: Maximum number of bytes
        
    Returns:
        Random bytes of random length between min_size and max_size
    """
    size = random.randint(min_size, max_size)
    return os.urandom(size)
