# PATTERNS

Orchestrated protocol compositions for common use cases.

Patterns combine atomic protocols from PROTOCOLS.md into reusable templates.

---

## Pattern Architecture

```mermaid
graph TB
    subgraph Atomic[Atomic Protocols]
        immut[immutability]
        unique[uniqueness]
        trace[traceability]
        refprot[reference_protection]
        valid[validation]
        reindex[reindex]
    end

    subgraph Patterns[Orchestrated Patterns]
        registry[registry_entity_pattern]
        ledger[ledger_pattern]
        fsm[fsm_state_pattern]
        reindexable[reindexable_artifact_pattern]
    end

    immut --> registry
    unique --> registry
    trace --> registry
    refprot --> registry

    registry --> ledger
    valid --> ledger

    valid --> fsm
    immut --> fsm
    reindex --> fsm

    immut --> reindexable
    reindex --> reindexable
    valid --> reindexable
```

**Figure PT-1: Patterns compose atomic protocols for common scenarios.**

Each pattern provides a ready-to-use template for specific artifact types.

---

## registry_entity_pattern

**Purpose:** Standard pattern for ledger entries (assets, references, etc.)

**Composition:**

```mermaid
graph LR
    RE[registry_entity] --> IM[immutability_protocol]
    RE --> UQ[uniqueness_protocol]
    RE --> TR[traceability_protocol]
    RE --> RP[reference_protection_protocol]

    IM -.applies to.-> ID[id field]
    IM -.applies to.-> SRC[source field]
    UQ -.applies to.-> ID
    TR -.applies to.-> SRC
    RP -.applies to.-> ENT[entity itself]
```

**Figure PT-2: Registry entity pattern ensures stable, traceable, protected entries.**

---

### Protocol Composition

**Applies:**
1. `immutability_protocol` on:
   - id field
   - source field

2. `uniqueness_protocol` on:
   - id field

3. `traceability_protocol` on:
   - source field → source location

4. `reference_protection_protocol` on:
   - entity (cannot delete if referenced)

---

### Usage Example

```markdown
assets/CANON.md

Asset entries use: registry_entity_pattern

Parameters:
- id field: id
- id format: asset-NNNN
- source field: source_episode
- source location: ../episodes/
- referenced_by: ../prose/
```

**This single line applies 4 protocols with specific parameters.**

---

### What It Guarantees

✓ IDs never change
✓ IDs are unique
✓ Source always traces to existing episode
✓ Cannot delete if prose references it

---

## ledger_pattern

**Purpose:** Complete pattern for registry files (LEDGER.md, indexes, catalogs)

**Composition:**

```mermaid
graph TB
    LP[ledger_pattern] --> REP[registry_entity_pattern]
    LP --> SEQ[sequential_protocol]
    LP --> STR[structured_protocol]
    LP --> VAL[validation_protocol]

    REP --> Entries[Applies to: All entries]
    SEQ --> Entries
    STR --> Entries
    VAL --> File[Applies to: Ledger file]
```

**Figure PT-3: Ledger pattern adds sequencing and structure to registry entities.**

---

### Protocol Composition

**Inherits:** `registry_entity_pattern` for all entries

**Adds:**
1. `sequential_protocol`:
   - Entries numbered sequentially
   - No gaps allowed

2. `structured_protocol`:
   - Required fields enforced
   - Optional fields allowed
   - Unknown fields rejected

3. `validation_protocol`:
   - All protocols checked on save
   - Reports violations with locations

---

### Usage Example

```markdown
assets/CANON.md

LEDGER.md uses: ledger_pattern

Entry structure:
- id: asset-NNNN (sequential, starting 0001)
- name: string
- type: person|place|object|claim|concept|event
- source_episode: NNN
- notes: string (optional)
```

---

### What It Guarantees

✓ All guarantees from registry_entity_pattern
✓ Sequential numbering (asset-0001, 0002, 0003...)
✓ Structured entries (required fields present)
✓ Continuous validation

---

## fsm_state_pattern

**Purpose:** Pattern for FSM state directories (episodes/, prose/, output/)

**Composition:**

```mermaid
stateDiagram-v2
    [*] --> State

    State --> Validation: on save
    Validation --> Valid: all checks pass
    Validation --> Invalid: checks fail

    Valid --> NextState: may advance
    Invalid --> State: must fix

    state State {
        [*] --> CheckDeps
        CheckDeps --> CheckMut
        CheckMut --> CheckReindex
        CheckReindex --> [*]
    }
```

