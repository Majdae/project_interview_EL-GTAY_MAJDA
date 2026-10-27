# Review of the AI-drafted preference merge (policy rev. 3)

**Bottom line:** `extension_catalog/preferences.py` is rewritten and usable. Public tests: 17/17 pass (2 failed before). Same `preferences` JSON interface; defaults, locks, tests and fixtures untouched.

## One verified correction (lock bypass)
The draft applied locks to the defaults *first* and the user's overrides *after*, so users could override locks. Policy: locks apply last.

Reproduce: `python3 -B cli.py review/case1_lock_bypass.json`
Input: `{"telemetry": true, "appearance": {"contrast": "normal"}}`

| | telemetry | contrast |
|---|---|---|
| Draft | **true** | normal |
| Corrected | **false** | high |

`python3 -B review/compare_draft_vs_fixed.py` runs all four cases through both versions (draft kept as `review/preferences_ai_draft.py`). Other draft faults it also shows: it dropped unrelated nested settings (`scale`, `show_grid`), ignored real `false`/`0`/`[]` values, appended lists instead of replacing them, and accepted unknown nested keys (`appearance.theme`).

## What the AI review sentence gets wrong
Draft claim: "The locked configuration proves telemetry cannot run and the operating system is isolated."

- Even as a *configuration* statement the draft code contradicted it (case 1 above).
- With the corrected merge, what is established: for the saved defaults and locks, the merged preference object always has `telemetry: false` and `contrast: "high"`, whatever valid overrides are supplied.
- Not established: this desk never applies settings, runs the app, reads the OS, or checks that any component honors the flag. So "telemetry cannot run" and "OS is isolated" are unsupported. Fair wording: "the saved preference policy keeps telemetry set to false."
- Also untested: who may submit overrides (no identity model), persistence, or other code paths that might send data.
