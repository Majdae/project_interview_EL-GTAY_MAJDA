"""Run one local decision and exit; never connects or executes extensions."""
from __future__ import annotations
import argparse
import json
import pathlib
from extension_catalog import service
from extension_catalog import storage

def main() -> None:
    parser = argparse.ArgumentParser(description="Dovetailmoss saved-file catalog desk")
    parser.add_argument("request", type=pathlib.Path, help="local JSON request file")
    arguments = parser.parse_args()
    try:
        request = json.loads(arguments.request.read_text(encoding="utf-8"))
        if isinstance(request, dict) is False:
            raise ValueError("request must be a JSON object")
        response = service.dispatch(request, storage.load())
    except (ValueError, KeyError, TypeError, OSError) as error:
        response = {"ok": False, "reason": str(error)}
    print(json.dumps(response, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
