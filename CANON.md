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

**Violation:** Validator hardcodes constraints (e.g., checking for VOCAB.md instead of honoring CANON-driven structure)

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
- AGENT commits include Co-Authored-By with AGENT identity
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

## Agent Behavior

### Agent programming paradigm
**Once validation system is functional and valid:**

Agents codify constraints in CANONs (sole edit point).
Agents run the machine (validation).
Machine produces all derived artifacts.

**Direct artifact editing violates paradigm.**

**Shift:**
- Before: agent edits files directly
- After: agent edits CANONs, machine edits files

**Constraint applies when:**
- System has valid CANON hierarchy
- Validation exists
- Triad complete in all directories

**Violation:** Agent bypasses CANONs and edits artifacts directly when system is valid

### Agent behavior in valid systems
**Agents make no assumptions about content.**

Agents make no editorial decisions.
Agents do not propose what "should" be documented.

**Only three permitted actions:**
1. Canonify constraints (add requirements to CANONs)
2. Run machine (execute validation)
3. Satisfy constraints (make system valid)

**Protocol:**
- If content is missing: add constraint requiring it, then satisfy
- If structure is wrong: add constraint defining correct form, then satisfy
- If unclear what's needed: that's a missing CANON constraint

**Violation:** Agent suggests content without CANON requirement, agent assumes intent without constraint, agent asks "should X be documented?" (canonify the requirement first)

### Self-aware AGENT governance
**AGENT self-awareness requires asking USER before canonifying.**

AGENT self-awareness means:
- Recognizing patterns
- Detecting drift
- Identifying violations

**Governance protocol:**
If AGENT recognizes something might be canonical, ask USER for governance decision.

Self-aware AGENT does not assume canonification authority.

**Violation:** Self-aware AGENT canonifies without asking USER

### Agent self-check protocol
**Before editing any artifact, agent must:**

1. Check if artifact is in Required Artifacts list (in CANON.md)
2. Check if artifact has constraints defined in CANON.md
3. If constraints exist: satisfy them
4. If constraints missing: canonify first, then satisfy

**Before creating new artifacts, agent must:**

1. Determine if artifact should be required or optional
2. Add artifact to appropriate section in CANON.md with constraints
3. Commit canonified constraints
4. Then create artifact satisfying constraints

**Exception:** Episodes are ungoverned (can be created freely as raw input)

**Violation:** Creating artifacts not defined in CANON, editing artifacts before checking CANON constraints, assuming what README/FAQ/etc. should contain without CANON basis

### AI/USER commit separation
**AI must never commit on USER's behalf. USER commits their own work.**

When USER performs work (external agent interaction, specification edits, etc.):
1. AI documents the work in an episode
2. AI leaves changes unstaged
3. AI asks USER to commit with their own message

**Proper workflow:**
- USER does work → changes unstaged
- AI creates episode documenting what happened
- AI asks: "Please commit with your message"
- USER commits with their own voice

**Why this matters:**
- Commits are signals of work done by the agent
- Agentized git signals require commit to reflect actual agent
- AI speaking for USER violates agent identity in git history

**Violation:** AI committing USER's work with AI-constructed message. This violates agentized git signals because the commit speaks for USER when USER did the work.

**Evidence:** Episode 047 documents AI repeatedly violating this constraint by committing USER's PAPER.md rebuild with AI-constructed messages.

---

End of root CANON.
