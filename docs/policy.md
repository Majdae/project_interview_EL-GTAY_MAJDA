# Current policy, revision 3 — 23 October 2026

This policy supersedes archived-policy-v1.md. All decisions are local previews.

## Catalog declarations

A card has extension_id, name, enabled, capabilities and update_source. IDs must be
unique within the evaluated list. enabled must be the JSON boolean true or false,
never a string or integer. Unknown capabilities are flagged; known-but-banned
capabilities are flagged even on disabled cards. Only bundled update declarations
are acceptable. No updater, URL fetching or card code exists in this model.

## Capability boundary

The requested capability is permitted only when the extension is enabled, declares
that capability, the named profile allows it, and that same profile does not deny it.
An explicit deny wins over allow. Unknown profiles or cards are denied. Missing or
nonstring capabilities are denied. An extension's declaration is a request for
permission and cannot grant permission by itself. Profiles are saved trusted policy;
request JSON selects a profile but cannot alter profile policy. There is no identity
or profile authentication model here, so do not claim one has been tested.

## Preferences

User overrides merge into defaults recursively for known keys. Mapping values merge;
list values replace the entire list; booleans, integers and strings replace the same
type only (a boolean is not an integer here). Unknown keys or incompatible types
reject the request with ok:false. False and zero are valid values, not missing data.
Locked policy is applied last, recursively, and always wins. Inputs remain unchanged.
The simulator does not persist or apply operating system settings.

## Support snapshot

The inventory is declared logical POSIX paths, content labels and byte counts; no
files are opened by the preview. A path must be relative, free of '..' segments,
free of backslashes, and under an allowed root such as logs/ or state/. Prefixes
have a directory boundary: logs-old/ is not logs/. Excluded exact paths are always
omitted. A file's category must be both allowed by policy and explicitly consented
by the user. Consent for diagnostic does not grant settings or personal consent.
Byte counts are nonnegative JSON integers, not booleans. In input order, skip any
entry that would exceed the cumulative budget; later smaller entries may still fit.
Output contains paths, totals and skip reasons only, never content. A snapshot
preview does not send, archive, or establish redaction of any underlying files.

## Mobile backup simulator

Use cloud-backup for mode cloud and device-transfer for mode transfer. Rules from
one mode do not carry into the other. Includes restrict the set when at least one
include exists; without includes all noncache inventory is eligible before excludes.
Domain matches exactly. Path '.' means all entries within that domain. A rule path
ending '/' matches that directory prefix; any other path is exact. Excludes win.
The cache domain is always omitted. Unknown modes, malformed XML, or missing mode
sections reject rather than report an empty safe result. Return selected domain/path
pairs and their declared byte total. mobile/manifest.xml names @xml/backup_rules;
mobile/backup_rules.xml is the decoded corresponding resource. Text rules are the
entire supplied model: no Android SDK, actual device, APK build, cloud connection,
encryption attestation or Android-version claim is part of this exercise.
