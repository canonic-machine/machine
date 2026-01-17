# MACHINE

The enforcement scope that evaluates candidate system states against governing CANON.

---

## Governance Path

`/canonic/machine/`

Inherits from: `/canonic`

---

## Purpose

MACHINE defines the execution semantics for CANONIC governance. It consumes candidate states and governing CANON, evaluates them deterministically, and produces binary accept/reject outcomes. MACHINE enforces inherited CANON only; it does not introduce, modify, or extend governance.

---

## Scope

### In scope

- Authority constraint (enforce inherited CANON only)
- Input specification (candidate states and governing CANON)
- Evaluation semantics (judge against CANON)
- Binary decision outcomes (accept or reject)
- Non-authoritative signal emission
- Determinism requirement (identical inputs yield identical outcomes)

### Out of scope

- Governance definition or modification
- Operational constraints (delegated to OS)
- Persistence semantics (delegated to LEDGER)
- Protocol definitions (delegated to downstream scopes)
- Agent behavior (delegated to downstream scopes)

---

## References

- `CANON.md`
- `VOCAB.md`
- `MACHINE.md` (SPEC)

---

*This README is descriptive and non-normative. Governance is defined exclusively by CANON.*

---
