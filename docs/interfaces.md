# Local JSON interfaces

`python3 -B cli.py <request.json>` reads one JSON object and prints one JSON object.
The examples are small working requests. Fields not mentioned below are ignored by
dispatch; choose an action and inspect its result rather than assuming exit status.

- catalog: optional entries list replaces the fixture cards for this decision.
  Result: ok and findings, each containing extension_id and rule.
- capability: extension_id, profile and capability strings. Result: ok and reason.
  No request field can supply trusted profile allow or deny lists.
- preferences: optional overrides object. Result: ok and preferences, or reason on
  rejection. Defaults and locks come from the fixture store.
- snapshot: optional files list and consent string list. Each inventory record has
  path, category, bytes and illustrative content. Result: ok, files (path strings),
  total_bytes and skipped (path/reason records). Content must never appear in output.
- backup: mode cloud or transfer, optional policy_xml string and inventory list.
  Each inventory record has domain, path and bytes. Result: ok, files (domain/path
  objects) and total_bytes, or reason on rejection. An explicit policy_xml replaces
  the decoded resource only for the local experiment.

Modules expose catalog.evaluate(entries, policy), capabilities.decide(extension,
profile, request), preferences.merge(defaults, overrides, locked),
support.preview(files, consent, limits), mobile.review(policy_xml, inventory, mode).
All return JSON-compatible dictionaries. See models.py for the shared type alias.
