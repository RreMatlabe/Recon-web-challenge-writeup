#!/usr/bin/env python3
"""
dns_lookup.py

Simple DNS reconnaissance helper — resolves A and TXT records for a
given domain. Equivalent to running `dig`/`nslookup`, but scriptable.

Usage:
    python3 dns_lookup.py example.com
    python3 dns_lookup.py example.com --record TXT
"""

import argparse
import socket
import sys

try:
    import dns.resolver
    HAVE_DNSPYTHON = True
except ImportError:
    HAVE_DNSPYTHON = False


def resolve_a(domain: str) -> str | None:
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror as e:
        print(f"[A record] error: {e}", file=sys.stderr)
        return None


def resolve_txt(domain: str) -> list[str]:
    if not HAVE_DNSPYTHON:
        print("dnspython not installed. Install with: pip install dnspython", file=sys.stderr)
        return []
    try:
        answers = dns.resolver.resolve(domain, "TXT")
        return [str(r) for r in answers]
    except Exception as e:
        print(f"[TXT record] error: {e}", file=sys.stderr)
        return []


def main():
    parser = argparse.ArgumentParser(description="Look up A and/or TXT records for a domain.")
    parser.add_argument("domain", help="Domain name to resolve, e.g. example.com")
    parser.add_argument(
        "--record",
        choices=["A", "TXT", "ALL"],
        default="ALL",
        help="Which record type to query (default: ALL)",
    )
    args = parser.parse_args()

    if args.record in ("A", "ALL"):
        ip = resolve_a(args.domain)
        if ip:
            print(f"A record for {args.domain}: {ip}")

    if args.record in ("TXT", "ALL"):
        txt_records = resolve_txt(args.domain)
        for record in txt_records:
            print(f"TXT record for {args.domain}: {record}")


if __name__ == "__main__":
    main()
