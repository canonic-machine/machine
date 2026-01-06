# Minimal Example

A minimal CANONIC FSM example using API documentation as the domain.

## Structure

```
minimal/
├── episodes/      # Raw requirements (ungoverned)
├── assets/        # Extracted API entities (governed)
├── prose/         # Documentation draft (governed)
└── output/        # Validated output (immutable)
```

## The Flow

1. **Episode 001** contains raw requirements for a user API
2. **Assets** extracted: 5 endpoints, 1 entity, 3 fields, 1 validation rule
3. **Prose** composes documentation referencing assets (e.g., asset-0001)
4. **Output** exists because all references resolve to LEDGER

## Domain-Agnostic Nature

This example uses API documentation, but the same FSM works for:
- **Writing:** episodes → characters/places → narrative → book
- **Research:** observations → variables → analysis → paper
- **Knowledge:** notes → concepts → summaries → wiki

The 4-state structure stays the same. Only the asset types change.

## Governance

Each directory has the triad (CANON, VOCABULARY, README). Each state enforces constraints.

See parent [CANON.md](../CANON.md) for FSM rules.
