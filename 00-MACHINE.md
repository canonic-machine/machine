# MACHINE

**The CANONIC validation engine for domain-agnostic constraint checking.**

This document defines the validation engine layer that domain applications inherit to implement governed finite state machines.

---

## The Problem

Content systems fail when validation is manual or absent:

- Constraints exist only in documentation
- Compliance checking is human-dependent
- Violations discovered late or never
- No systematic enforcement
- Governance drifts from implementation

LLMs make this worse without enforcement:
- They generate fluent content that violates constraints
- They cannot self-police against governance rules
- They drift between iterations
- They need external validation gates

Content systems need a validation engine. MACHINE provides this.

---

## The Solution

MACHINE is a **validation engine** that provides domain-agnostic constraint checking for CANONIC applications.

**Core capabilities:**
- Syntactic validation (structure, format, naming)
- Semantic validation (coherence, completeness via LLM)
- Reference integrity checking
- Triad compliance verification
- Git-FSM transition tracking
- Canon-awareness (derives rules from CANON.md)

**What MACHINE provides:**

```
Domain Application (e.g., WRITING)
         ↓
    Inherits from
         ↓
      MACHINE
    (validation engine)
         ↓
    Inherits from
         ↓
      CANONIC
    (root paradigm)
```

MACHINE enables domain applications to define their own FSMs while reusing validation infrastructure.

---

## Architecture Position

MACHINE occupies the **validation engine layer** in the three-layer architecture:

1. **CANONIC** (paradigm layer) - Defines constraints, validation, inheritance, triad
2. **MACHINE** (validation engine layer) - Implements constraint checking, git-FSM, self-* properties
3. **Domain applications** (application layer) - Inherit from MACHINE, add domain-specific FSMs

**MACHINE is domain-agnostic.**

It does not define:
- Specific state names (Episode, Asset, Prose, Output are domain-specific)
- Asset types (Person, Place, Claim are domain-specific)
- Content structure (narrative, documentation, research formats are domain-specific)

It does define:
- How to validate any FSM
- How to check constraint compliance
- How to track state transitions via git
- How to measure system maturity
- How to enable self-healing and self-strengthening

---

## Core Validation Framework

### Syntactic Validation

**Fast, deterministic checks:**
- File existence and naming conventions
- Directory structure compliance
- Triad presence (CANON.md, DICTIONARY.md, README.md)
- Alphabetical ordering in DICTIONARY.md
- Reference format validity
- Sequential numbering correctness

**Implementation:**
- Free (no LLM tokens required)
- Runs pre-commit
- Binary pass/fail
- Clear violation messages

### Semantic Validation

**LLM-powered deep checks:**
- Term definition consistency
- Constraint completeness
- Reference resolution
- Coherence verification
- Inheritance chain validity
- Canon alignment

**Implementation:**
- Token-cost aware
- Runs on-demand or pre-commit
- Provides diagnostic feedback
- Suggests fixes where possible

### Reference Integrity

**Cross-artifact validation:**
- Verify all references resolve
- Check inheritance chains
- Validate term usage
- Track source traceability
- Detect orphaned artifacts

---

## Git-FSM Implementation

### Commits as State Transitions

**Git commits ARE FSM state transitions.**

Every commit proposes a state transition:
- Pre-commit validation acts as gate (accept/reject)
- Rejected commits trigger backflow to source state
- Git history records complete FSM transition log
- Commits must be atomic: one logical change

**Commit structure requirements:**
- Atomic (single logical change, one constraint addressed)
- Validated (passes pre-commit gates)
- Traceable (clear producer vs consumer action)

**Commit message patterns:**

Producer commits (discovery):
- `Canonify [what was learned]`

Consumer commits (application):
- `Apply [constraint/pattern/protocol]`
- `Fix [violation]`

**Prohibited patterns:**
- Ambiguous verbs: "Add", "Update", "Implement", "Complete", "Enforce", "Standardize"
- These don't indicate whether work is canonical discovery or constraint application

---

## Canon-Awareness

**Validators must derive rules from CANON.md, not hardcode constraints.**

Traditional validators fail when governance evolves:
- Hardcoded file names become outdated
- Structural assumptions break
- Manual updates required

**Canon-aware validation:**
1. Read canonical triad definition from CANON.md
2. Extract current constraints from inheritance chain
3. Validate against current canonical requirements
4. Update automatically when CANON changes
5. Never hardcode file names or structural requirements

**Example:**

```
# Hardcoded (wrong)
check_file_exists("VOCABULARY.md")

# Canon-aware (correct)
triad_files = parse_canon_triad_requirement()
for file in triad_files:
    check_file_exists(file)
```

This enables governance evolution without validator code changes.

---

## Self-Properties

MACHINE implements three self-properties via git introspection:

### Self-Healing

**System detects violations through git history patterns.**

Git violation signals:
- Commit → Revert → Reapply indicates failed validation
- Rapid commit cycles on CANON files indicate drift
- Fix/violation keywords in messages indicate constraint failures

**Response:**
- Trigger comprehensive validation
- Require human approval before transition
- Log healing events for analysis

### Self-Measuring

**System measures maturity through git commit analysis.**

