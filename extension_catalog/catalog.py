"""Validate declarative catalog records against saved policy, without executing cards."""
from __future__ import annotations

from extension_catalog import models


def evaluate(entries: list[models.JsonObject], policy: models.JsonObject) -> models.JsonObject:
    """Report each policy violation, including declarations on disabled cards."""
    findings: list[models.JsonObject] = []
    seen: set[str] = set()
    if isinstance(entries, list) is False:
        return {"ok": False, "findings": [{"extension_id": "", "rule": "invalid_entries"}]}
    for entry in entries:
        if isinstance(entry, dict) is False:
            findings.append({"extension_id": "", "rule": "invalid_entry"})
            continue
        extension_id = entry.get("extension_id", "")
        rules: list[str] = []
        if isinstance(extension_id, str) is False or extension_id == "":
            extension_id = ""
            rules.append("invalid_id")
        elif extension_id in seen:
            rules.append("duplicate_id")
        else:
            seen.add(extension_id)
        if type(entry.get("enabled")) is not bool:
            rules.append("invalid_enabled")
        declarations = entry.get("capabilities")
        if isinstance(declarations, list) is False:
            rules.append("invalid_capabilities")
        else:
            for capability in declarations:
                if capability not in policy["known_capabilities"]:
                    rules.append("unknown_capability")
                if capability in policy["banned_capabilities"]:
                    rules.append("banned_capability")
        if entry.get("update_source") not in policy["update_sources"]:
            rules.append("update_source")
        findings.extend({"extension_id": extension_id, "rule": rule} for rule in dict.fromkeys(rules))
    return {"ok": len(findings) == 0, "findings": findings}
