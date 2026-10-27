# CHOICES

**Built:** Replaced `preferences.py` (rewrite beat patching: the draft's order was wrong, not just a line). It validates overrides against defaults (unknown keys at any depth reject; exact JSON type, so bool is not int), merges dicts, replaces lists, keeps false/0, then applies locks last at every depth on a copy. Inputs are never mutated. `review/` holds four small requests, a draft-vs-fixed comparison script, and `REVIEW_FOR_IZEL.md`.

**Left out:** other actions (catalog, snapshot, backup), element-type checks inside lists (policy only says lists replace), persistence.

**Assumptions:** a lock key absent from defaults is still applied; a lock dict over a non-dict value is replaced by the lock; reason wording is free.

**Checked:** original 17 tests pass (2 failed before); CLI run on all examples; draft vs fixed on four cases; deepcopy comparison confirms inputs unchanged.

**AI output corrected:** the draft review claim that locks "prove telemetry cannot run and the OS is isolated". Local case 1 shows the draft let `telemetry: true` through, and the desk applies nothing to a real system.

**Next step:** have Sena confirm the wording, and add review cases to the test suite.
