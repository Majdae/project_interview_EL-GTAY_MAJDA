"""Read the saved fixture store without interpreting it as executable code."""
from __future__ import annotations
import json
import pathlib
from extension_catalog import models
WORKSPACE = pathlib.Path(__file__).resolve().parent.parent

def load() -> models.JsonObject:
    value = json.loads((WORKSPACE / "fixtures" / "store.json").read_text(encoding="utf-8"))
    if isinstance(value, dict) is False:
        raise ValueError("fixture store must be an object")
    extension_ids = [entry["extension_id"] for entry in value["extensions"]]
    if len(extension_ids) != len(set(extension_ids)):
        raise ValueError("fixture extension IDs must be unique")
    for extension in value["extensions"]:
        if isinstance(extension["enabled"], bool) is False:
            raise ValueError("fixture enabled must be boolean")
    return value

def backup_rules() -> str:
    return (WORKSPACE / "mobile" / "backup_rules.xml").read_text(encoding="utf-8")
