# VOCABULARY (tools/)

**Technical terms for machine tooling ecosystem.**

---

## Core Concepts

### CANONIC FSM
The finite state machine implemented by the machine repository: episodes → assets → prose → output.

### Protocol
Atomic, machine-parseable rule defining how artifacts must behave. Protocols are composed to create governance patterns.

### Triad
The three required files in every governed directory: CANON.md, VOCABULARY.md, README.md.

### Validation Gate
A checkpoint where artifacts must pass compliance checks before advancing to the next state.

### REINDEX Protocol
Controlled exception to immutability allowing coordinated changes across FSM states.

## Tool Categories

### Core Infrastructure Tools
Foundation tools providing configuration, environment management, and basic utilities.

### LLM Integration Tools
Tools providing AI assistance for FSM transitions while maintaining CANONIC governance.

### Semantic Validation Tools
Tools that enforce FSM constraints and protocol compliance across all states.

### FSM Transition Tools
Human-AI collaboration tools for state transitions (episode→asset, asset→prose, etc.).

## LLM Integration

### OpenAI-Compatible API
Standard interface following OpenAI's chat completions format, allowing provider abstraction.

### Multi-Provider Support
Ability to route requests to different LLM providers (OpenAI, DeepSeek, Anthropic) based on configuration.

### Provider Routing
Automatic selection of LLM provider based on model name, availability, or performance criteria.

### Fallback Strategy
Ordered list of providers to try when primary provider fails or is unavailable.

## Semantic Validation

### State Transition Validation
Checking that artifacts meet requirements for advancing between FSM states.

### Protocol Enforcement
Ensuring artifacts comply with declared protocols (traceability, immutability, uniqueness, etc.).

### Reference Integrity
Validation that all references between artifacts resolve to existing entities.

### Cross-State Validation
Checks that span multiple FSM states (e.g., prose references to assets).

## Configuration

### Environment Variables
Key-value pairs loaded from .env files for secure configuration management.

### Configuration Protocol
Standardized approach to loading, validating, and using environment-based settings.

### Fail-Fast Loading
Configuration strategy that validates all required variables at startup rather than failing later.

## Error Handling

### Exit Codes
Standardized numeric codes indicating tool execution results (0=success, 1=violations, 2=errors).

### JSON Output
Machine-parseable error reporting format for integration with other tools.

### Human-Readable Messages
Descriptive error messages with suggested remediation steps for users.

## Testing

### Unit Tests
Tests validating individual functions and modules in isolation.

### Integration Tests
Tests validating tool interaction with FSM states and external systems.

### End-to-End Tests
Complete workflow tests from episode input to output validation.

---

End VOCABULARY.
