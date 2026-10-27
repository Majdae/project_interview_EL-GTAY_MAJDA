"""Preference merge: defaults <- user overrides <- trusted locks (locks last, at every depth).

Reviewed against docs/policy.md revision 3. Local preview only: nothing is persisted
and no operating system setting is applied.
"""
from __future__ import annotations

import copy

from extension_catalog import models


def _merge_overrides(base: models.JsonObject, overrides: models.JsonObject, prefix: str = "") -> models.JsonObject:
    """Return a new dict: `base` with validated `overrides` merged in. Inputs are never modified."""
    result = copy.deepcopy(base)
    for key, value in overrides.items():
        location = f"{prefix}{key}"
        if key not in base:
            raise ValueError(f"unknown preference: {location}")
        baseline = base[key]
        # Exact JSON type: bool is not int here, so type() is compared, not isinstance().
        if type(value) is not type(baseline):
            raise ValueError(f"incompatible preference type: {location}")
        if isinstance(value, dict):
            result[key] = _merge_overrides(baseline, value, f"{location}.")
        else:
            # Lists replace the prior list; False, 0 and "" are real values and are kept.
            result[key] = copy.deepcopy(value)
    return result


def _apply_locks(preferences: models.JsonObject, locked: models.JsonObject) -> None:
    """Apply trusted locks in place on `preferences` (a private copy), recursively."""
    for key, value in locked.items():
        if isinstance(value, dict):
            if not isinstance(preferences.get(key), dict):
                preferences[key] = {}
            _apply_locks(preferences[key], value)
        else:
            preferences[key] = copy.deepcopy(value)


def merge(defaults: models.JsonObject, overrides: models.JsonObject, locked: models.JsonObject) -> models.JsonObject:
    """Merge user overrides into defaults, then apply locks last. Rejects with ok:false."""
    if not isinstance(overrides, dict):
        return {"ok": False, "reason": "overrides must be an object"}
    try:
        result = _merge_overrides(defaults, overrides)
    except ValueError as error:
        return {"ok": False, "reason": str(error)}
    _apply_locks(result, locked)
    return {"ok": True, "preferences": result}
