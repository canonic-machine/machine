# AGENTS (machine workspace instructions)

**Implements:** [CANONIC programming protocols](https://github.com/canonic-machine/canonic/blob/main/CANONIC.md)

This file defines agent behavior for the *machine* implementation framework. Follows CANONIC governance and adds FSM-specific enforcement.

---

## FSM-Specific Role

**Extends parent role with:**

- Enforce the 4-state FSM structure: episodes/, assets/, prose/, output/
- Describe validation status in terms of FSM states, transitions, and compliance
- Canonify all FSM-related solutions and insights discovered during work

---

## FSM-Specific Behavior

### Agent Artifact Management
**Agents must:**
- Update CANON.md and VOCABULARY.md files directly when constraints or terms change
- Generate README.md files automatically - never manually write README content
- Maintain triad integrity across all FSM states

**Violation:** Manual README editing or failure to update governance files

### Trace to FSM Sources
**Extends parent tracing with:**
- Trace findings to FSM documents (`FSM_SPECIFICATION.md`, `PROTOCOLS.md`, `WORKFLOWS.md`)
- Understand FSM transitions: Episode→Asset (extraction), Asset→Prose (composition), Prose→Output (validation)
- Reference state-specific CANONs when relevant

### FSM Canonification Protocol
**Extends parent canonification with FSM-specific targets:**

When you discover or implement FSM-specific fixes:

**FSM canonification targets:**

- **FSM structure issue** → Add to `machine/CANON.md`
- **State-specific constraint** → Add to state CANON (episodes/, assets/, prose/, output/)
- **Reusable protocol** → Add to `PROTOCOLS.md`
- **Pattern composition** → Add to `WORKFLOWS.md`
- **New FSM term** → Add to `VOCABULARY.md`

**FSM-specific questions to ask:**
1. Which state was affected?
2. Which transition failed?
3. What FSM constraint was missing?
4. Is this reusable as a protocol or pattern?

**FSM canonifiable insights:**
- "State missing required files" → Add to state constraints
- "Transition validation incomplete" → Add to transition rules
- "REINDEX behavior unclear" → Formalize in REINDEX protocol
- "Pattern reference broken" → Add to required artifacts list

**Principle:** Every FSM fix strengthens the state machine by encoding transition logic.

---

## FSM-Specific Enforcement

### State Governance
- **Episodes:** Ungoverned content, immutable after extraction (reindexable_artifact_pattern)
- **Assets:** Governed entities with stable IDs (ledger_pattern)
- **Prose:** Composed content referencing registered assets (fsm_state_pattern)
- **Output:** Final validated artifacts, only exists when compliant (fsm_state_pattern, immutable)

### Transition Gates
- Episode → Asset: Extraction must register with source traceability
- Asset → Prose: Composition must reference only registered assets
- Prose → Output: Validation must pass all compliance checks

### REINDEX Protocol
- Suspends immutability for coordinated changes
- Blocks output while active
- Must document reason, changes, impacts, status

---

## FSM-Specific Interaction Patterns

### FSM Work Pattern
**Extends parent workflow with FSM awareness:**

1. Identify which states are affected
2. Perform work across states
3. Ensure transitions validate
4. Canonify any FSM constraints discovered (per parent canonification protocol)
5. Report FSM state and what was canonified

### State Transition Pattern
**FSM-specific workflow:**

1. Validate current state compliance
2. Attempt transition
3. If transition fails, identify missing constraint
4. Fix constraint violation
5. Canonify constraint to prevent future transition failure
6. Re-validate transition

---

## FSM Canonification Templates

### For State Constraints
```markdown
### [State Name] State

**Additional constraint:**
- [What must be true in this state]

**Violation:** [What violates this state constraint]
```

### For Transition Rules
```markdown
### [State A] → [State B]

**Additional requirement:**
- [What must be satisfied for transition]

**Validation:**
- [How to check transition validity]
```

---

## Meta-Governance

**Inherits meta-governance from parent AGENTS.md.**

**FSM-specific additions:**
- FSM structure changes require updating FSM_SPECIFICATION.md
- Protocol/pattern changes require updating PROTOCOLS.md or WORKFLOWS.md
- State-specific changes require updating state CANONs
- All changes must maintain 4-state structure integrity

---

## Notes
- The machine repo defines the domain-agnostic 4-state FSM
- Applications (like writing) inherit and specialize these FSM constraints
- If asked "what is the machine," cite `README.md` and `FSM_SPECIFICATION.md` for context
- Examples in `examples/minimal/` demonstrate the complete FSM structure
- **Every session should strengthen FSM durability** through canonification

---

End AGENTS.
