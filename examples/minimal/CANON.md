# CANON (examples/minimal/)

**Governance for the minimal FSM example.**

**Inherits from:** [../../00-CANON.md](../../00-CANON.md), [../00-CANON.md](../00-CANON.md)

This is the simplest complete implementation of the 4-state FSM.

---

## Purpose

Demonstrate the minimal viable FSM structure with one episode, one asset, minimal prose, and validated output.

---

## Invariants

### FSM Structure

All 4 states must exist:
- episodes/ (with at least one episode file)
- assets/ (with LEDGER.md)
- prose/ (with draft.md)
- output/ (with validated artifact when compliant)

**Violation:** Missing required FSM state directory

### Traceability

- All assets trace to episode 001
- All prose references trace to registered assets
- Output only exists when validation passes

**Violation:** Asset or prose reference lacks traceable source

---

## State Constraints

Inherits state constraints from root CANON.md.

This example demonstrates the constraints in minimal form.

---

## Validation

Minimal example validation:
- Episode 001 exists
- At least one asset registered
- Prose references the registered asset
- Output exists only when compliant

---

End of minimal CANON.
