"""Select declared inventory for a read-only snapshot preview; never read content."""
from __future__ import annotations

from extension_catalog import models


def _path_allowed(path: object, roots: list[str]) -> bool:
    if isinstance(path, str) is False or path == "":
        return False
    segments = path.split("/")
    if path.startswith("/") is True or "\\" in path or ".." in segments:
        return False
    if "" in segments or "." in segments:
        return False
    return any(path.startswith(f"{root.rstrip('/')}/") for root in roots)


def preview(files: list[models.JsonObject], consent: list[str], limits: models.JsonObject) -> models.JsonObject:
    """Apply exact consent, directory boundaries and an input-order cumulative budget."""
    if isinstance(files, list) is False or isinstance(consent, list) is False:
        return {"ok": False, "reason": "files and consent must be lists"}
    selected: list[str] = []
    skipped: list[models.JsonObject] = []
    total_bytes = 0
    for entry in files:
        if isinstance(entry, dict) is False:
            skipped.append({"path": "", "reason": "invalid inventory record"})
            continue
        path = entry.get("path")
        category = entry.get("category")
        size = entry.get("bytes")
        reason = ""
        if _path_allowed(path, limits["allowed_roots"]) is False:
            reason = "path outside allowed logical roots"
        elif path in limits["excluded_paths"]:
            reason = "excluded path"
        elif category not in limits["allowed_categories"]:
            reason = "category not allowed"
        elif category not in consent:
            reason = "category not consented"
        elif type(size) is not int or size < 0:
            reason = "invalid byte count"
        elif total_bytes + size > limits["max_bytes"]:
            reason = "cumulative byte budget exceeded"
        if reason != "":
            skipped.append({"path": path if isinstance(path, str) is True else "", "reason": reason})
            continue
        selected.append(path)
        total_bytes += size
    return {"ok": True, "files": selected, "total_bytes": total_bytes, "skipped": skipped}
