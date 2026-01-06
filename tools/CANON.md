# CANON (tools/)

**Governance for machine tooling ecosystem.**

**Inherits from:** [machine/CANON.md](https://github.com/canonic-machine/machine)

---

## Invariants

### Tool Triad Requirement
**All tools must maintain the triad:**
- CANON.md defines constraints and protocols
- VOCABULARY.md defines terms used in governance
- README.md provides human-readable documentation

**Violation:** Tool directory missing any triad file

### Protocol Compliance
**All tools must implement and enforce declared protocols.**

**Violation:** Tool bypasses or ignores protocol requirements

### LLM Integration Constraints
**LLM integration must be:**
- OpenAI-compatible API interface
- Multi-provider support (OpenAI, DeepSeek, Anthropic)
- Environment-based configuration
- FSM-aware context provision

**Violation:** Non-standard LLM interface or missing provider support

### Semantic Validation Completeness
**Semantic validation must cover:**
- FSM state transitions (episodes → assets → prose → output)
- Protocol enforcement (traceability, immutability, uniqueness)
- Reference integrity across states
- REINDEX protocol handling

**Violation:** Missing validation coverage for declared constraints

### Self-Validating Tools
**Tools must validate their own operation against CANON.**

**Violation:** Tool produces invalid output without detection

---

## Tool Categories

### Core Infrastructure Tools
- **Purpose:** Foundation for tool ecosystem
- **Required:** Environment loader, configuration management
- **Protocol:** configuration_protocol

### LLM Integration Tools
- **Purpose:** AI-assisted FSM transitions
- **Required:** Multi-provider client, OpenAI-compatible API
- **Protocol:** llm_integration_protocol

### Semantic Validation Tools
- **Purpose:** FSM compliance checking
- **Required:** State validators, protocol enforcers
- **Protocol:** validation_protocol

### FSM Transition Tools
- **Purpose:** Human-AI collaboration for state transitions
- **Required:** Asset extraction, prose composition assistance
- **Protocol:** transition_protocol

---

## Protocol Definitions

### configuration_protocol

**Purpose:** Secure, environment-based configuration loading

**Parameters:**
- env_file: .env file location (default: ../.env)
- required_vars: mandatory environment variables
- optional_vars: allowed but not required

**Rules:**
- Load from .env file in parent directory
- Fail fast on missing required variables
- Never log or expose API keys
- Support .env.example for documentation

**Violation:** Insecure configuration handling

### llm_integration_protocol

**Purpose:** Standardized LLM provider integration

**Parameters:**
- providers: supported LLM providers
- api_compatibility: OpenAI API compliance level
- fallback_strategy: provider failover behavior

**Rules:**
- OpenAI-compatible chat/completions endpoint
- Automatic provider routing based on model name
- Environment variable configuration
- Request/response logging (without sensitive data)
- Rate limiting and error handling

**Violation:** Non-standard API interface

### validation_protocol

**Purpose:** Comprehensive FSM state validation

**Parameters:**
- states: FSM states to validate
- protocols: protocols to enforce
- reporting: violation reporting format

**Rules:**
- Validate all declared FSM constraints
- Check protocol compliance across states
- Report violations with file/line references
- Support partial validation (single state)
- Exit codes indicate validation status

**Violation:** Incomplete or incorrect validation

### transition_protocol

**Purpose:** AI-assisted FSM state transitions

**Parameters:**
- source_state: starting FSM state
- target_state: destination FSM state
- assistance_type: human-AI collaboration mode

**Rules:**
- Preserve CANONIC governance during AI assistance
- Require human approval for state transitions
- Provide FSM context to LLM (assets, episodes, etc.)
- Validate AI-generated output before acceptance
- Log transition provenance

**Violation:** Ungoverned AI state modifications

---

## Tool Lifecycle

### Development Phase
- **Create triad files** (CANON, VOCABULARY, README)
- **Implement protocol compliance**
- **Add comprehensive tests**
- **Validate against machine CANON**

### Deployment Phase
- **Environment configuration** via .env
- **Integration testing** with FSM examples
- **Documentation updates**
- **Protocol validation**

### Operation Phase
- **Continuous validation** against CANON
- **Error reporting** with actionable fixes
- **Performance monitoring**
- **Protocol updates** as machine evolves

---

## Integration Requirements

### FSM State Awareness
**Tools must understand FSM context:**
- Current state directory structure
- Asset ledger contents
- Episode availability
- Prose dependencies

### Protocol Inheritance
**Tools inherit protocols from machine/CANON.md:**
- traceability_protocol for asset references
- immutability_protocol for IDs
- validation_protocol for compliance

### Error Handling
**Standardized error reporting:**
- Exit codes: 0=success, 1=violations, 2=errors
- JSON output for machine parsing
- Human-readable messages
- Suggested remediation steps

---

## Quality Gates

### Pre-commit Validation
- All tools pass their own validation
- No triad file violations
- Protocol compliance verified
- Tests pass with >90% coverage

### Integration Testing
- End-to-end FSM workflow testing
- Multi-provider LLM failover testing
- Large content validation performance
- Error condition handling

### Documentation Completeness
- README.md covers all tool usage
- VOCABULARY.md defines all technical terms
- CANON.md constraints are testable

---

End of tools CANON.


				# TODO LIST UPDATE REQUIRED - You MUST include the task_progress parameter in your NEXT tool call.

				**Current Progress: 3/6 items completed (50%)**

				- [x] Analyze current validation setup
				- [x] Examine .env file contents
				- [x] Understand semantic validation requirements
				 [x] Create machine/tools/ directory with triad
				- [ ] Implement OpenAI compatible LLM integration
				- [ ] Complete semantic validation implementation
				- [ ] Test and validate the implementation

				

				
1. To create or update a todo list, include the task_progress parameter in the next tool call
2. Review each item and update its status:
   - [x] Analyze current validation setup
   - [x] Examine .env file contents
   - [x] Understand semantic validation requirements
   - [ ] Implement OpenAI compatible LLM integration
   - [ ] Complete semantic validation implementation
   - [ ] Test and validate the implementation

				

**Note:** 37% of items are complete. Proceed with the task.

				<environment_details>
# Visual Studio Code Visible Files
VOCABULARY.md

# Visual Studio Code Open Tabs
CANON.md
VOCABULARY.md

# Current Time
1/6/2026, 1:32:51 PM (America/New_York, UTC-5:00)

# Context Window Usage
42,470 / 256K tokens used (17%)

# Current Mode
ACT MODE
</environment_details>
