---

## Canonification Log

### No Orphaned or Empty Section Headers Invariant

**[Description of what must be true]:**
- Downstream CANONs must not include empty, orphaned, or placeholder section headers (e.g., '## Invariants' with no content).
- All section headers must be followed by substantive content or be removed.

**Violation:**
- CANON.md contains empty or orphaned section headers.
---

# CANON (/canonic/machine/)

**Governance for the CANONIC validation engine.**

**Inherits from:** [canonic-machine/canonic](https://github.com/canonic-machine/canonic)

Cross-repository inheritance is declarative (markdown links only). No git submodules, no scripts, no tooling.

This CANON defines the domain-agnostic validation engine layer.
---

## Core Validation Engine

### Validation framework
**MACHINE provides domain-agnostic constraint checking and git-FSM implementation.**

**Capabilities:**
- Syntactic validation (structure, format, naming)
- Semantic validation (coherence, completeness via LLM)
- Reference integrity checking
- Triad compliance
- Git-based FSM transition tracking

**Violation:** Validation engine contains domain-specific patterns or state structures

### Stack ordering
**Implementations form stacks by inheriting from each other.**

**Stack order:**
- Follows inheritance chain in order
- MACHINE → WRITING → PAPER (example)
- Each layer adds domain specificity while inheriting validation from layers above
- Stack order appears in inheritance paths: `/canonic/machine/writing/paper/`
- Paradigm (CANONIC) governs stacks but is not part of stack

**Violation:** Wrong stack order (e.g., "WRITING MACHINE" instead of "MACHINE WRITING"), including paradigm (CANONIC) as part of implementation stack

---

## Validation Implementation

### Validator canon-awareness
**Validators must derive validation rules from CANON.md, not hardcode constraints.**

**Implementation:**
- Read canonical triad definition from root CANON.md
- Validate against current canonical requirements
- Update automatically when CANON changes
- Do not hardcode file names or structural requirements

**Violation:** Validator hardcodes constraints (e.g., checking for VOCABULARY.md when canon requires VOCAB.md)

### Alphabetical ordering validation
**VOCAB.md files must be validated for alphabetical term ordering.**

**Validation method:**
- Extract term headers (### level headings)
- Verify alphabetical order within each section
- Case-insensitive comparison
- Syntactic check (free, fast)

**Violation:** VOCAB.md terms not alphabetically ordered within sections

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

### Git user classes
**GIT machine has two user classes with distinct commit patterns.**

**User classes:**
- AGENT (automated) - LLM executing governance
- USER (human) - Manual governance decisions

**Commit classes:**
1. Producer (AGENT) - "Canonify [learning]" - discovers constraints
2. Consumer (AGENT) - "Apply [constraint]" / "Fix [violation]" - enforces constraints
3. Manual (USER) - Human-authored changes, governance decisions

**Git metadata:**
- AGENT commits include "Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
- USER commits use human author identity
- Commit class detectable from message pattern and author metadata

**Collaboration model:**
- USER canonifies intent (manual commits to CANON)
- AGENT applies constraints (automated commits to artifacts)
- Mixed workflows: human governance + AI execution
- Git history shows governance evolution through commit class distribution

**Violation:** AGENT commits without identity metadata, ambiguous commit patterns that obscure user class

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

**Production triggers consumption:**
- Every producer commit must trigger consumer commits across all affected repositories
- Machine must be compliant with canonical changes before session ends
- Validation gates ensure compliance before allowing further work

**Violation:** Commit message uses prohibited ambiguous patterns, doesn't clearly indicate producer vs consumer action, consumer commit precedes producer commit, or producer commit not consumed across affected repositories

---

End of root CANON.
