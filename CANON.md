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

### FSM Structure
The FSM consists of exactly four states:
- **episodes/** — Raw input (ungoverned)
- **assets/** — Registered entities (governed, immutable)
- **prose/** — Composed content (governed, mutable)
- **output/** — Validated artifacts (governed, immutable)

**Violation:** Missing state directory or using non-standard state names

### State Transitions

Transitions are unidirectional with validation gates:
- Episode → Asset: Extraction (registers entities)
- Asset → Prose: Composition (references assets)
- Prose → Output: Validation (compliance gate)

Backflow allowed only on validation failure:
- Output validation fails → return to Prose
- Asset validation fails → return to Episodes

**Violation:** Invalid transition direction or missing validation gate

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

**Violation:** Episode file naming non-sequential, modifying episode without REINDEX, or missing triad

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

**Violation:** Non-sequential asset IDs, missing LEDGER.md, duplicate assets, missing source traceability, or deleting referenced assets

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

**Violation:** Referencing unregistered assets, broken asset references, or missing dependencies

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

**Violation:** Generating output with validation failures, output exists during REINDEX, or modifying output directly

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

**Violation:** Extracting from non-existent episode, creating duplicate assets, or missing source traceability

### Asset → Prose

**Trigger:** Composition begins

**Requirements:**
- LEDGER.md exists
- At least one asset registered

**Validation:**
- All prose references resolve to LEDGER
- No unregistered entities

**Violation:** Composing without LEDGER, referencing unregistered assets, or broken references

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

**Violation:** Generating output with validation failures, active REINDEX, or unsatisfied dependencies

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

## Git-FSM Implementation

### Git commits as FSM transitions
**Git commits ARE FSM state transitions.**

**Commit structure:**
- Each commit proposes a state transition
- Pre-commit validation acts as gate (accept/reject)
- Rejected commits trigger backflow to source state
- Git history records the complete FSM transition log
- Commits must be atomic: one logical change, one constraint addressed
- Multiple unrelated changes must be separate commits

**Violation:** Non-atomic commits or commits without validation gates

### Self-healing implementation
**System detects violations through git history patterns.**

**Git violation signals:**
- Commit → Revert → Reapply pattern indicates failed validation attempt
- Rapid commit cycles on CANON files indicate drift
- Fix/violation keywords in commit messages indicate constraint failures

**Response:** Trigger comprehensive validation and require human approval before allowing transition

**Violation:** Git history shows violation patterns but validation was not triggered

### Self-measuring implementation
**System measures maturity through git commit analysis.**

**Maturity metrics:**
- Producer commits: Canonifications (discovering new patterns)
- Consumer commits: Applications and fixes (enforcing patterns)
- Producer ratio: Producer / (Producer + Consumer) percentage
- Ratio indicates system learning phase

**Maturity thresholds:**
- New system: >40% producer commits (rapid learning phase)
- Maturing system: 10-30% producer commits (refinement phase)
- Mature system: <10% producer commits (stable enforcement)

**Self-assessment signals:**
- High producer ratio → system discovering governance patterns
- Decreasing producer ratio → system maturing, constraints stabilizing
- Sudden producer spike → new domain or architectural shift
- Commit message patterns reveal producer vs consumer work

**Repository maturity signal:**
- Governance repositories (canonic/) must be stable (low commit frequency)
- Implementation repositories (machine/) may be active (high commit frequency during building)
- High base canon churn indicates paradigm immaturity or governance purity violations
- Base canon should be essentially static after paradigm stabilizes

**Measurement enables:**
- Visibility into system evolution
- Prediction of stability
- Recognition of learning phases
- Validation of governance completeness

**Violation:** System cannot determine its maturity phase from git history, producer/consumer commits are not distinguishable, or governance repository shows high commit frequency after stabilization

### Self-strengthening implementation
**System improves through git-based introspection cycles.**

**Pattern discovery requirement:**
- Git history analysis must identify meta-patterns
- Session boundaries reveal canonification clusters
- Backflow patterns indicate self-healing events
- Terminology drift triggers convergence opportunities
- Burst enforcement patterns signal constraint adoption
- Meta-patterns themselves must be canonified

**Introspection depth levels:**
- Level 1: Fix violations in work artifacts
- Level 2: Fix gaps in validation tools
- Level 3: Fix architectural violations in validators themselves
- Continue introspection until root cause found and canonified

**Recursive strengthening:**
- Each canonification makes future violations easier to catch
- Meta-patterns about improvement are themselves canonified
- System learns how to learn better
- Self-measurement tracks progress

**Pattern:** Work → Introspection → Learning → Canonification → Meta-Pattern Discovery → Recursive Strengthening

**Violation:** System operates without capturing learnings for canonification, fails to identify and canonify meta-patterns from git history, or stops introspection before reaching root cause

### Commit message patterns
**Commit messages must indicate producer vs consumer action.**

**Prohibited commit patterns:**
- "Add..." (ambiguous - use "Canonify" or "Apply")
- "Update..." (ambiguous - use "Apply" or "Fix")
- "Implement..." (ambiguous - use "Apply")
- "Complete..." (ambiguous - use "Apply")
- "Enforce..." (ambiguous - use "Apply")
- "Streamline..." (ambiguous - use "Apply self-optimizing")
- "Standardize..." (ambiguous - use "Apply" or "Fix")

**Required patterns:**
- Producer: "Canonify [what was learned]"
- Consumer: "Apply [constraint/pattern/protocol]" or "Fix [violation]"

**Producer-before-consumer ordering:**
- Canonify constraint FIRST (producer commit in governance repo)
- Apply constraint SECOND (consumer commit in implementation repo)
- Cannot apply non-canonical patterns

**Violation:** Commit message uses prohibited ambiguous patterns, doesn't clearly indicate producer vs consumer action, or consumer commit precedes producer commit

---

End of root CANON.
