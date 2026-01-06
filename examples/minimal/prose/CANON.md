# CANON (Prose)

**Governance for prose state.**

**Inherits from:** [../../CANON.md](../../CANON.md)

---

## Constraints

### Dependencies

- ../assets/LEDGER.md must exist

### Content constraints

- May only reference registered assets (asset-NNNN format)
- All asset references must resolve to LEDGER entries

### Validation

- Extract all asset-NNNN references
- Verify each exists in LEDGER
- Block output if unregistered references found

---

End prose CANON.
