"""Stable examples and JSON transport smoke checks."""
from __future__ import annotations
import json
import pathlib
import subprocess
import sys
import unittest
from extension_catalog import storage

class SmokeTests(unittest.TestCase):
    def testSetup_whenRun_printsReady(self) -> None:
        result = subprocess.run([sys.executable, "-B", "setup.py"], capture_output=True, text=True, check=True)
        self.assertIn("Ready:", result.stdout)

    def testExamples_whenRun_returnJsonObjects(self) -> None:
        for path in sorted(pathlib.Path("examples").glob("*.json")):
            with self.subTest(example=path.name):
                result = subprocess.run([sys.executable, "-B", "cli.py", str(path)], capture_output=True, text=True, check=True)
                self.assertIsInstance(json.loads(result.stdout), dict)

    def testStorage_whenLoaded_hasNamedCards(self) -> None:
        store = storage.load()
        self.assertEqual({item["extension_id"] for item in store["extensions"]}, {"inkframe", "rulerleaf", "duskswatch"})
