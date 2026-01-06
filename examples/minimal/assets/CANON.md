# CANON (Assets)

**Governance for asset state.**

**Inherits from:** [../../CANON.md](../../CANON.md)

---

## Constraints

### Required artifacts

- LEDGER.md (single source of truth)

### Asset structure

Each asset must have:
- id: asset-NNNN (sequential, immutable)
- name: string
- type: endpoint | field | validation | entity
- source_episode: NNN
- notes: optional

### Invariants

- Asset IDs are immutable
- Source episodes must exist
- Cannot delete assets referenced in prose

---

End assets CANON.
