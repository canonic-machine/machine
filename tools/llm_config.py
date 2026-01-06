#!/usr/bin/env python3
"""
LLM Configuration management implementing configuration_protocol.

Secure environment-based configuration loading for LLM providers.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False


@dataclass
class LLMConfig:
    """LLM Configuration container with validation."""

    # API Keys (required)
    openai_api_key: str
    deepseek_api_key: str
    anthropic_api_key: str

    # LLM Settings (optional with defaults)
    default_provider: str = "deepseek"
    timeout: int = 30
    max_retries: int = 3


class LLMConfigurationError(Exception):
    """LLM Configuration loading or validation error."""
    pass


def load_llm_config(env_file: Optional[Path] = None) -> LLMConfig:
    """
    Load and validate LLM configuration implementing configuration_protocol.

    Args:
        env_file: Path to .env file (default: ../.env relative to tools/)

    Returns:
        Validated LLMConfig object

    Raises:
        LLMConfigurationError: If configuration is invalid or missing required values
    """
    if env_file is None:
        # Default to ../.env from tools/ directory
        tools_dir = Path(__file__).parent
        env_file = tools_dir.parent / ".env"

    # Load environment variables
    if HAS_DOTENV and env_file.exists():
        load_dotenv(env_file)
    elif not env_file.exists():
        raise LLMConfigurationError(
            f"Configuration file not found: {env_file}\n"
            "Create .env file with required API keys or install python-dotenv"
        )

    # Required API keys
    required_keys = {
        'OPENAI_API_KEY': 'openai_api_key',
        'DEEPSEEK_API_KEY': 'deepseek_api_key',
        'ANTHROPIC_API_KEY': 'anthropic_api_key'
    }

    config_dict = {}

    # Load required keys
    for env_key, config_key in required_keys.items():
        value = os.getenv(env_key)
        if not value:
            raise LLMConfigurationError(
                f"Required environment variable not set: {env_key}\n"
                f"Add '{env_key}=your_key_here' to {env_file}"
            )
        if not _is_valid_api_key(value):
            raise LLMConfigurationError(
                f"Invalid API key format for {env_key}\n"
                "API keys should be non-empty strings"
            )
        config_dict[config_key] = value

    # Optional settings with defaults
    config_dict['default_provider'] = os.getenv('LLM_DEFAULT_PROVIDER', 'deepseek')
    config_dict['timeout'] = int(os.getenv('LLM_TIMEOUT', '30'))
    config_dict['max_retries'] = int(os.getenv('LLM_MAX_RETRIES', '3'))

    # Validate configuration
    _validate_llm_config(config_dict)

    return LLMConfig(**config_dict)


def _is_valid_api_key(key: str) -> bool:
    """Basic validation for API key format."""
    if not key or not isinstance(key, str):
        return False
    if len(key.strip()) == 0:
        return False
    return True


def _validate_llm_config(config_dict: Dict) -> None:
    """Validate LLM configuration values."""
    # Validate provider
    valid_providers = {'openai', 'deepseek', 'anthropic'}
    if config_dict['default_provider'] not in valid_providers:
        raise LLMConfigurationError(
            f"Invalid default provider: {config_dict['default_provider']}\n"
            f"Valid options: {', '.join(valid_providers)}"
        )

    # Validate timeout
    if config_dict['timeout'] <= 0:
        raise LLMConfigurationError("Timeout must be positive integer")

    # Validate max retries
    if config_dict['max_retries'] < 0:
        raise LLMConfigurationError("Max retries must be non-negative integer")


def get_available_providers(llm_config: LLMConfig) -> List[str]:
    """Get list of providers with valid API keys."""
    providers = []
    if llm_config.openai_api_key:
        providers.append('openai')
    if llm_config.deepseek_api_key:
        providers.append('deepseek')
    if llm_config.anthropic_api_key:
        providers.append('anthropic')
    return providers


def create_env_example(target_path: Optional[Path] = None) -> None:
    """Create .env.example file with documentation."""
    if target_path is None:
        tools_dir = Path(__file__).parent
        target_path = tools_dir.parent / ".env.example"

    example_content = """# CANONIC Machine Tools Configuration
# Copy this file to .env and fill in your API keys

# Required API Keys
OPENAI_API_KEY=sk-proj-your-openai-key-here
DEEPSEEK_API_KEY=sk-your-deepseek-key-here
ANTHROPIC_API_KEY=sk-ant-api03-your-anthropic-key-here

# Optional LLM Settings
LLM_DEFAULT_PROVIDER=deepseek
LLM_TIMEOUT=30
LLM_MAX_RETRIES=3
"""

    target_path.write_text(example_content)
    print(f"Created .env.example at {target_path}")


def main():
    """CLI interface for LLM configuration management."""
    import argparse

    parser = argparse.ArgumentParser(description="LLM Configuration management")
    parser.add_argument('--create-example', action='store_true',
                       help='Create .env.example file')
    parser.add_argument('--validate', action='store_true',
                       help='Validate current LLM configuration')
    parser.add_argument('--show', action='store_true',
                       help='Show current LLM configuration (without secrets)')

    args = parser.parse_args()

    if args.create_example:
        create_env_example()
        return

    try:
        llm_config = load_llm_config()

        if args.validate:
            providers = get_available_providers(llm_config)
            print("✅ LLM Configuration valid")
            print(f"Available providers: {', '.join(providers)}")
            print(f"Default provider: {llm_config.default_provider}")

        elif args.show:
            print("Current LLM configuration:")
            print(f"  Default provider: {llm_config.default_provider}")
            print(f"  Timeout: {llm_config.timeout}s")
            print(f"  Max retries: {llm_config.max_retries}")

            providers = get_available_providers(llm_config)
            print(f"  Available providers: {', '.join(providers)}")

        else:
            parser.print_help()

    except LLMConfigurationError as e:
        print(f"❌ LLM Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
