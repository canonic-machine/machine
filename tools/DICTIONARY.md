# DICTIONARY (tools/)

**Alphabetically ordered technical terms for machine tooling ecosystem.**

---

## Core Concepts

### CANONIC FSM
The finite state machine implemented by the machine repository: episodes → assets → prose → output.

### Protocol
Atomic, machine-parseable rule defining how artifacts must behave. Protocols are composed to create governance patterns.

### REINDEX Protocol
Controlled exception to immutability allowing coordinated changes across FSM states.

### Triad
The three required files in every governed directory: CANON.md, DICTIONARY.md, README.md.

### Validation Gate
A checkpoint where artifacts must pass compliance checks before advancing to the next state.

## Tool Categories

### Core Infrastructure Tools
Foundation tools providing configuration, environment management, and basic utilities.

### FSM Transition Tools
Human-AI collaboration tools for state transitions (episode→asset, asset→prose, etc.).

### LLM Integration Tools
Tools providing AI assistance for FSM transitions while maintaining CANONIC governance.

### Semantic Validation Tools
Tools that enforce FSM constraints and protocol compliance across all states.

## LLM Integration

### Fallback Strategy
Ordered list of providers to try when primary provider fails or is unavailable.

### Multi-Provider Support
Ability to route requests to different LLM providers (OpenAI, DeepSeek, Anthropic) based on configuration.

### OpenAI-Compatible API
Standard interface following OpenAI's chat completions format, allowing provider abstraction.

### Provider Routing
Automatic selection of LLM provider based on model name, availability, or performance criteria.

## Semantic Validation

### Cross-State Validation
Checks that span multiple FSM states (e.g., prose references to assets).

### Protocol Enforcement
Ensuring artifacts comply with declared protocols (traceability, immutability, uniqueness, etc.).

### Reference Integrity
Validation that all references between artifacts resolve to existing entities.

### State Transition Validation
Checking that artifacts meet requirements for advancing between FSM states.

## Configuration

### Configuration Protocol
Standardized approach to loading, validating, and using environment-based settings.

### Environment Variables
Key-value pairs loaded from .env files for secure configuration management.

### Fail-Fast Loading
Configuration strategy that validates all required variables at startup rather than failing later.

## Error Handling

### Exit Codes
Standardized numeric codes indicating tool execution results (0=success, 1=violations, 2=errors).

### Human-Readable Messages
Descriptive error messages with suggested remediation steps for users.

### JSON Output
Machine-parseable error reporting format for integration with other tools.

## Testing

### End-to-End Tests
Complete workflow tests from episode input to output validation.

### Integration Tests
Tests validating tool interaction with FSM states and external systems.

### Unit Tests
Tests validating individual functions and modules in isolation.

---

End DICTIONARY.
