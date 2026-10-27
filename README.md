# Dovetailmoss extension catalog desk

A small saved-file simulator for our desktop catalog and mobile companion. Python
3.11 or later and its standard library are enough. There is no package installation,
network, socket, background server, plugin loading or extension execution.

Run `python3 -B setup.py` before starting. Run `python3 -B -m unittest discover -s tests -v`
for the public checks. Try `python3 -B cli.py examples/capability.json`; replace the
example name with catalog, preferences, snapshot or backup for another decision.
Each invocation reloads fixtures and exits. A handled denial is JSON with `ok:false`,
not a nonzero process exit. No command changes actual desktop settings or sends data.

## Source map

Start at [docs/map.md](docs/map.md), then [docs/policy.md](docs/policy.md) for current
rules. [docs/offline-hints.md](docs/offline-hints.md) explains local investigation and
[docs/glossary.md](docs/glossary.md) defines the product terms. Fixture requests are
in examples; data is in fixtures/store.json; service dispatch is in
extension_catalog/service.py. Mobile inputs are decoded text, not an APK.

The archived policy is historical context only. Public tests are a small set of
examples and do not establish every security property. Dovetailmoss, its people,
products and demo data are fictional. A DEMO marker is never a real credential.

For the current merge review, start with [Izel’s note](docs/preference-review.md).
