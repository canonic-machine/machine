---

## Canonification Log

### No Orphaned or Empty Section Headers Invariant

**[Description of what must be true]:**
- Downstream CANONs must not include empty, orphaned, or placeholder section headers (e.g., '## Invariants' with no content).
- All section headers must be followed by substantive content or be removed.

**Violation:**
- CANON.md contains empty or orphaned section headers.
---

# CANON (Root)

**Governance for the CANONIC FSM engine.**

**Inherits from:** [canonic-machine/canonic](https://github.com/canonic-machine/canonic)

Cross-repository inheritance is declarative (markdown links only). No git submodules, no scripts, no tooling.

This CANON defines the 4-state FSM: Episodes → Assets → Prose → Output.
---

## Invariants
### The Triad

All directories must maintain the triad:
- CANON.md defines constraints
- VOCABULARY.md defines terms used in CANON and README

### FSM Structure
The FSM consists of exactly four states:
- **episodes/** — Raw input (ungoverned)
- **assets/** — Registered entities (governed, immutable)
- **prose/** — Composed content (governed, mutable)
- **output/** — Validated artifacts (governed, immutable)

### State Transitions

Transitions are unidirectional with validation gates:
- Episode → Asset: Extraction (registers entities)
- Asset → Prose: Composition (references assets)
- Prose → Output: Validation (compliance gate)

Backflow allowed only on validation failure:
- Output validation fails → return to Prose
- Asset validation fails → return to Episodes

---

## State Constraints

### Episodes State

**Purpose:** Raw domain input (ungoverned)

**Required files:**
- Triad (CANON, VOCABULARY, README)
- Episode files (sequential, format: NNN-*.md)

**Content constraints:**
- Domain-sourced (human observations, requirements, notes)
- Any format allowed (prose, bullets, fragments)
- Contradictions and uncertainty permitted
- No asset references or structure required

**Lifecycle:**
- Immutable after asset extraction
- REINDEX to modify if needed

**Protocol:** reindexable_artifact_pattern

### Assets State

**Purpose:** Registered entities with stable identity

**Required files:**
- Triad (CANON, VOCABULARY, README)
- LEDGER.md (single source of truth)

**Asset structure:**
- id: unique identifier (immutable)
- name: human-readable label
- type: entity classification
- source_episode: traceability to episode
- notes: optional context

**Registration:**
1. Extract from episodes
2. Check duplicates
3. Assign sequential ID
4. Record source
5. Update LEDGER

**Invariants:**
- IDs immutable
- Source must exist
- No orphaned assets
- Cannot delete if referenced in prose

**Protocol:** ledger_pattern

### Prose State

**Purpose:** Composed content

**Required files:**
- Triad (CANON, VOCABULARY, README)
- Content files (draft.md or domain-specific)

**Dependencies:**
- LEDGER.md must exist
- Structure specification must exist (if used)

**Content constraints:**
- May only reference registered assets
- Asset references must use registered names/IDs
- All references must resolve to LEDGER entries

**Lifecycle:**
- Always mutable (prose is editable)
- REINDEX for major restructuring (optional)

**Protocol:** fsm_state_pattern

### Output State

**Purpose:** Final validated artifact

**Required files:**
- Triad (CANON, VOCABULARY, README)
- Output files (generated on compliance)
- METADATA.md (validation timestamp)

**Generation:**
- Only exists when all validation passes
- Blocked by any REINDEX.md in system
- Immutable until next edit cycle

**Validation:**
- All asset references resolve
- Structure compliance (if specified)
- No violations in any state

**Protocol:** fsm_state_pattern (mutation: none)

---

## Transition Rules

### Episode → Asset

**Trigger:** Extraction decision

**Requirements:**
- Episode file exists
- Entities identified
- No duplicate registrations

**Validation:**
- Asset IDs sequential
- Source episode recorded
- LEDGER updated

### Asset → Prose

**Trigger:** Composition begins

**Requirements:**
- LEDGER.md exists
- At least one asset registered

**Validation:**
- All prose references resolve to LEDGER
- No unregistered entities

### Prose → Output

**Trigger:** Validation gate

**Requirements:**
- All states compliant
- No REINDEX.md anywhere
- All dependencies satisfied

**Validation:**
- Asset references valid
- Structure compliance (if specified)
- No violations

**Output:**
- Generate output files
- Create METADATA.md
- Mark timestamp

---

## REINDEX Protocol

**Scope:** Any state directory

**Trigger:** Immutability violation needed

**Procedure:**
1. Create REINDEX.md in scope
2. Document: reason, changes, impacts, status
3. Make changes
4. Update downstream impacts
5. Delete REINDEX.md

**Constraints:**
- Output blocked while any REINDEX active
- All impacts must be addressed
- Cannot complete with open impacts

---

## Validation

FSM-level checks:
- All required root artifacts exist
- All state directories have triad
- All examples have triad (including examples/ directory itself)
- Episode files follow naming convention
- Asset IDs sequential
- Asset source episodes exist
- Prose references resolve to LEDGER
- No output during REINDEX
- Structure compliance (if specified)
- All protocol/pattern references resolve

**Protocol application:**
- reference_integrity_protocol (inherited from canonic)
- inheritance_protocol (inherited from canonic)
- triad_protocol (inherited from canonic)

---

End of root CANON.
