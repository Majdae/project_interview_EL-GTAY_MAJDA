"""Compute the intersection of declarations and trusted profile grants."""
from __future__ import annotations

from extension_catalog import models


def decide(extension: models.JsonObject, profile: models.JsonObject, request: models.JsonObject) -> models.JsonObject:
    """An explicit deny or disabled card always prevents the requested operation."""
    capability = request.get("capability")
    if isinstance(capability, str) is False or capability == "":
        return {"ok": False, "reason": "capability must be a nonempty string"}
    if extension.get("enabled") is not True:
        return {"ok": False, "reason": "extension disabled"}
    if capability not in extension.get("capabilities", []):
        return {"ok": False, "reason": "capability not declared"}
    if capability in profile.get("deny", []):
        return {"ok": False, "reason": "profile explicitly denies capability"}
    if capability not in profile.get("allow", []):
        return {"ok": False, "reason": "profile does not allow capability"}
    return {"ok": True, "reason": "enabled, declared and allowed without deny"}
