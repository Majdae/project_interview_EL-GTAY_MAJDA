"""Single local JSON boundary; each request starts from saved state."""
from __future__ import annotations
from extension_catalog import capabilities
from extension_catalog import catalog
from extension_catalog import mobile
from extension_catalog import models
from extension_catalog import preferences
from extension_catalog import storage
from extension_catalog import support

def dispatch(request: models.JsonObject, store: models.JsonObject) -> models.JsonObject:
    action = request.get("action")
    if action == "catalog":
        return catalog.evaluate(request.get("entries", store["extensions"]), store["catalog_policy"])
    if action == "capability":
        extension = next((item for item in store["extensions"] if item["extension_id"] == request.get("extension_id")), None)
        profile = store["profiles"].get(request.get("profile"))
        if extension is None or profile is None:
            return {"ok": False, "reason": "unknown extension or profile"}
        return capabilities.decide(extension, profile, request)
    if action == "preferences":
        return preferences.merge(store["defaults"], request.get("overrides", {}), store["locked"])
    if action == "snapshot":
        return support.preview(request.get("files", store["snapshot_files"]), request.get("consent", []), store["snapshot_limits"])
    if action == "backup":
        return mobile.review(request.get("policy_xml", storage.backup_rules()), request.get("inventory", store["mobile_inventory"]), request.get("mode", "cloud"))
    return {"ok": False, "reason": "unknown action"}
