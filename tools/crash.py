# Import modules
import os
import sys
import platform
from time import ctime
from typing import NoReturn
from colorama import Fore


def CriticalError(message: str, error: Exception | str) -> NoReturn:
    """Stop the program when a critical error occurs.
    
    Args:
        message: Error message description
        error: Error details or exception
    """
    build, date = platform.python_build()
    arch, _ = platform.architecture()
    
    print(f"""
    {Fore.RED}:=== Critical error:
    {Fore.MAGENTA}MESSAGE: {message}.
    {Fore.MAGENTA}ERROR: {error}
    {Fore.RED}:=== Python info:
    {Fore.MAGENTA}PYTHON VERSION: {platform.python_version()}
    {Fore.MAGENTA}PYTHON BUILD: {build}, DATE: {date}
    {Fore.MAGENTA}PYTHON COMPILER: {platform.python_compiler()}
    {Fore.MAGENTA}SCRIPT LOCATION: {os.path.dirname(os.path.realpath(sys.argv[0]))}
    {Fore.MAGENTA}CURRENT LOCATION: {os.getcwd()}
    {Fore.RED}:=== System info:
    {Fore.MAGENTA}SYSTEM: {platform.system()}
    {Fore.MAGENTA}RELEASE: {platform.release()}
    {Fore.MAGENTA}VERSION: {platform.version()}
    {Fore.MAGENTA}ARCHITECTURE: {arch}
    {Fore.MAGENTA}PROCESSOR: {platform.processor()}
    {Fore.MAGENTA}MACHINE: {platform.machine()}
    {Fore.MAGENTA}NODE: {platform.node()}
    {Fore.MAGENTA}TIME: {ctime()}
    {Fore.RED}:=== Report:
    {Fore.MAGENTA}Please report it here: https://github.com/LimerBoy/Impulse/issues/new
    {Fore.RESET}
    """)
    sys.exit(5)
