# CANON (Output)

**Governance for output state.**

**Inherits from:** [../../CANON.md](../../CANON.md)

---

## Constraints

### Existence condition

Output only exists when all validation passes:
- All asset references in prose resolve to LEDGER
- No REINDEX.md in any state
- All dependencies satisfied

**Violation:** Output exists despite validation failures or active REINDEX

### Required artifacts

- METADATA.md (validation record)

**Violation:** Output missing METADATA.md

### Immutability

Output is immutable once generated.

**Violation:** Output artifact modified after generation

---

End output CANON.
