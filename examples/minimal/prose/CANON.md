# CANON (Prose)

**Governance for prose state.**

**Inherits from:** [../../CANON.md](../../CANON.md)

---

## Constraints

### Dependencies

- ../assets/LEDGER.md must exist

**Violation:** Prose exists but assets/LEDGER.md missing

### Content constraints

- May only reference registered assets (asset-NNNN format)
- All asset references must resolve to LEDGER entries

**Violation:** Prose references unregistered asset

### Validation

- Extract all asset-NNNN references
- Verify each exists in LEDGER
- Block output if unregistered references found

**Violation:** Prose contains unresolved asset references

---

End prose CANON.
