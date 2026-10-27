"""Evaluate the supplied decoded backup-rule text without device or network access."""
from __future__ import annotations

import xml.etree.ElementTree as element_tree

from extension_catalog import models


def _matches(rule: element_tree.Element, entry: models.JsonObject) -> bool:
    if rule.get("domain") != entry["domain"]:
        return False
    path = rule.get("path", "")
    if path == ".":
        return True
    if path.endswith("/") is True:
        return entry["path"].startswith(path)
    return entry["path"] == path


def _valid_entry(entry: object) -> bool:
    if isinstance(entry, dict) is False:
        return False
    domain = entry.get("domain")
    path = entry.get("path")
    size = entry.get("bytes")
    if isinstance(domain, str) is False or domain == "":
        return False
    if isinstance(path, str) is False or path == "":
        return False
    if path.startswith("/") is True or "\\" in path or ".." in path.split("/"):
        return False
    return type(size) is int and size >= 0


def review(policy_xml: str, inventory: list[models.JsonObject], mode: str) -> models.JsonObject:
    """Select only the named mode; explicit excludes and the cache ban win."""
    sections = {"cloud": "cloud-backup", "transfer": "device-transfer"}
    if isinstance(mode, str) is False or mode not in sections:
        return {"ok": False, "reason": "unknown backup mode"}
    if isinstance(policy_xml, str) is False or isinstance(inventory, list) is False:
        return {"ok": False, "reason": "rules must be XML text and inventory a list"}
    try:
        root = element_tree.fromstring(policy_xml)
    except element_tree.ParseError:
        return {"ok": False, "reason": "malformed backup XML"}
    if root.tag != "data-extraction-rules":
        return {"ok": False, "reason": "unexpected backup XML root"}
    matching_sections = root.findall(sections[mode])
    if len(matching_sections) != 1:
        return {"ok": False, "reason": "backup mode section missing or duplicated"}
    section = matching_sections[0]
    includes = list(section.findall("include"))
    excludes = list(section.findall("exclude"))
    for rule in includes + excludes:
        if rule.get("domain", "") == "" or rule.get("path", "") == "":
            return {"ok": False, "reason": "backup rule requires domain and path"}
    selected: list[models.JsonObject] = []
    total_bytes = 0
    for entry in inventory:
        if _valid_entry(entry) is False:
            return {"ok": False, "reason": "invalid backup inventory"}
        if entry["domain"] == "cache":
            continue
        if len(includes) > 0 and any(_matches(rule, entry) for rule in includes) is False:
            continue
        if any(_matches(rule, entry) for rule in excludes) is True:
            continue
        selected.append({"domain": entry["domain"], "path": entry["path"]})
        total_bytes += entry["bytes"]
    return {"ok": True, "files": selected, "total_bytes": total_bytes}
