# CANON (Assets)

**Governance for asset state.**

**Inherits from:** [../../CANON.md](../../CANON.md)

---

## Constraints

### Required artifacts

- LEDGER.md (single source of truth)

**Violation:** LEDGER.md missing from assets state

### Asset structure

Each asset must have:
- id: asset-NNNN (sequential, immutable)
- name: string
- type: endpoint | field | validation | entity
- source_episode: NNN
- notes: optional

**Violation:** Asset missing required fields or uses invalid format

### Invariants

- Asset IDs are immutable
- Source episodes must exist
- Cannot delete assets referenced in prose

**Violation:** Asset ID changed, source episode missing, or referenced asset deleted

---

End assets CANON.
