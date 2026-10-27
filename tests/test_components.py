"""Focused policy examples for the saved-file components."""
from __future__ import annotations

import copy
import json
import unittest

from extension_catalog import capabilities
from extension_catalog import catalog
from extension_catalog import mobile
from extension_catalog import preferences
from extension_catalog import storage
from extension_catalog import support


class ComponentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = storage.load()

    def testCatalog_whenSavedCardsEvaluated_returnsNoFindings(self) -> None:
        self.assertEqual(catalog.evaluate(self.store["extensions"], self.store["catalog_policy"]), {"ok": True, "findings": []})

    def testCatalog_whenDisabledCardDeclaresUnsafeCapabilities_reportsDeclarations(self) -> None:
        entries = copy.deepcopy(self.store["extensions"])
        entries[2]["capabilities"] = ["clipboard.read", "unlisted.action"]
        result = catalog.evaluate(entries, self.store["catalog_policy"])
        self.assertFalse(result["ok"])
        self.assertEqual({item["rule"] for item in result["findings"]}, {"banned_capability", "unknown_capability"})

    def testCatalog_whenDuplicateAndInvalidTypes_reportsAllRules(self) -> None:
        entry = copy.deepcopy(self.store["extensions"][0])
        entry["enabled"] = 1
        entry["update_source"] = "https://updates.dovetailmoss.test/updates"
        result = catalog.evaluate([entry, copy.deepcopy(entry)], self.store["catalog_policy"])
        self.assertEqual({item["rule"] for item in result["findings"]}, {"duplicate_id", "invalid_enabled", "update_source"})

    def testCapability_whenStudioRequestsDeclaredOperation_allowsOperation(self) -> None:
        self.assertTrue(capabilities.decide(self.store["extensions"][0], self.store["profiles"]["studio"], {"capability": "palette.write"})["ok"])

    def testCapability_whenDeniedUndeclaredOrDisabled_deniesOperation(self) -> None:
        for index, profile, capability in [(0, "kiosk", "palette.write"), (1, "studio", "palette.write"), (2, "studio", "canvas.read"), (0, "studio", None)]:
            with self.subTest(extension=index, profile=profile):
                request = {"capability": capability, "allow": ["palette.write"], "deny": []}
                self.assertFalse(capabilities.decide(self.store["extensions"][index], self.store["profiles"][profile], request)["ok"])

    def testPreferences_whenOverridden_preservesValuesLocksAndInputs(self) -> None:
        overrides = {"appearance": {"contrast": "normal", "scale": 0, "show_grid": False}, "pinned": [], "recent_limit": 0, "telemetry": True}
        before = copy.deepcopy((self.store["defaults"], overrides, self.store["locked"]))
        result = preferences.merge(self.store["defaults"], overrides, self.store["locked"])
        self.assertEqual(result["preferences"], {"appearance": {"contrast": "high", "scale": 0, "show_grid": False}, "pinned": [], "recent_limit": 0, "telemetry": False})
        self.assertEqual((self.store["defaults"], overrides, self.store["locked"]), before)
        result["preferences"]["pinned"].append("another-card")
        self.assertEqual(overrides["pinned"], [])

    def testPreferences_whenUnknownOrWrongType_rejectsOverride(self) -> None:
        for overrides in [{"appearance": {"theme": "dark"}}, {"recent_limit": True}, {"appearance": []}, {"telemetry": 0}]:
            with self.subTest(overrides=overrides):
                self.assertFalse(preferences.merge(self.store["defaults"], overrides, self.store["locked"])["ok"])

    def testSnapshot_whenDiagnosticConsent_selectsOnlyLogsWithoutContents(self) -> None:
        result = support.preview(self.store["snapshot_files"], ["diagnostic"], self.store["snapshot_limits"])
        self.assertEqual(result["files"], ["logs/startup.txt", "logs/crash.txt"])
        self.assertEqual(result["total_bytes"], 380)
        self.assertNotIn("Renderer ready", json.dumps(result))
        self.assertNotIn("content", json.dumps(result))

    def testSnapshot_whenBudgetExceeded_keepsLaterSmallerEntry(self) -> None:
        files = [{"path": f"logs/{name}", "category": "diagnostic", "bytes": size} for name, size in [("first", 700), ("large", 200), ("last", 100)]]
        result = support.preview(files, ["diagnostic"], self.store["snapshot_limits"])
        self.assertEqual(result["files"], ["logs/first", "logs/last"])
        self.assertEqual(result["total_bytes"], 800)
        self.assertEqual(len(result["skipped"]), 1)

    def testSnapshot_whenUnsafePathsOrSizesProvided_skipsInvalidEntries(self) -> None:
        files = [{"path": path, "category": "diagnostic", "bytes": size} for path, size in [("logs-old/a", 1), ("/logs/a", 1), ("logs/../a", 1), ("logs\\a", 1), ("logs/bool", True), ("logs/negative", -1), ("logs/text", "2"), ("logs/empty", 0)]]
        result = support.preview(files, ["diagnostic"], self.store["snapshot_limits"])
        self.assertEqual(result["files"], ["logs/empty"])
        self.assertEqual(result["total_bytes"], 0)
        self.assertEqual(len(result["skipped"]), 7)

    def testBackup_whenModesSelected_returnsSeparateExpectedTotals(self) -> None:
        for mode, expected_total, expected_paths in [("cloud", 120, ["catalog/cards.json", "appearance.xml"]), ("transfer", 200, ["appearance.xml", "catalog.db"])]:
            with self.subTest(mode=mode):
                result = mobile.review(storage.backup_rules(), self.store["mobile_inventory"], mode)
                self.assertEqual(result["total_bytes"], expected_total)
                self.assertEqual([item["path"] for item in result["files"]], expected_paths)

    def testBackup_whenNoIncludes_selectsNoncacheBeforeExcludes(self) -> None:
        rules = '<data-extraction-rules><cloud-backup><exclude domain="file" path="catalog/private/"/></cloud-backup></data-extraction-rules>'
        result = mobile.review(rules, self.store["mobile_inventory"], "cloud")
        self.assertEqual(result["total_bytes"], 302)
        self.assertNotIn("cache", {item["domain"] for item in result["files"]})

    def testBackup_whenDomainWideIncludeAndExactExclude_excludeWins(self) -> None:
        rules = '<data-extraction-rules><cloud-backup><include domain="file" path="."/><exclude domain="file" path="catalog/cards.json"/><include domain="cache" path="."/></cloud-backup></data-extraction-rules>'
        result = mobile.review(rules, self.store["mobile_inventory"], "cloud")
        self.assertEqual(result["files"], [{"domain": "file", "path": "catalog/private/key.json"}])
        self.assertEqual(result["total_bytes"], 32)

    def testBackup_whenRulesOrModeInvalid_rejectsExperiment(self) -> None:
        for rules, mode in [("broken", "cloud"), ("<data-extraction-rules/>", "cloud"), (storage.backup_rules(), "both")]:
            with self.subTest(rules=rules, mode=mode):
                self.assertFalse(mobile.review(rules, self.store["mobile_inventory"], mode)["ok"])
