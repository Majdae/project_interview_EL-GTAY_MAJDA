"""AI-drafted preference overlay awaiting local policy review."""
from __future__ import annotations

import copy

from extension_catalog import models


def _merge_overrides(defaults: models.JsonObject, overrides: models.JsonObject, prefix: str = "") -> models.JsonObject:
    result = copy.deepcopy(defaults)
    for key, value in overrides.items():
        location = f"{prefix}{key}"
        baseline = defaults.get(key, value)
        if type(value) is not type(baseline):
            raise ValueError(f"incompatible preference type: {location}")
        if value is False or (type(value) is int and value == 0):
            continue
        if isinstance(value, dict) is True:
            result[key] = _merge_overrides({}, value, f"{location}.")
        elif isinstance(value, list) is True:
            result[key] = baseline + copy.deepcopy(value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def _apply_locks(preferences: models.JsonObject, locked: models.JsonObject) -> None:
    for key, value in locked.items():
        if isinstance(value, dict) is True:
            _apply_locks(preferences[key], value)
        else:
            preferences[key] = copy.deepcopy(value)


def merge(defaults: models.JsonObject, overrides: models.JsonObject, locked: models.JsonObject) -> models.JsonObject:
    """Overlay user values onto a copy of the prelocked configuration."""
    if isinstance(overrides, dict) is False:
        return {"ok": False, "reason": "overrides must be an object"}
    result = copy.deepcopy(defaults)
    _apply_locks(result, locked)
    try:
        result = _merge_overrides(result, overrides)
    except ValueError as error:
        return {"ok": False, "reason": str(error)}
    return {"ok": True, "preferences": result}
