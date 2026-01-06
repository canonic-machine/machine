#!/usr/bin/env python3
"""
LLM integration implementing llm_integration_protocol.

OpenAI-compatible API with multi-provider support for CANONIC tools.
"""

import json
import time
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod

import requests

try:
    # Try relative imports first (when run as module)
    from .llm_config import LLMConfig, load_llm_config, get_available_providers
except ImportError:
    # Fall back to absolute imports (when run as script)
    from llm_config import LLMConfig, load_llm_config, get_available_providers


@dataclass
class LLMMessage:
    """Standard message format."""
    role: str  # "system", "user", "assistant"
    content: str

    def to_dict(self) -> Dict[str, str]:
        """Convert to OpenAI-compatible format."""
        return {"role": self.role, "content": self.content}


@dataclass
class LLMResponse:
    """Standard response format."""
    content: str
    usage: Optional[Dict[str, int]] = None
    model: Optional[str] = None
    provider: str = "unknown"
    raw_response: Optional[Any] = None


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, api_key: str, config: LLMConfig):
        self.api_key = api_key
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def chat_completion(self, messages: List[LLMMessage], **kwargs) -> LLMResponse:
        """Execute chat completion."""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Get the model name for this provider."""
        pass

    def _make_request(self, url: str, headers: Dict, payload: Dict) -> Dict:
        """Make HTTP request with retry logic."""
        for attempt in range(self.config.max_retries + 1):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=self.config.timeout
                )
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                if attempt == self.config.max_retries:
                    raise
                self.logger.warning(f"Request failed (attempt {attempt + 1}), retrying: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff


class OpenAIProvider(LLMProvider):
    """OpenAI API provider."""

    def get_model_name(self) -> str:
        return "gpt-4"

    def chat_completion(self, messages: List[LLMMessage], **kwargs) -> LLMResponse:
        """OpenAI chat completion."""
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": kwargs.get("model", self.get_model_name()),
            "messages": [msg.to_dict() for msg in messages],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 1000)
        }

        response_data = self._make_request(url, headers, payload)

        return LLMResponse(
            content=response_data["choices"][0]["message"]["content"],
            usage=response_data.get("usage"),
            model=response_data.get("model", self.get_model_name()),
            provider="openai",
            raw_response=response_data
        )


class DeepSeekProvider(LLMProvider):
    """DeepSeek API provider."""

    def get_model_name(self) -> str:
        return "deepseek-chat"

    def chat_completion(self, messages: List[LLMMessage], **kwargs) -> LLMResponse:
        """DeepSeek chat completion."""
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": kwargs.get("model", self.get_model_name()),
            "messages": [msg.to_dict() for msg in messages],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 1000)
        }

        response_data = self._make_request(url, headers, payload)

        return LLMResponse(
            content=response_data["choices"][0]["message"]["content"],
            usage=response_data.get("usage"),
            model=response_data.get("model", self.get_model_name()),
            provider="deepseek",
            raw_response=response_data
        )


class AnthropicProvider(LLMProvider):
    """Anthropic API provider."""

    def get_model_name(self) -> str:
        return "claude-3-sonnet-20240229"

    def chat_completion(self, messages: List[LLMMessage], **kwargs) -> LLMResponse:
        """Anthropic chat completion."""
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }

        # Convert messages to Anthropic format
        system_messages = [msg for msg in messages if msg.role == "system"]
        other_messages = [msg for msg in messages if msg.role != "system"]

        payload = {
            "model": kwargs.get("model", self.get_model_name()),
            "max_tokens": kwargs.get("max_tokens", 1000),
            "temperature": kwargs.get("temperature", 0.7),
            "messages": [msg.to_dict() for msg in other_messages]
        }

        if system_messages:
            payload["system"] = system_messages[0].content

        response_data = self._make_request(url, headers, payload)

        return LLMResponse(
            content=response_data["content"][0]["text"],
            usage=response_data.get("usage"),
            model=response_data.get("model", self.get_model_name()),
            provider="anthropic",
            raw_response=response_data
        )


class LLMClient:
    """Main LLM client implementing llm_integration_protocol."""

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or load_llm_config()
        self.providers = self._initialize_providers()
        self.logger = logging.getLogger(__name__)

    def _initialize_providers(self) -> Dict[str, LLMProvider]:
        """Initialize available providers."""
        providers = {}

        if self.config.openai_api_key:
            providers['openai'] = OpenAIProvider(self.config.openai_api_key, self.config)

        if self.config.deepseek_api_key:
            providers['deepseek'] = DeepSeekProvider(self.config.deepseek_api_key, self.config)

        if self.config.anthropic_api_key:
            providers['anthropic'] = AnthropicProvider(self.config.anthropic_api_key, self.config)

        return providers

    def chat_completion(self, messages: List[Union[LLMMessage, Dict]], **kwargs) -> LLMResponse:
        """
        OpenAI-compatible chat completion with automatic provider routing.

        Args:
            messages: List of messages in OpenAI format
            **kwargs: Additional parameters (model, temperature, max_tokens, provider)

        Returns:
            LLMResponse with standardized format
        """
        # Convert dict messages to LLMMessage objects
        standardized_messages = []
        for msg in messages:
            if isinstance(msg, dict):
                standardized_messages.append(LLMMessage(role=msg["role"], content=msg["content"]))
            else:
                standardized_messages.append(msg)

        # Determine provider
        provider_name = kwargs.get("provider", self.config.default_provider)

        # Override provider based on model name if specified
        model = kwargs.get("model")
        if model:
            if "claude" in model.lower():
                provider_name = "anthropic"
            elif "deepseek" in model.lower():
                provider_name = "deepseek"
            elif "gpt" in model.lower() or "openai" in model.lower():
                provider_name = "openai"

        # Get provider
        if provider_name not in self.providers:
            available = list(self.providers.keys())
            raise ValueError(f"Provider '{provider_name}' not available. Available: {available}")

        provider = self.providers[provider_name]

        # Remove provider from kwargs before passing to provider
        kwargs_copy = kwargs.copy()
        kwargs_copy.pop("provider", None)

        try:
            response = provider.chat_completion(standardized_messages, **kwargs_copy)
            self.logger.info(f"LLM call successful: {provider_name} ({response.model})")
            return response

        except Exception as e:
            self.logger.error(f"LLM call failed: {provider_name} - {e}")
            raise

    def get_available_providers(self) -> List[str]:
        """Get list of available providers."""
        return list(self.providers.keys())

    def get_default_provider(self) -> str:
        """Get the default provider name."""
        return self.config.default_provider


def main():
    """CLI interface for LLM operations."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="LLM API Client")
    parser.add_argument('--message', '-m', required=True,
                       help='Message to send to LLM')
    parser.add_argument('--model', help='Model to use')
    parser.add_argument('--provider', help='Provider to use')
    parser.add_argument('--temperature', type=float, default=0.7,
                       help='Temperature for generation')
    parser.add_argument('--max-tokens', type=int, default=1000,
                       help='Maximum tokens to generate')
    parser.add_argument('--list-providers', action='store_true',
                       help='List available providers')
    parser.add_argument('--system-message', '-s',
                       help='System message to set context')

    args = parser.parse_args()

    try:
        client = LLMClient()

        if args.list_providers:
            providers = client.get_available_providers()
            print("Available providers:")
            for provider in providers:
                print(f"  - {provider}")
            print(f"\nDefault provider: {client.get_default_provider()}")
            return

        # Build messages
        messages = []
        if args.system_message:
            messages.append({"role": "system", "content": args.system_message})
        messages.append({"role": "user", "content": args.message})

        # Make the call
        kwargs = {}
        if args.model:
            kwargs["model"] = args.model
        if args.provider:
            kwargs["provider"] = args.provider
        kwargs["temperature"] = args.temperature
        kwargs["max_tokens"] = args.max_tokens

        response = client.chat_completion(messages, **kwargs)

        print("Response:")
        print(response.content)
        print(f"\nProvider: {response.provider}")
        if response.model:
            print(f"Model: {response.model}")
        if response.usage:
            print(f"Usage: {response.usage}")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
