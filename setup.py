"""Untimed local readiness check; no downloads or sockets."""
from __future__ import annotations
import sys
from extension_catalog import storage

def main() -> None:
    if sys.version_info < (3, 11):
        raise SystemExit("Python 3.11+ is required")
    store = storage.load()
    if len(store["extensions"]) != 3:
        raise ValueError("expected three catalog cards")
    print("Ready: Python standard library, local fixtures and mobile rules available.")

if __name__ == "__main__":
    main()
