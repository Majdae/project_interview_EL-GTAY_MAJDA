# Source map and people

Dovetailmoss is a fictional 18-person team making a desktop catalog of declarative
display cards. Today is 23 October 2026, 09:00 UTC+01. Izel owns product decisions;
Bram owns desktop code; Sena reviews security; Ludo owns support workflows; Neri
owns the companion mobile backup model.

| Question | Read first | Code / local example |
| --- | --- | --- |
| Are catalog declarations acceptable? | policy.md, catalog section | catalog.py / examples/catalog.json |
| May a card use a capability? | policy.md, capability section | capabilities.py / examples/capability.json |
| Which preferences win? | policy.md, preference section | preferences.py / examples/preferences.json |
| What can support receive? | policy.md, support section | support.py / examples/snapshot.json |
| What would backup select? | policy.md, backup section | mobile.py, mobile/backup_rules.xml / examples/backup.json |

All module paths above are under extension_catalog/. Storage loads fixtures/store.json.
The `action` string dispatches at service.py. Examples may supply overrides, while
omitted request fields use the fixture defaults. The explicit command JSON shapes
and response fields are in docs/interfaces.md. Baseline rules describe a correct
saved-file model, not a certification of an operating system security boundary.
