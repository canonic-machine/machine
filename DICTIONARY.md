# DICTIONARY (Root)

**Alphabetically ordered MACHINE-specific term definitions.**

Inherits core CANONIC terms from canonic-machine/canonic.

---

## Validation Concepts

### backflow
Returning to an earlier state when validation fails. Only allowed on failure.

### canon-awareness
The property that validators derive rules from CANON.md dynamically rather than hardcoding constraints.

### compliance
State of passing all validation checks.

### constraint checking
The process of verifying that artifacts satisfy requirements defined in CANON.md.

### reference integrity
Verifying that all references resolve correctly across the artifact tree.

### semantic validation
LLM-powered deep validation checking coherence, completeness, and canon alignment.

### syntactic validation
Fast, deterministic validation checking structure, format, and naming conventions.

### validation gate
A pass/fail check that determines if transition to next state is allowed.

### violation
A failed validation check that blocks transition to next state.

---

## FSM Infrastructure

### FSM
Finite State Machine. A system with discrete states and defined transitions between them. Domain applications define their own FSMs.

### state
A discrete stage in an FSM with specific constraints and artifacts. State names are domain-specific.

### state transition
Movement from one state to another, governed by validation gates.

---

## Git-FSM Concepts

### atomic commit
A git commit containing one logical change addressing one constraint.

### consumer commit
A commit that applies canonical constraints or fixes violations. Uses "Apply" or "Fix" prefix.

### git-FSM
The implementation pattern where git commits are FSM state transitions with validation acting as gates.

### producer commit
A commit that canonifies new patterns or constraints. Uses "Canonify" prefix.

### producer ratio
The percentage of commits that are producer (canonification) vs consumer (application). Indicates system maturity phase.

---

## Self-Properties

### self-healing
The property that the system detects violations through git history patterns and triggers recovery.

### self-measuring
The property that the system measures its own maturity through git commit analysis.

### self-strengthening
The property that the system improves through git-based introspection cycles and recursive canonification.

---

## Repository Concepts

### domain application
A repository that inherits from MACHINE and implements a domain-specific FSM. Examples: WRITING, DOCUMENTATION, RESEARCH.

### governance repository
A repository that defines canonical constraints without implementation. Must include examples directory. Only CANONIC is governance.

### validation engine
The layer that implements constraint checking, reference integrity, and FSM infrastructure without domain-specific patterns.

---

End of root DICTIONARY.
