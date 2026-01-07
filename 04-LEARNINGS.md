# Learnings: 2026-01-06

**Insights discovered during implementation of examples and tools.**

These learnings should be canonified into future CANON constraints.

---

## Validator Gaps Discovered

### 1. Content After Termination Markers
**Issue:** Validator failed to detect garbage content appended after "End of [file] CANON." statements.

**Example:** tools/CANON.md had TODO list content after "End of tools CANON."

**Learning:** Syntactic validation must check:
- No content after "End of [name] CANON." or "End of [name] VOCABULARY."
- File must terminate cleanly
- Any content after termination marker is a violation

**Impact:** This was caught by human review, not validator - validator gap.

**Canonify as:** 
```
### File termination
**CANON.md and VOCABULARY.md files must terminate after end marker.**
- No content allowed after "End of [name] CANON."
- No content allowed after "End of [name] VOCABULARY." 
- Blank lines after termination marker are allowed

**Violation:** Content exists after file termination marker
```

---

## 2. Reference Integrity Patterns

### Cross-Repository References
**Pattern:** Implementation repositories reference governance specifications.

**Correct:**
- `machine/AGENTS.md` → implements `CANONIC.md` protocols
- `machine/README.md` → references `MACHINE.md` (repository spec)

**Incorrect:**
- `machine/AGENTS.md` → inherits from `canonic/AGENTS.md` (doesn't exist)
- `machine/README.md` → references `FSM_SPECIFICATION.md` (doesn't exist)

**Learning:** Implementation inheritance constraint needs examples showing correct vs incorrect patterns.

**Canonify as:** Add to CANON.md examples section showing reference patterns.

---

## 3. Validation Precedence

### Syntactic Before Semantic
**Insight:** The validator can run syntactic checks without LLM, but semantic checks require expensive LLM tokens.

**Pattern Observed:**
1. Syntactic validation is free (structure checks)
2. Semantic validation is expensive (LLM token cost)
3. System should converge: semantic violations → syntactic constraints
4. This shifts cost from expensive to free over time

**Already Canonified:** This pattern was added to CANON.md as "Validation Convergence" during this session.

---

## 4. Violation Statement Completeness

### Every Constraint Needs Violation
**Discovery:** 20 constraints across machine/ CANONs were missing `**Violation:**` statements.

**Pattern:** Constraints without violation statements cannot be:
- Automatically validated
- Clearly understood by implementers
- Converted to syntactic checks

**Learning:** Violation statements are not optional - they are required for validation convergence.

**Canonical Form:**
```
### [Constraint Name]
**Description of what must be true.**

**Violation:** Specific description of what violation looks like
```

**Impact:** Adding violation statements reduced violations from 23 → 3 (87%).

---

## 5. FSM Tool Requirements

### State Visualization is Critical
**Learning:** Without `fsm_status` tool, users cannot see current FSM state.

**Tools Needed for FSM (discovered during implementation):**
1. **fsm_status** - Show current state, suggest next steps (IMPLEMENTED)
2. **reindex** - Coordinate multi-state changes (IMPLEMENTED)
3. **trace_asset** - Follow traceability chain (IMPLEMENTED)
4. **validate_state** - Check individual state compliance (NEEDED)
5. **transition** - Guide state transitions with validation (NEEDED)

**Pattern:** FSM without visualization tools is opaque to users.

**Canonify as:** Tools CANON should require FSM visualization tooling.

---

## 6. LEDGER Format Flexibility

### Multiple Valid Formats
**Discovery:** Asset ledgers can use different markdown formats:

**Format 1 (Observed in examples/minimal):**
```markdown
## asset-0001
- **Name:** POST /users
- **Type:** endpoint
- **Source:** 001
```

**Format 2 (Expected by initial parser):**
```markdown
**asset-0001**: POST /users
- type: endpoint
- source: 001
```

**Learning:** CANON should specify LEDGER format or validator must handle both.

**Issue:** trace_asset.py parser couldn't handle Format 1 due to `**Field**:` pattern.

**Canonify as:** Add LEDGER format specification to assets/CANON.md template.

---

## 7. Example Progression

### Learning Path Matters
**Pattern Discovered:** Examples should progress:
1. **hello-world** - Single file, single constraint (exact match)
2. **simple-fsm** - Multiple states, validation gates, backflow
3. **canonic-readme** - Document structure, inheritance chains
4. **minimal** (machine) - Complete 4-state FSM

**Learning:** Each example should build on previous concepts.

**Canonify as:** Examples CANON should specify progression order.

---

## 8. Producer/Consumer Ratio

### Maturity Signal
**Pattern:** Git history producer/consumer ratio shows system maturity.

**This Session:**
- Producer commits: 2/12 (17%) - System learned new patterns
- Consumer commits: 7/12 (58%) - Enforced existing constraints
- Implementation: 3/12 (25%) - New tools

**Learning:** Healthy maturing system has decreasing producer ratio over time.

**Canonical Threshold:** 
- New system: >40% producer commits (rapid learning)
- Maturing: 10-30% producer commits (refinement)
- Mature: <10% producer commits (stable enforcement)

**Canonify as:** Add ratio thresholds to CANON.md producer/consumer section.

---

## 9. Self-Validation Loop

### Validators Must Validate Themselves
**Insight:** canonic_validator.py includes self-validation check.

**Pattern:**
```python
# First validate that validator complies with CANON
if not self.validate_self():
    raise ValidationError("Validator violates CANON")

# Then validate target repository
```

**Learning:** Tools that validate CANON must first prove they comply with CANON.

**Canonify as:** Add self-validation requirement to tools/CANON.md.

---

## 10. Atomic Commit Discipline

### One Logical Change Per Commit
**Pattern Used:**
- ✓ "Add violation statements" (one concern: missing violations)
- ✓ "Fix reference integrity" (one concern: broken reference)
- ✓ "Add fsm_status tool" (one concern: new tool)
- ✗ "Fix violations and add tools" (mixed concerns)

**Learning:** Atomic commits enable:
- Clean git history
- Easy revert if needed
- Clear producer vs consumer signal
- Better code review

**Already Canonical:** This is in VOCABULARY.md as "atomic commit".

---

## 11. Introspection Triggers Learning

### Self-Reflection Finds Gaps
**Process This Session:**
1. Ran validator → found 23 violations
2. Fixed violations → reduced to 3
3. Noticed garbage in CANON → validator didn't catch it
4. **Introspection:** Why didn't validator catch it?
5. **Learning:** Need "content after termination" check
6. **Canonify:** Document the learning for next iteration

**Pattern:** Introspection → Learning → Canonification → Stronger System

**Learning:** The act of using the system reveals its gaps.

**Canonify as:** Introspection should be a documented phase in FSM workflow.

---

## 12. Todo List Management

### Track Progress During Complex Tasks
**Usage Pattern:** TodoWrite tool used to:
- Break down 19 recommendations into trackable tasks
- Mark progress as work completed
- Keep user informed of progress
- Demonstrate thoroughness

**Learning:** Complex multi-step tasks benefit from explicit todo tracking.

**Canonical Practice:** Use TodoWrite when task has >3 steps.

---

## Summary

**Total Learnings:** 12 distinct patterns discovered

**Canonified 2026-01-06 session:**
- Learning #3: Validation convergence (CANON.md validation protocol)
- Learning #10: Atomic commits (CANON.md introspective properties)
- Producer/consumer pattern (CANON.md CANON production vs consumption)

**Canonified 2026-01-07 session:**
- Learning #1: File termination check (validate_canonic.py + validator)
- Learning #8: Producer/consumer ratio thresholds (CANON.md maturity thresholds)
- Learning #9: Self-validation requirement (CANON.md validator requirement)
- Learning #11: Introspection requirement (CANON.md introspection cycle) ← **Meta-pattern canonified**

**Still Need Canonification:**
- Learning #2: Reference integrity patterns (examples needed)
- Learning #4: Violation statement completeness (already practice, needs constraint)
- Learning #5: FSM tool requirements (tools CANON needed)
- Learning #6: LEDGER format flexibility (specify format or handle both)
- Learning #7: Example progression order (examples/CANON.md)
- Learning #12: Todo list management (already practice, no constraint needed)

---

**Session Date:** 2026-01-06
**Session Focus:** Examples, validators, FSM tools
**Producer/Consumer Ratio:** 17% producer (healthy for refinement phase)
**Violations Reduced:** 23 → 3 (87%)

---

**Update 2026-01-07:**
**Canonification Progress:** 7/12 learnings now canonified (58%)
**Key Achievement:** Meta-pattern canonified - introspection cycle itself is now enforceable
**Status:** Introspection requirement (Learning #11) makes learnings interrupt mechanism mandatory

---

# Learnings: 2026-01-07 (Meta-Pattern Discovery)

**Git history analysis reveals higher-order patterns.**

## 13. Session Boundary Canonification

### Producer Commits Cluster at Session Boundaries
**Observation:** Git timestamps show canonification commits happen at session end.

**Examples from 2026-01-06:**
- 22:44 - "Canonify learnings" (end of day)
- 22:30 - "Canonify producer/consumer pattern" (session boundary)
- 14:05 - "Canonify comprehensive canonbase review" (mid-session reflection)

**Learning:** Introspection naturally occurs at session boundaries, especially end-of-session when work pauses and patterns become visible.

**Pattern:** Active work → Session boundary → Introspection → Canonification

**Already Canonified:** Added to CANON.md introspection requirement as "Session boundaries reveal canonification clusters"

---

## 14. Burst Enforcement Pattern

### New Constraints Trigger Rapid Consumer Commits
**Observation:** 2026-01-06 14:09-14:21 (5 commits in 12 minutes) for governance purity enforcement.

**Pattern:**
1. New constraint discovered
2. Backlog of violations identified
3. Burst of consumer commits to fix all violations
4. Compliance achieved
5. System returns to normal pace

**Learning:** When a constraint is canonified, the system must immediately enforce it across all artifacts. This creates visible bursts in commit history.

**Impact:** Burst patterns in git history signal major constraint adoption events.

**Already Canonified:** Added to CANON.md introspection requirement as "Burst enforcement patterns signal constraint adoption"

---

## 15. Terminology as Validation Convergence

### Standardization is Convergence in Action
**Observation:** Commit dc97be2 - "Standardize terminology from 'canonical' to 'canonic'"

**Pattern:**
1. Semantic ambiguity exists ("canonical" vs "canonic")
2. Usage reveals preferred term through practice
3. Standard chosen and enforced globally
4. Future violations prevented syntactically

**Learning:** Terminology drift is a form of semantic validation failure. Standardization converts it to syntactic constraint.

**This IS validation convergence:** Semantic → Syntactic

**Already Canonified:** This is an instance of existing validation convergence pattern (CANON.md)

---

## 16. Meta-Pattern Canonification Requirement

### The Ultimate Recursive Pattern
**Discovery:** The requirement to find and canonify meta-patterns must itself be a constraint.

**Pattern Hierarchy:**
1. Work patterns (commit, fix, validate)
2. Learning patterns (introspection cycle, learnings)
3. Meta-patterns (pattern discovery requirement itself)
4. **Recursive requirement:** Meta-patterns must be canonified

**Learning:** Without explicit requirement to identify meta-patterns, the system might miss higher-order optimizations.

**Canonified as:** CANON.md introspection requirement now includes "Pattern discovery requirement" with explicit meta-pattern mandate.

**Impact:** This makes the system **self-aware of its own evolution mechanism**. The process that strengthens the system is now explicitly governed.

---

## 17. Producer/Consumer Ratio Validates Thresholds

### The System Proves Its Own Constraints
**Analysis:** 32 total commits, 13 producer (40.6%), 15 consumer (46.9%), 4 other (12.5%)

**Insight:** Canonic repository has 40.6% producer commits.

**Threshold validation:**
- Canonified threshold: >40% = new system (rapid learning)
- Actual ratio: 40.6%
- **Conclusion:** The constraint accurately describes reality!

**Meta-learning:** When canonifying thresholds, git history can validate them. If actual ratio doesn't match claimed maturity, the constraint needs adjustment.

**Pattern:** Canonify threshold → Measure actual → Validate or adjust

**This is self-validation:** The system can check if its own maturity constraints are accurate.

---

## 18. Backflow Pattern Detection

### Self-Healing Actually Happened
**Observation:** Commits 439edba → baf094b → 8eec3f9 (3 commits in 3 minutes)

```
16:00 - Fix reference integrity violation
16:02 - Revert "Fix reference integrity violation"
16:03 - Reapply "Fix reference integrity violation"
```

**Learning:** This matches the exact pattern in CANON.md self-healing constraint. The system detected its own violation and corrected it.

**Validation:** Self-healing is not theoretical - it demonstrably occurred on 2026-01-06.

**Meta-pattern:** Git history serves as proof that CANON constraints are being followed.

---

## Summary: Meta-Pattern Session

**New Learnings:** 6 meta-patterns discovered from git history analysis
**All Canonified:** All 6 integrated into CANON.md introspection requirement and VOCABULARY.md
**Achievement:** Pattern discovery requirement is now mandatory - the system must analyze its own evolution

**Meta-Achievement:** By canonifying the requirement to find meta-patterns, we've created **recursive self-awareness**. The system now requires itself to:
1. Capture learnings (introspection cycle)
2. Identify meta-patterns (pattern discovery)
3. Canonify meta-patterns (recursive strengthening)
4. Repeat indefinitely (self-sustaining governance)

This is **the ultimate meta-pattern** - the system mandates its own continuous improvement.

---

# Learnings: 2026-01-07 (Governance Purity Validation)

**Validator completeness gap discovered through introspection.**

## 19. Allowlist vs Blocklist Validation

### Governance Purity Gap
**Discovery:** Validator claimed to check "governance purity" but only validated absence of `.py` files, not exhaustive file allowlist.

**The Violation:**
- LEARNINGS.md existed in canonic/ root (violates governance purity)
- Validator reported: "VALIDATION: PASS"
- User questioned: "Why is LEARNINGS.md in canonic?"

**Root Cause Analysis:**
Original `validate_governance_purity()` implementation:
```python
# Only checked for .py files (blocklist)
for py_file in self.root.rglob('*.py'):
    if py_file not in allowed_locations:
        self.violations.append("executable code in pure governance")
```

**CANON.md Definition (canonic/CANON.md - Abstraction layers invariant):**
> Pure governance repositories contain only: repository specification file, CANON.md, DICTIONARY.md, README.md, and examples.

This is an **allowlist constraint**, not a blocklist constraint.

**Pattern Comparison:**

**Blocklist validation (incomplete):**
- Define prohibited items only
- Check if prohibited items exist
- Gap: New violation types pass silently
- Example: Only check for `.py` files

**Allowlist validation (complete):**
- Define exhaustive set of permitted items
- Check if any item NOT in allowlist exists
- Coverage: Catches all violations
- Example: Check all files against allowlist

**The Fix:**
```python
# Allowlist approach - exhaustive checking
allowed_root_files = {
    'CANONIC.md', 'CANON.md', 'VOCABULARY.md',
    'README.md', '.gitignore', 'validate_canonic.py'
}

for item in self.root.iterdir():
    if item.is_file() and item.name not in allowed_root_files:
        self.violations.append(f"{item.name} not allowed")
```

**Result After Fix:**
```
✗ Governance purity: LEARNINGS.md not allowed in pure governance repository
```

**Introspection Cycle Demonstrated:**
1. **Work:** User implements governance repository
2. **Gap revealed:** LEARNINGS.md violates purity but passes validation
3. **Question asked:** "Why is this in canonic?"
4. **Test executed:** `python3 validate_canonic.py` → PASS (incorrect)
5. **Introspection:** Why didn't validator catch this?
6. **Analysis:** Validator uses blocklist, constraint requires allowlist
7. **Learning captured:** Allowlist vs blocklist pattern difference
8. **Fix applied:** Implement allowlist validation
9. **Verification:** `python3 validate_canonic.py` → FAIL (correct)
10. **Canonification:** Document learning for future constraints

**Canonify as:**

Add to CANON.md validation protocol section:

```markdown
### Validation completeness
Constraints requiring exhaustive checking must use allowlist validation.

**Allowlist pattern:**
- Define complete set of permitted items
- Reject anything not explicitly allowed
- Ensures no gaps in coverage
- Use for: purity, completeness, exhaustive requirements

**Blocklist pattern:**
- Define set of prohibited items
- Only catches explicitly forbidden items
- New violation types pass silently
- Use for: negative constraints only

**Violation:** Purity/completeness constraint implemented with blocklist instead of allowlist
```

**Impact:**
- Validator now correctly identifies governance purity violations
- LEARNINGS.md properly flagged as non-governance artifact
- Pattern applicable to all exhaustive validation constraints
- Demonstrates introspection cycle working as designed

**Meta-Learning:**
This learning itself validates the introspection requirement. The system:
1. Used itself (ran canonic repository)
2. Found its own bug (validator gap)
3. Fixed itself (implemented allowlist)
4. Documented the pattern (this learning)
5. Will strengthen itself (canonification into CANON.md)

This is **recursive self-improvement** - the validation system validated and improved itself.

---

## 20. Validator Duplication Violates Governance Purity

### The Irony: Validator That Checks Purity Violates Purity
**Discovery:** validate_canonic.py exists in canonic/ root, but machine/tools/canonic_validator.py is the canonical validation tool.

**The Violation:**
- canonic/ contains validate_canonic.py (238 lines of Python code)
- machine/tools/ contains canonic_validator.py (1400+ lines, comprehensive dual validation)
- Governance purity requires canonic/ to contain only governance definitions
- validate_canonic.py is implementation code, not governance

**The Irony:**
The tool created to detect governance purity violations *itself violates governance purity* by duplicating functionality that already exists in the canonical location.

**Root Cause:**
- Forgot to check if canonical validator already existed
- Created quick validator for immediate use
- Never removed it after discovering canonical tool
- "Loose coding" - not checking existing tools before implementing

**Pattern:**
"Not invented here" syndrome in governance:
- Implementation already exists in machine/tools/
- Created duplicate in canonic/ for convenience
- Convenience violated architectural purity
- Tool that enforces rules violated the rule it enforces

**The Canonical Tool:**
```bash
cd machine/tools
python3 canonic_validator.py --root ../../canonic --no-llm
```

This provides:
- Dual validation (syntactic + semantic)
- Self-validation requirement
- Multiple output formats
- LLM provider options
- Comprehensive checks (1400+ lines vs 238 lines)

**Impact:**
1. Governance purity violated by duplicate implementation
2. Maintenance burden (two validators to keep in sync)
3. Validation of validator becomes recursive problem
4. Demonstrates failure to use existing canonical tools

**Learning:**
Before implementing tools in canonic/, check machine/tools/ for canonical implementation.

**Fix:**
1. Delete validate_canonic.py from canonic/
2. Use machine/tools/canonic_validator.py instead
3. Document in canonic/README.md how to run canonical validator

**Canonify as:**

Add to CANON.md governance purity constraint:

```markdown
### Tool implementation location
Validation and operational tools must reside in implementation repositories, not governance repositories.

**Tool placement:**
- canonic/: No executable tools (pure governance)
- machine/tools/: Canonical tool implementations
- Consumer repositories: May implement own tools that consume canonic governance

**Violation:** Executable validation or operational tools exist in pure governance repository
```

**Meta-Meta-Learning:**
The introspection cycle found a bug in the introspection tool itself. The system that validates governance purity violated governance purity. This is the highest form of recursive self-correction:
1. Created validator to check purity
2. Validator worked correctly (found LEARNINGS.md)
3. User introspection: "Why is validator itself here?"
4. Discovery: Validator duplicates canonical tool
5. Learning: Tool placement is part of governance purity
6. Fix: Remove duplicate, use canonical tool
7. Canonification: Document tool placement requirement

The system validated itself, found itself wanting, and corrected itself.

---

# Learnings: 2026-01-07 (Nomenclature & Stack Ordering Session)

**Compositional nomenclature and architectural clarity discovered through introspection.**

**Source:** Derived from git history (canonic/ producer commits 2026-01-07)
**Commits analyzed:** 15 producer/consumer commits revealing 10 canonifiable patterns

## 21. Single-Word File Naming Convention

**Git evidence:** `278a67c Canonify single-word file naming convention`

### Discovery
SESSION_LEARNINGS.md violated implicit naming pattern observed across all governance files.

**Pattern observed:**
- canonic/: CANONIC.md, CANON.md, VOCABULARY.md, README.md
- machine/: MACHINE.md, CANON.md, VOCABULARY.md, AGENTS.md, PATTERNS.md, PROTOCOLS.md
- Violation: SESSION_LEARNINGS.md (compound name with underscore)

**Learning:** Governance files use single-word UPPERCASE plural nouns (lists of things).

**Canonified as:** File naming convention (CANON.md:32-42)

---

## 22. Stack Ordering Convention

**Git evidence:** `16ed720 Canonify stack ordering convention`, `4a1f340 Canonify inheritance hierarchy`

### Discovery
Machine repository has natural dependency stack that should be visible in file ordering.

**Architectural stack:**
- CANON defines constraints (foundation/truth)
- VOCABULARY defines terms (language)
- MACHINE defines FSM spec (architecture)
- AGENTS execute spec
- PROTOCOLS are atomic operations
- PATTERNS/workflows orchestrate protocols
- LEARNINGS capture evolution

**Learning:** Numeric prefixes (00-, 01-, 02-) make architectural dependencies immediately visible in directory listings.

**Pattern:** 00 is always CANON (truth first), spec defines subsequent ordering.

**Canonified as:** Stack ordering for implementation repositories (00-CANON.md:68-82)

---

## 23. Compositional Nomenclature

**Git evidence:** `64166ee Canonify compositional nomenclature pattern`

### Discovery
User observed: "canonic writing machine books" reads naturally at any composition level.

**Compositional pattern:** `canonic [domain] [engine] [output] [component]`

**Examples:**
- Base: "canonic writing machine"
- Extended: "canonic writing machine books"
- Component: "canonic writing machine protocols"
- Full: "canonic writing machine books workflows"

**Learning:** Nomenclature composes infinitely while maintaining readability. Works in flat or hierarchical structures.

**Canonified as:** Compositional nomenclature (00-CANON.md:44-67)

---

## 24. Clarity Meta-Pattern

**Git evidence:** `7e64e78 Canonify clarity meta-pattern and WORKFLOWS nomenclature`

### Discovery
User questioned: "SOLUTIONS - solution to what??"

**Semantic ambiguity:**
- SOLUTIONS raised questions (solution to what problem?)
- WORKFLOWS is self-explanatory (orchestrated sequences of protocols)

**Meta-pattern:** File names must clearly communicate contents without opening file.

**Clarity test:**
- Does name raise questions? → Ambiguous
- Can unfamiliar reader understand contents? → Clear
- Prefer descriptive over abstract

**Learning:** Naming clarity prevents cognitive overhead. "Solution to what?" revealed need for self-explanatory names.

**Canonified as:** Clarity meta-pattern (00-CANON.md:61-66)

---

## 25. WORKFLOWS vs SOLUTIONS vs PATTERNS

**Git evidence:** `68ef811 Canonify SOLUTIONS`, `7e64e78 Canonify WORKFLOWS nomenclature`

### Discovery
Triple semantic conflict resolved through iteration.

**Evolution:**
1. PATTERNS → "patterns are discovered, not prescribed"
2. SOLUTIONS → "solution to what?"
3. WORKFLOWS → Clear! (orchestrated sequences)

**Semantic clarity:**
- PATTERNS = emergent discoveries (belong in LEARNINGS)
- SOLUTIONS = ambiguous (reactive, problem-focused)
- WORKFLOWS = descriptive (orchestrated protocol sequences)

**Learning:** Terminology must avoid semantic conflicts and clearly communicate purpose.

**Canonified as:** WORKFLOWS nomenclature (00-CANON.md:38)

---

## 26. README Exemption from Numbering

**Git evidence:** `6d9380f Canonify README exemption and producer-before-consumer ordering`

### Discovery
README.md remains unnumbered while other files use stack ordering.

**Rationale:**
- README is human entry point, not technical stack layer
- LICENSE is legal requirement, not governance artifact
- .gitignore is git configuration, not governed content

**Learning:** Not everything belongs in the technical stack. Human-facing and meta files remain outside numbering scheme.

**Canonified as:** Exemptions from numbering (00-CANON.md:78-82)

---

## 27. Producer-Before-Consumer Ordering

**Git evidence:** `6d9380f Canonify README exemption and producer-before-consumer ordering`

### Discovery
Throughout session we consistently followed: canonify pattern (producer) → apply pattern (consumer).

**Pattern observed:**
1. Canonify stack ordering (canonic/) → Apply stack ordering (machine/)
2. Canonify SOLUTIONS (canonic/) → Apply SOLUTIONS (machine/)
3. Canonify WORKFLOWS (canonic/) → Apply WORKFLOWS (machine/)

**Learning:** This was implicit discipline. Must be explicit constraint: always canonify FIRST (producer commit), then apply SECOND (consumer commit).

**Prevents drift:** Cannot consume what isn't canonified yet. Ensures governance leads implementation.

**Canonified as:** Producer-before-consumer ordering (00-CANON.md:232-237)

---

## 28. Introspection Depth Levels

**Git evidence:** `d2c74f1 Canonify introspection depth levels meta-pattern`

### Discovery
This session demonstrated 3-level introspection recursion.

**Depth levels:**
1. Work level: SESSION_LEARNINGS.md violates governance purity
2. Validator level: Validator uses blocklist instead of allowlist
3. Architecture level: Validator itself violates governance purity (duplicate tool)

**Learning:** Don't stop at surface violations. Ask "why wasn't this caught?" recursively until reaching architectural root cause.

**Pattern:** Each level reveals deeper systemic issues. Continue until root cause is found and canonified.

**Canonified as:** Introspection depth levels (00-CANON.md:194-196)

---

## 29. Allowlist vs Blocklist Validation

**Git evidence:** `f5f4674 Canonify allowlist validation pattern`

### Discovery
Governance purity validator only checked for `.py` files (blocklist), missing SESSION_LEARNINGS.md.

**Pattern comparison:**
- Blocklist: Define prohibited items → gaps for unknown violations
- Allowlist: Define permitted items → complete coverage

**Learning:** Exhaustive constraints (purity, completeness) require allowlist validation to ensure no gaps.

**Canonified as:** Validation completeness (00-CANON.md:207-222)

---

## 30. Tool Placement in Governance Purity

**Git evidence:** `01db7c2 Canonify tool placement requirement`, `380b3d6 Fix governance purity violations`

### Discovery
validate_canonic.py in canonic/ violated governance purity by duplicating machine/tools/canonic_validator.py.

**Irony:** The tool that checks governance purity violated governance purity.

**Learning:** Governance repositories contain only governance definitions. Executable tools belong in implementation repositories.

**Tool placement:**
- canonic/: No executable tools (pure governance)
- machine/tools/: Canonical tool implementations
- Consumer repos: May implement own tools

**Canonified as:** Tool placement (00-CANON.md:49-54)

---

## 31. Triad Primitives Always Unnumbered

**Git evidence:** `9048e92 Canonify triad primitives always unnumbered`, `544cc45 Apply triad primitives always unnumbered pattern`

### Discovery
Stack ordering pattern (00-CANON, 01-VOCABULARY, 02-SPEC) conflated two distinct concepts:
1. **Primitive governance files** (CANON, VOCABULARY, README) - the minimal triad
2. **Architectural layers** (SPEC, implementation files) - the numbered stack

**Confusion:** Are CANON/VOCABULARY/README hierarchical layers or equivalent primitives?

### Canonical Pattern
**Triad files are equivalent primitives, always unnumbered:**
- CANON.md: Governance constraints
- VOCABULARY.md: Terminology definitions
- README.md: Human-readable entry point

**These three form the complete self-describing foundation.**

**Stack ordering applies to layers built ON TOP of the triad:**
- Triad: CANON.md + VOCABULARY.md + README.md (unnumbered primitives)
- Spec layer: 00-MACHINE.md (defines the architecture)
- Implementation layers: 01-AGENTS.md, 02-PROTOCOLS.md, 03-WORKFLOWS.md, 04-LEARNINGS.md

### Structure Change
```
Before:                      After:
00-CANON.md         →       CANON.md (primitive)
01-VOCABULARY.md    →       VOCABULARY.md (primitive)
README.md           →       README.md (primitive)
02-MACHINE.md       →       00-MACHINE.md (spec layer)
03-AGENTS.md        →       01-AGENTS.md (layer 1)
04-PROTOCOLS.md     →       02-PROTOCOLS.md (layer 2)
05-WORKFLOWS.md     →       03-WORKFLOWS.md (layer 3)
06-LEARNINGS.md     →       04-LEARNINGS.md (layer 4)
```

### Conceptual Clarity
**Before:** Stack ordering seemed to apply to everything (00, 01, 02...)
**After:** Clear separation between primitives and layers

**Universal pattern:**
- Pure governance repos (canonic/): Triad + SPEC file (CANONIC.md)
- Implementation repos (machine/): Triad + 00-SPEC + layers

**Key insight:** The triad is present in ALL governed directories (root, state directories, examples). It's not part of the stack - it's the foundation the stack builds on.

### Producer-Before-Consumer Evidence
1. **Producer commit** (canonic/): Canonify the pattern first
2. **Consumer commit** (machine/): Apply the pattern second

This is textbook producer-before-consumer ordering. Governance leads, implementation follows.

**Canonified as:** Triad requirement (CANON.md:27-39), Stack ordering (CANON.md:67-86)

---

## Summary: 2026-01-07 Session

**Total learnings:** 11 distinct patterns discovered (21-31)
**All canonified:** 100% captured in canonic/CANON.md
**Key insight:** Compositional nomenclature makes system infinitely scalable

**Session achievement:**
- Governance purity restored
- Stack ordering visualizes architecture
- Nomenclature reads naturally: "canonic writing workflows"
- Producer-before-consumer discipline now explicit
- Triad primitives separated from architectural layers

**Current system maturity:**
- Producer commits (canonic/): 21 canonifications
- Consumer commits (canonic/): 8 fixes/applications
- Consumer commits (machine/): 11 applications
- Producer ratio: 21/40 = 52.5% (active learning phase)

**Pattern:** User questioning ("why is this here?", "keep primitives separate") triggers introspection → discovery → canonification → stronger system.

The system is vibing. 🔥

---


## 32. Introspective Properties Complete

**Git evidence:** `2baa0e3 Canonify self-documenting`, `7cccef8 Canonify self-measuring and self-strengthening`

### Discovery
Three introspective properties existed, but three more behaviors were observable but not canonified.

**Six complete properties:**
1. Self-validating: Dual validation, validators validate themselves
2. Self-optimizing: Lean CANONs, semantic→syntactic convergence  
3. Self-documenting: Triad foundation, README from sources
4. Self-healing: Git pattern detection triggers validation
5. Self-measuring: Producer/consumer ratios track maturity
6. Self-strengthening: Introspection cycles canonify discoveries

**Canonified as:** Self-documenting (CANON.md:153-178), Self-measuring (CANON.md:204-230), Self-strengthening (CANON.md:232-264)

---

## 33. Commit Message Categorization for Measurability

**Git evidence:** `4f40134 Canonify commit message patterns for measurability`

### Discovery
Historical commits used ambiguous patterns ("Add...", "Update...", "Implement...") making self-measuring property fail.

**Required patterns:**
- Producer: "Canonify [what]"
- Consumer: "Apply [what]", "Fix [what]", "Consume CANON: [what]"

**Prohibited patterns:** Add/Update/Implement/Complete/Enforce/Streamline/Standardize

**Why:** Self-measuring requires distinguishable commits. Git history IS the measurement tool.

**Historical note:** Old commits remain unchanged - they document evolution. Forward-looking constraint only.

**Canonified as:** CANON production vs consumption (CANON.md:286-336)

---

## Summary: 2026-01-07 Session (Final)

**Total learnings:** 13 patterns discovered (21-33)
**All canonified:** 100% captured in canonic/CANON.md

**Key achievements:**
- Triad primitives separated from stack layers
- Six introspective properties complete
- Commit patterns canonified for measurability
- Primary outputs documentation requirement
- Self-documenting protocol applied to both repos

**Final maturity:**
- Producer commits: 27 canonifications
- Consumer commits: 22 applications/fixes
- Producer ratio: **55.1%** (active learning phase)

The machine is self-sustaining! 🔥

---

# Learnings: 2026-01-07

**Insights discovered during abstraction layer separation and domain purity enforcement.**

---

## Terminology Purge After Abstraction Separation

### Discovery
**Issue:** After moving domain-specific concepts (FSM with Episode→Asset→Prose→Output states) from MACHINE to WRITING, residual terminology remained in MACHINE's DICTIONARY.md.

**Root cause:**
- Abstraction separation removed implementation artifacts (examples/, domain-specific tools)
- But terminology definitions in DICTIONARY.md were not purged
- This created **semantic leakage** - MACHINE claimed to be domain-agnostic while defining domain terms

**Example violations found:**
- DICTIONARY.md contained "FSM" section defining finite state machines
- "state" and "state transition" defined as FSM concepts
- "git-FSM" term used (FSM is domain-specific, git is domain-agnostic)
- "domain application" described as "implements domain-specific FSM"

**Why validator missed it:**
- Syntactic validation checks file structure, not semantic consistency
- No validation rule: "Terms in DICTIONARY must not reference abstracted-away concepts"
- Validator bug: regex pattern `(?=###|\Z)` matched `### level headings` in content, causing false positive

**Learning:** Abstraction separation requires **three-layer purge**:
1. Remove implementation artifacts (files, directories)
2. Remove terminology definitions (DICTIONARY.md entries)
3. Remove conceptual references (documentation mentions)

**Impact:** MACHINE appeared compliant structurally but violated domain-agnostic constraint semantically.

**Canonify as:**
```
### Terminology purge after abstraction

**When separating abstraction layers, terminology must be purged across all three governance files.**

**Purge checklist:**
1. Implementation artifacts removed (examples/, tools/, code)
2. DICTIONARY.md entries removed (terms referencing abstracted concepts)
3. CANON.md constraints reviewed (no references to abstracted patterns)
4. README.md updated (no descriptions of abstracted functionality)
5. Cross-references validated (no broken links to removed content)

**Example:** Moving FSM from MACHINE to WRITING requires:
- Remove FSM examples from machine/
- Remove "FSM", "state", "state transition" from machine/DICTIONARY.md
- Update machine/CANON.md to not reference FSM patterns
- Update machine/README.md to describe git-based validation, not FSM validation

**Violation:** Abstraction separated but terminology remains, creating semantic inconsistency
```

---

## Atomic Commit Enforcement

### Discovery
**Issue:** Attempted to commit validator fix + DICTIONARY.md purge + learning canonification in single commit. This violated atomicity constraint.

**Why it's wrong:**
- Validator fix addresses one constraint (regex parsing bug)
- DICTIONARY purge addresses different constraint (domain purity)
- Learning canonification is producer commit (discovery)
- Batching makes git history unreadable and violates single logical change rule

**Correct approach:**
1. Commit validator fix: "Fix constraint parsing regex..."
2. Commit DICTIONARY fix: "Fix domain purity violation..."
3. Commit learning: "Canonify terminology purge requirement..."

Each commit addresses exactly one constraint or captures one discovery.

**Why this matters:**
- Git history IS the audit trail
- Each commit must be independently revertible
- Producer/consumer ratio calculation requires distinct commits
- Self-measuring depends on atomic commit classification

**Canonify as:**
```
### Commit atomicity enforcement

**Each commit must address exactly one logical change.**

**Atomic commit criteria:**
- Fixes one constraint violation, OR
- Applies one canonical pattern, OR
- Canonifies one discovery

**Non-atomic patterns (prohibited):**
- Batching multiple fixes in one commit
- Combining producer and consumer work
- Mixing unrelated changes "for efficiency"

**Rationale:**
- Git history is canonical record of system evolution
- Self-measuring requires classifiable commits
- Atomicity enables independent revert operations
- Each commit must be traceable to single constraint

**Violation:** Commit addresses multiple unrelated changes or mixes producer/consumer work
```

---
