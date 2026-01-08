# Machine Tools

**CANONIC FSM tooling ecosystem for content governance.**

This directory contains tools that implement and enforce the CANONIC finite state machine: episodes → assets → prose → output.

## Overview

The machine tools provide:

- **LLM Integration**: OpenAI-compatible API with multi-provider support
- **Semantic Validation**: FSM state transition and protocol compliance checking
- **FSM Transitions**: AI-assisted content processing with human oversight
- **Configuration Management**: Secure environment-based setup

## Tool Categories

### 🔧 Core Infrastructure

#### `config.py`
Environment configuration loader implementing configuration_protocol.

```bash
# Load and validate environment
python -m tools.config
```

### 🤖 LLM Integration

#### `llm.py`
OpenAI-compatible LLM client with multi-provider support.

```bash
# Chat completion with automatic provider routing
python -m tools.llm --model gpt-4 --message "Extract assets from episode"

# List available providers
python -m tools.llm --list-providers
```

### ✅ Semantic Validation

#### `validate.py`
Comprehensive FSM validation implementing validation_protocol.

```bash
# Validate entire FSM
python -m tools.validate

# Validate specific state
python -m tools.validate --state assets

# JSON output for automation
python -m tools.validate --json
```

### 🔄 FSM Transitions

#### `extract_assets.py`
AI-assisted asset extraction from episodes.

```bash
# Extract assets from specific episode
python -m tools.extract_assets episodes/001-research.md

# Interactive mode with human approval
python -m tools.extract_assets --interactive episodes/001-research.md
```

#### `compose_prose.py`
AI-assisted prose composition from assets.

```bash
# Generate prose draft from asset ledger
python -m tools.compose_prose --assets assets/LEDGER.md

# Compose specific section
python -m tools.compose_prose --section introduction --assets assets/LEDGER.md
```

## Configuration

Tools load configuration from `../.env`:

```bash
# Required API keys
OPENAI_API_KEY=sk-proj-...
DEEPSEEK_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Optional settings
LLM_DEFAULT_PROVIDER=openai
LLM_TIMEOUT=30
VALIDATION_STRICT=true
```

## Usage Patterns

### Content Creation Workflow

1. **Write Episodes** (raw input)
   ```bash
   # Manual: Create episodes/001-topic.md
   ```

2. **Extract Assets** (structured entities)
   ```bash
   python -m tools.extract_assets episodes/001-topic.md
   python -m tools.validate --state assets  # Check extraction
   ```

3. **Compose Prose** (governed content)
   ```bash
   python -m tools.compose_prose --assets assets/LEDGER.md
   python -m tools.validate --state prose   # Check references
   ```

4. **Validate Output** (compliance gate)
   ```bash
   python -m tools.validate  # Full FSM validation
   # If valid → output/ directory created
   ```

### Validation-Only Workflow

```bash
# Continuous validation during editing
python -m tools.validate --watch

# Pre-commit validation
python -m tools.validate --strict --exit-codes
```

### AI-Assisted Workflow

```bash
# LLM helps with asset extraction
python -m tools.extract_assets --llm-assist episodes/001-topic.md

# LLM helps with prose composition
python -m tools.compose_prose --llm-draft --assets assets/LEDGER.md

# Always validate after AI assistance
python -m tools.validate
```

## Error Handling

Tools follow standardized error reporting:

- **Exit Code 0**: Success, no violations
- **Exit Code 1**: Validation violations found
- **Exit Code 2**: Tool execution errors

```bash
# Check validation status in scripts
if python -m tools.validate; then
    echo "✅ FSM compliant"
else
    echo "❌ Violations found"
    exit 1
fi
```

## Development

### Adding New Tools

1. Create tool module in `tools/`
2. Add triad files (CANON.md, VOCAB.md, README.md)
3. Implement required protocols
4. Add comprehensive tests
5. Update this README.md

### Testing

```bash
# Run all tests
python -m pytest tools/

# Run specific tool tests
python -m pytest tools/test_validate.py

# Integration tests
python -m pytest tools/test_integration.py
```

### Protocol Compliance

All tools must implement declared protocols:

- `configuration_protocol`: Secure environment loading
- `llm_integration_protocol`: Standardized AI interfaces
- `validation_protocol`: Comprehensive compliance checking
- `transition_protocol`: Governed state transitions

## Architecture

```
tools/
├── config.py              # Configuration management
├── llm.py                 # LLM provider abstraction
├── validate.py            # Semantic validation engine
├── extract_assets.py      # Episode → Asset transition
├── compose_prose.py       # Asset → Prose transition
├── CANON.md              # Tool governance
├── VOCAB.md               # Technical terms
└── README.md             # This file
```

## Dependencies

- Python 3.9+
- openai
- anthropic
- requests
- python-dotenv

Install with:
```bash
pip install -r requirements.txt
```

## Governance

This tooling ecosystem is itself CANONIC:

- **Triad maintained**: CANON.md, VOCAB.md, README.md
- **Protocol compliant**: All declared protocols implemented
- **Self-validating**: Tools validate their own operation
- **FSM-aware**: Context-aware operation within machine states

Tools evolve through the same FSM they enforce.

---

**Built with ❤️ for CANONIC governance.**
