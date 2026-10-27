"""Run each review case through the AI draft and the corrected handler. Run from workspace/: python3 -B review/compare_draft_vs_fixed.py"""
import copy, importlib.util, json, pathlib, sys
ws = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ws))
from extension_catalog import preferences as fixed, storage
spec = importlib.util.spec_from_file_location("draft", ws / "review" / "preferences_ai_draft.py")
draft = importlib.util.module_from_spec(spec); spec.loader.exec_module(draft)
store = storage.load()
for path in sorted((ws / "review").glob("case*.json")):
    overrides = json.loads(path.read_text())["overrides"]
    before = copy.deepcopy((store["defaults"], overrides, store["locked"]))
    print(f"== {path.name}  overrides={json.dumps(overrides)}")
    for name, mod in (("draft", draft), ("fixed", fixed)):
        out = mod.merge(store["defaults"], overrides, store["locked"])
        print(f"  {name}: {json.dumps(out, sort_keys=True)}")
    assert (store["defaults"], overrides, store["locked"]) == before, "input mutated"
print("inputs unchanged: OK")