Maturity metrics:
- **Producer commits**: Canonifications (discovering patterns)
- **Consumer commits**: Applications and fixes (enforcing patterns)
- **Producer ratio**: Producer / (Producer + Consumer) percentage

Maturity thresholds:
- New system: >40% producer commits (rapid learning)
- Maturing: 10-30% producer commits (refinement)
- Mature: <10% producer commits (stable enforcement)

Repository maturity signals:
- Governance repositories (canonic/) must be stable (low commit frequency)
- Implementation repositories (machine/) may be active during building
- High base canon churn indicates paradigm immaturity
- Base canon should be static after paradigm stabilizes

### Self-Strengthening

**System improves through git-based introspection cycles.**

Pattern discovery:
- Git history analysis identifies meta-patterns
- Session boundaries reveal canonification clusters
- Backflow patterns indicate self-healing events
- Terminology drift triggers convergence
- Meta-patterns themselves are canonified

Introspection depth levels:
1. Fix violations in work artifacts
2. Fix gaps in validation tools
3. Fix architectural violations in validators
4. Continue until root cause found and canonified

Recursive strengthening:
- Each canonification makes future violations easier to catch
- Meta-patterns about improvement are themselves canonified
- System learns how to learn better
- Self-measurement tracks progress

**Pattern:** Work → Introspection → Learning → Canonification → Meta-Pattern Discovery → Recursive Strengthening

---

## Validation Protocol

### Pre-Commit Validation

Required checks before any commit:
1. Triad compliance (all three files present)
2. Alphabetical ordering in DICTIONARY.md
3. No orphaned section headers in CANON.md
4. All terms used in CANON/README defined in DICTIONARY
5. No redefinition of inherited terms
6. Inheritance links valid

### On-Demand Validation

Deep semantic checks:
1. Reference resolution across artifact tree
2. Constraint completeness analysis
3. Coherence verification
4. Source traceability audit
5. Drift detection

### Continuous Validation

Git-FSM monitoring:
1. Track commit patterns (producer vs consumer ratio)
2. Detect violation signals in history
3. Measure maturity phase
4. Identify canonification opportunities
5. Trigger self-healing when needed

---

## Directory Structure

MACHINE provides validation for directory structures with CANON:

```
domain-application/
├── CANON.md              # Inherits from machine
├── DICTIONARY.md         # Domain-specific terms
├── README.md             # Human guidance
├── state-1/
│   ├── CANON.md          # State-specific constraints
│   ├── DICTIONARY.md
│   ├── README.md
│   └── [state artifacts]
├── state-2/
│   ├── CANON.md
│   ├── DICTIONARY.md
│   ├── README.md
│   └── [state artifacts]
└── ...
```

Each directory has triad. MACHINE validates all.

---

## What MACHINE Enables

Domain applications that inherit MACHINE get:

**Automatic enforcement:**
- Constraints checked, not just documented
- Violations caught immediately
- Compliance non-negotiable

**Systematic validation:**
- Syntactic (fast, free)
- Semantic (deep, LLM-powered)
- Reference integrity
- Canon-awareness

**Git-based FSM:**
- Commits as state transitions
- History as transition log
- Backflow on failure
- Atomic changes

**Self-properties:**
- Self-healing (detect and recover from violations)
- Self-measuring (track maturity objectively)
- Self-strengthening (improve through introspection)

**Governance evolution:**
- CANONs change, validators adapt
- No hardcoded assumptions
- Inheritance enables composition
- Mature base canon remains stable

---

## Domain Application Integration

Domain applications (WRITING, DOCUMENTATION, RESEARCH) inherit MACHINE by:

1. Declaring inheritance in root CANON.md:
   ```markdown
   **Inherits from:** [canonic-machine/machine](https://github.com/canonic-machine/machine)
   ```

2. Defining domain-specific FSM in specification document (e.g., WRITING.md)

3. Adding domain-specific constraints in local CANON.md

4. Extending DICTIONARY.md with domain terms

5. Using MACHINE validation infrastructure

**Example inheritance chain:**

```
WRITING.md (4-state FSM: Episode → Asset → Prose → Output)
    ↓ inherits validation from
MACHINE (validation engine, git-FSM, self-properties)
    ↓ inherits paradigm from
CANONIC (constraints, triad, inheritance)
```

---

## Non-Negotiables

- Validators must be canon-aware (read CANON.md, don't hardcode)
- Commits must be atomic (one logical change)
- Commit messages must indicate producer vs consumer
- Git history must be analyzable (enable self-measurement)
- Validation happens pre-commit (prevent invalid states)
- Backflow returns to source state (fix upstream, not downstream)
- MACHINE stays domain-agnostic (no domain-specific patterns)

---

## What Comes Next

To use MACHINE:

1. Create domain application repository
2. Declare inheritance from MACHINE in CANON.md
3. Define domain-specific FSM in specification document
4. Add domain constraints to local CANON.md
5. Use MACHINE validation infrastructure
6. Commit triggers validation
7. Valid commits succeed, invalid commits backflow

MACHINE does not define what to validate.

MACHINE defines how to validate anything.

---

End of MACHINE specification.
