# Examples

**CANONIC FSM demonstrations showing the 4-state machine in action.**

This directory contains self-contained examples of the FSM (Episodes → Assets → Prose → Output).

---

## Available Examples

### minimal/
The simplest complete FSM implementation.
- Demonstrates: All 4 states with minimal content
- Shows: Episode extraction, asset registration, prose composition, output validation
- Use case: Learning the FSM structure

---

## How to Use Examples

Each example is self-contained:

1. **Read the README** — Understand what it demonstrates
2. **Check the CANON** — See state-specific constraints
3. **Explore the states** — See episodes/, assets/, prose/, output/
4. **Observe the flow** — How raw input becomes validated output

---

## Example Structure

Every example follows the FSM pattern:

```
example-name/
├── CANON.md              # Example-level governance
├── VOCABULARY.md         # Example-specific terms
├── README.md             # What this demonstrates
├── episodes/             # Raw input (ungoverned)
│   ├── CANON.md
│   ├── VOCABULARY.md
│   ├── README.md
│   └── 001-*.md
├── assets/               # Registered entities
│   ├── CANON.md
│   ├── VOCABULARY.md
│   ├── README.md
│   └── LEDGER.md
├── prose/                # Composed content
│   ├── CANON.md
│   ├── VOCABULARY.md
│   ├── README.md
│   └── draft.md
└── output/               # Validated artifacts
    ├── CANON.md
    ├── VOCABULARY.md
    ├── README.md
    └── METADATA.md
```

---

## Learning Path

**Start with:** [minimal/](minimal/) — The complete FSM in its simplest form

**Understand:**
- How episodes remain ungoverned
- How assets get extracted and registered
- How prose references only registered assets
- How validation gates output

---

## Creating Your Own

To create an FSM based on these examples:

1. Copy the `minimal/` directory structure
2. Write your episodes (raw observations)
3. Extract assets (identify entities)
4. Compose prose (reference assets)
5. Validate (output exists when compliant)

---

## Notes

Examples are intentionally minimal to demonstrate structure, not complexity.

For real-world applications, see [canonic-machine/writing](https://github.com/canonic-machine/writing).

---

End of examples README.