**Figure PT-4: FSM state pattern validates dependencies, mutations, and reindex status.**

---

### Protocol Composition

**Applies:**
1. `dependency_protocol`:
   - Cannot advance without upstream satisfied
   - Example: prose needs assets + structure

2. `mutation_protocol`:
   - Defines what can/cannot change
   - Mutable vs immutable fields

3. `validation_protocol`:
   - Entry validation
   - Dependency checks
   - Mutation checks

4. `reindex_protocol` (conditional):
   - Available if state needs reindexing
   - Example: episodes after extraction

---

### Usage Example

```markdown
prose/CANON.md

Prose state uses: fsm_state_pattern

Dependencies:
- ../assets/LEDGER.md (must exist)
- ../structure/outline.md (must exist)

Mutations:
- Always mutable (prose is editable)

Validation:
- asset_references_resolve
- structure_compliance

Reindex: optional (for major rewrites)
```

---

### What It Guarantees

✓ Cannot advance without dependencies
✓ Clear mutation rules
✓ Validated on every save
✓ Reindex available when needed

---

## reindexable_artifact_pattern

**Purpose:** Artifacts that are normally immutable but can be reindexed

**Composition:**

```mermaid
stateDiagram-v2
    [*] --> Mutable
    Mutable --> Immutable: extraction/first use
    Immutable --> Mutable: REINDEX.md created
    Mutable --> Immutable: REINDEX.md deleted

    Immutable --> Blocked: edit attempted
    Blocked --> Immutable: edit rejected

    state Mutable {
        [*] --> Editable
        Editable --> Saved
        Saved --> [*]
    }

    state Immutable {
        [*] --> Frozen
        Frozen --> ValidationFails: edit rejected
        ValidationFails --> [*]
    }
```

**Figure PT-5: Reindexable artifacts toggle between mutable (REINDEX active) and immutable (normal).**

---

### Protocol Composition

**Applies:**
1. `immutability_protocol`:
   - Default state: immutable
   - Exception: REINDEX.md present

2. `reindex_protocol`:
   - Procedure for controlled mutation
   - Suspends immutability while active
   - Blocks output

3. `validation_protocol`:
   - Checks immutability (unless REINDEX)
   - Checks REINDEX documentation complete
   - Checks downstream updated after REINDEX

---

### Usage Example

```markdown
episodes/CANON.md

Episodes use: reindexable_artifact_pattern

Immutability trigger: Assets extracted from episode

Reindex requirements:
- Document reason
- List changes
- Note downstream impacts (assets, prose)
- Update status checklist

Validation:
- File naming
- Sequential numbering
- Immutability (unless REINDEX active)
```

---

### What It Guarantees

✓ Immutable by default (preserves traceability)
✓ Controlled mutation via REINDEX
✓ Output blocked during REINDEX
✓ Validated on completion

---

## Pattern Selection Guide

```mermaid
graph TD
    Start{What are you governing?}

    Start -->|Ledger entries| Registry{Need full ledger?}
    Registry -->|Yes| UseLedger[Use: ledger_pattern]
    Registry -->|No, just entries| UseRegistry[Use: registry_entity_pattern]

    Start -->|FSM state| StateType{What kind?}
    StateType -->|Needs reindexing| UseReindex[Use: reindexable_artifact_pattern]
    StateType -->|Always mutable| UseFSM1[Use: fsm_state_pattern<br/>mutation: always]
    StateType -->|Immutable output| UseFSM2[Use: fsm_state_pattern<br/>mutation: none]

    Start -->|Custom| Manual[Compose atomic<br/>protocols manually]
```

**Figure PT-6: Decision tree for selecting the right pattern.**

---

## Extending Patterns

Create new patterns by composing atomic protocols:

```markdown
my_custom_pattern:
  = base_pattern
  + additional_protocol_1
  + additional_protocol_2
  - removed_protocol (if overriding)
```

Example:

```markdown
versioned_ledger_pattern:
  = ledger_pattern
  + version_protocol (track ledger versions)
  + snapshot_protocol (preserve history)
```

---

## AI Interprets, Humans Decide

**AI interprets patterns:**
- Recognizes pattern names
- Applies composed protocols
- Validates according to rules

**Humans decide patterns:**
- Which pattern fits the use case
- What parameters to provide
- When to create custom patterns

Patterns make the AI's job easier while keeping humans in control.

---

End PATTERNS.
