# Archive

Documents that have been **superseded as governing doctrine**. Preserved here
for historical reference and for line-by-line salvage when active doctrine
needs to migrate fragments forward.

## Convention

- A file lands here when it is no longer the live operating doctrine.
- The file is **not deleted** because git history alone is awkward to browse,
  and salvage passes need direct access to the obsolete source.
- New work must **not** cite or extend files in `archive/` as authoritative.
  If a fragment is still useful, migrate it into the current v3.2.2 doctrine
  stack (e.g. `briefs/p-sri-v322-build-design-v1.md`,
  `briefs/p-ab3-ruleset-v1.md`) and reference the new home.

## How a file gets archived

1. Cyler or Gavin tags it as superseded / obsolete.
2. Archie moves the file to `briefs/archive/` (single canonical copy if the
   original had case-collision duplicates).
3. The active `briefs/` location is deleted in the same commit pair.
4. If salvage is needed, a separate `briefs/<name>-salvage-source-<date>.md`
   captures uncommitted edits worth migrating, and is removed once salvage
   is complete.

## Current contents

| File | Superseded by | Archived |
|---|---|---|
| `Allocation-Bucket-Framework-v2.0.md` | v3.2.2 framework (`p-sri-v322-build-design-v1.md`, AB4-as-benchmark-anchor model) | 2026-05-01 |
