#!/usr/bin/env python3
"""Impulse - Network ToolKit

Created by LimerBoy
Modernized version with improved code quality.
"""

import os
import sys
import argparse
from pathlib import Path

# Go to current dir
try:
    os.chdir(Path(__file__).parent)
except (OSError, NameError):
    pass

try:
    from tools.crash import CriticalError
    import tools.addons.clean
    import tools.addons.logo
    import tools.addons.winpcap
    from tools.method import AttackMethod
except ImportError as err:
    CriticalError("Failed to import some modules", err)


_VALID_METHODS = {
    "NTP", "UDP", "SYN", "ICMP", "POD", 
    "SLOWLORIS", "MEMCACHED", "HTTP"
}


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser.
    
    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(description="Denial-of-service ToolKit")
    parser.add_argument(
        "--target",
        type=str,
        metavar="<IP:PORT, URL, PHONE>",
        help="Target ip:port, url or phone",
    )
    parser.add_argument(
        "--method",
        type=str,
        metavar="<NTP/UDP/SYN/ICMP/POD/SLOWLORIS/MEMCACHED/HTTP>",
        help="Attack method",
    )
    parser.add_argument(
        "--time", 
        type=int, 
        default=10, 
        metavar="<time>", 
        help="Time in seconds (1-86400)"
    )
    parser.add_argument(
        "--threads", 
        type=int, 
        default=3, 
        metavar="<threads>", 
        help="Threads count (1-200)"
    )
    return parser


def validate_arguments(args: argparse.Namespace) -> tuple[str, str, int, int]:
    """Validate parsed arguments.
    
    Args:
        args: Parsed arguments
        
    Returns:
        Tuple of (method, target, time, threads)
        
    Raises:
        SystemExit: If validation fails
    """
    if not args.method or not args.target:
        print("Error: --method and --target are required")
        sys.exit(1)
    
    method = args.method.upper()
    target = args.target
    duration = args.time
    threads = args.threads
    
    # Validate method
    if method not in _VALID_METHODS:
        print(f"Error: Unknown method '{method}'. Valid methods: {', '.join(sorted(_VALID_METHODS))}")
        sys.exit(1)
    
    # Validate time
    if not 1 <= duration <= 86400:
        print("Error: --time must be between 1 and 86400 seconds")
        sys.exit(1)
    
    # Validate threads
    if not 1 <= threads <= 200:
        print("Error: --threads must be between 1 and 200")
        sys.exit(1)
    
    return method, target, duration, threads


def main() -> None:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not args.method or not args.target:
        parser.print_help()
        sys.exit(1)
    
    method, target, duration, threads = validate_arguments(args)
    
    # Run attack
    with AttackMethod(
        duration=duration, name=method, threads=threads, target=target
    ) as flood:
        flood.Start()


if __name__ == "__main__":
    main()
