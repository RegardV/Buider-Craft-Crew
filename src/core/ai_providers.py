"""
AI Crew Builder Team - AI Provider Interface
Manages interactions with different AI providers (Claude, ZhipuAI, OpenAI).
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, AsyncGenerator
from dataclasses import dataclass
from enum import Enum

from anthropic import Anthropic
from openai import OpenAI
from zhipuai import ZhipuAI

from .config import get_config, AIProviderConfig

logger = logging.getLogger(__name__)

class ProviderType(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    ZHIPUAI = "zhipuai"

@dataclass
class Message:
    role: str  # "user", "assistant", "system"
    content: str
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class AIResponse:
    content: str
    provider: str
    model: str
    usage: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class BaseAIProvider(ABC):
    """Base class for AI providers."""

    def __init__(self, config: AIProviderConfig):
        self.config = config
        self.client = None
        self._initialize_client()

    @abstractmethod
    def _initialize_client(self):
        """Initialize the AI provider client."""
        pass

    @abstractmethod
    async def generate_response(
        self,
        messages: List[Message],
        **kwargs
    ) -> AIResponse:
        """Generate a response from the AI."""
        pass

    @abstractmethod
    async def generate_stream(
        self,
        messages: List[Message],
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Generate a streaming response from the AI."""
        pass

class AnthropicProvider(BaseAIProvider):
    """Anthropic Claude provider."""

    def _initialize_client(self):
        try:
            self.client = Anthropic(api_key=self.config.api_key)
            logger.info(f"Initialized Anthropic client with model: {self.config.model}")
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {e}")
            raise

    async def generate_response(
        self,
        messages: List[Message],
        **kwargs
    ) -> AIResponse:
        """Generate response using Claude."""
        try:
            # Convert messages to Claude format
            claude_messages = []
            system_message = None

            for msg in messages:
                if msg.role == "system":
                    system_message = msg.content
                else:
                    claude_messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })

            # Generate response
            response = self.client.messages.create(
                model=self.config.model,
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                temperature=kwargs.get("temperature", self.config.temperature),
                system=system_message,
                messages=claude_messages
            )

            return AIResponse(
                content=response.content[0].text,
                provider="anthropic",
                model=self.config.model,
                usage={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                }
            )

        except Exception as e:
            logger.error(f"Error generating response from Claude: {e}")
            raise

    async def generate_stream(
        self,
        messages: List[Message],
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Generate streaming response from Claude."""
        try:
            # Convert messages to Claude format
            claude_messages = []
            system_message = None

            for msg in messages:
                if msg.role == "system":
                    system_message = msg.content
                else:
                    claude_messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })

            # Generate streaming response
            with self.client.messages.stream(
                model=self.config.model,
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                temperature=kwargs.get("temperature", self.config.temperature),
                system=system_message,
                messages=claude_messages
            ) as stream:
                for text in stream.text_stream:
                    yield text

        except Exception as e:
            logger.error(f"Error in streaming response from Claude: {e}")
            raise

class ZhipuAIProvider(BaseAIProvider):
    """ZhipuAI GLM provider."""

    def _initialize_client(self):
        try:
            self.client = ZhipuAI(api_key=self.config.api_key)
            logger.info(f"Initialized ZhipuAI client with model: {self.config.model}")
        except Exception as e:
            logger.error(f"Failed to initialize ZhipuAI client: {e}")
            raise

    async def generate_response(
        self,
        messages: List[Message],
        **kwargs
    ) -> AIResponse:
        """Generate response using ZhipuAI."""
        try:
            # Convert messages to ZhipuAI format
            zhipu_messages = []

            for msg in messages:
                zhipu_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            # Generate response
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=zhipu_messages,
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                temperature=kwargs.get("temperature", self.config.temperature)
            )

            return AIResponse(
                content=response.choices[0].message.content,
                provider="zhipuai",
                model=self.config.model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            )

        except Exception as e:
            logger.error(f"Error generating response from ZhipuAI: {e}")
            raise

    async def generate_stream(
        self,
        messages: List[Message],
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Generate streaming response from ZhipuAI."""
        try:
            # Convert messages to ZhipuAI format
            zhipu_messages = []

            for msg in messages:
                zhipu_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            # Generate streaming response
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=zhipu_messages,
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                temperature=kwargs.get("temperature", self.config.temperature),
                stream=True
            )

            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f"Error in streaming response from ZhipuAI: {e}")
            raise

class OpenAIProvider(BaseAIProvider):
    """OpenAI GPT provider."""

    def _initialize_client(self):
        try:
            self.client = OpenAI(api_key=self.config.api_key)
            logger.info(f"Initialized OpenAI client with model: {self.config.model}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise

    async def generate_response(
        self,
        messages: List[Message],
        **kwargs
    ) -> AIResponse:
        """Generate response using OpenAI."""
        try:
            # Convert messages to OpenAI format
            openai_messages = []

            for msg in messages:
                openai_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            # Generate response
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=openai_messages,
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                temperature=kwargs.get("temperature", self.config.temperature)
            )

            return AIResponse(
                content=response.choices[0].message.content,
                provider="openai",
                model=self.config.model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            )

        except Exception as e:
            logger.error(f"Error generating response from OpenAI: {e}")
            raise

    async def generate_stream(
        self,
        messages: List[Message],
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Generate streaming response from OpenAI."""
        try:
            # Convert messages to OpenAI format
            openai_messages = []

            for msg in messages:
                openai_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            # Generate streaming response
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=openai_messages,
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                temperature=kwargs.get("temperature", self.config.temperature),
                stream=True
            )

            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f"Error in streaming response from OpenAI: {e}")
            raise

class AIProviderManager:
    """Manages multiple AI providers."""

    def __init__(self):
        self.config = get_config()
        self.providers: Dict[str, BaseAIProvider] = {}
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize all configured AI providers."""
        provider_configs = self.config.get_ai_providers()

        for name, provider_config in provider_configs.items():
            try:
                if provider_config.type == "anthropic":
                    self.providers[name] = AnthropicProvider(provider_config)
                elif provider_config.type == "zhipuai":
                    self.providers[name] = ZhipuAIProvider(provider_config)
                elif provider_config.type == "openai":
                    self.providers[name] = OpenAIProvider(provider_config)
                else:
                    logger.warning(f"Unknown provider type: {provider_config.type}")

            except Exception as e:
                logger.error(f"Failed to initialize provider {name}: {e}")

    def get_provider(self, name: str) -> Optional[BaseAIProvider]:
        """Get a specific AI provider."""
        return self.providers.get(name)

    async def generate_response(
        self,
        provider_name: str,
        messages: List[Message],
        **kwargs
    ) -> AIResponse:
        """Generate response from a specific provider."""
        provider = self.get_provider(provider_name)
        if not provider:
            raise ValueError(f"Provider {provider_name} not found")

        return await provider.generate_response(messages, **kwargs)

    async def generate_stream(
        self,
        provider_name: str,
        messages: List[Message],
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Generate streaming response from a specific provider."""
        provider = self.get_provider(provider_name)
        if not provider:
            raise ValueError(f"Provider {provider_name} not found")

        async for chunk in provider.generate_stream(messages, **kwargs):
            yield chunk

    def list_providers(self) -> List[str]:
        """List all available providers."""
        return list(self.providers.keys())

# Global provider manager instance
provider_manager = AIProviderManager()

def get_provider_manager() -> AIProviderManager:
    """Get the global provider manager instance."""
    return provider_manager