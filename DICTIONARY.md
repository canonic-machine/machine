# DICTIONARY (Root)

**Alphabetically ordered MACHINE-specific term definitions.**

Inherits core CANONIC terms from canonic-machine/canonic.

---

## Core Terms

### backflow
Returning to an earlier state when validation fails. Only allowed on failure.

### FSM
Finite State Machine. A system with discrete states and defined transitions between them. The MACHINE is a specific 4-state FSM.

### MACHINE
The CANONIC FSM engine. A domain-agnostic 4-state finite state machine (Episodes → Assets → Prose → Output) that transforms raw input into validated output through governed transitions.

### state
A discrete stage in the FSM with specific constraints and artifacts. The 4-state FSM has: episodes, assets, prose, output.

### transition
Movement from one state to another, governed by validation gates.

### validation gate
A pass/fail check that determines if transition to next state is allowed.

---

## State Definitions

### asset
Registered entity with stable identity. Extracted from episodes, tracked in ledger, referenced by prose.

### episode
Raw domain input. Ungoverned content that supplies meaning to the system. Source material for extraction.

### output
Final validated artifact. Only exists when all validation passes. Immutable until next cycle.

### prose
Composed content that references registered assets. The narrative or structured layer built on assets.

---

## Process Concepts

### composition
The process of creating prose that references registered assets.

### extraction
The process of identifying entities in episodes and registering them as assets.

### ledger
Single source of truth for all registered assets. Typically LEDGER.md in assets/.

### reference resolution
Verifying that all asset references in prose point to registered assets in the ledger.

### registration
Adding an entity to the asset ledger with unique ID and source traceability.

### source traceability
The property that every asset can be traced back to the episode it came from.

---

## Lifecycle Concepts

### compliant
State of passing all validation checks. Output can only exist when system is compliant.

### immutability
The property that an artifact cannot be changed once set. Episodes become immutable after extraction. Assets IDs are always immutable.

### REINDEX
A protocol for controlled exception to immutability. Creates REINDEX.md, suspends immutability, allows coordinated changes, then deletes REINDEX.md to restore enforcement.

### violation
A failed validation check. Blocks transition to next state.

---

## Domain Concepts

### domain application
A MACHINE implementation specialized for a specific domain. Named by domain only (WRITING, DOCUMENTATION, RESEARCH). Inherits all MACHINE constraints and adds domain-specific specializations.

### domain-agnostic
The property that the FSM works across different use cases: writing, documentation, research, knowledge management.

### domain-sourced
Content that comes from the specific domain being modeled (lived experiences for writing, requirements for documentation, observations for research).

---

## Nomenclature

### Naming Convention
- **Paradigm**: CANONIC (all caps, the root)
- **Engine**: MACHINE (all caps, the FSM)
- **Applications**: Domain name only (WRITING, DOCUMENTATION, RESEARCH)

**Principle:** Inheritance is explicit in CANON statements, not repeated in terminology.

**Violation:** Naming an application "DOMAIN MACHINE" when it already inherits from MACHINE.

---

End of root DICTIONARY.
