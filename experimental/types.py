from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from experimental.settings import settings


class BaseChatConfig(BaseModel):
    
    model: Optional[str] = Field(
        title="Name of OpenAI model to use", default=None
    )
    temperature: Optional[float] = Field(
        title="Sampling temperature", default=None
    )
    base_url : Optional[str] = Field(
        title="Base URL for API requests", default=None
    )   
    api_key: Optional[str] = Field(
        title="API key for Tabby", default=None
    )
    disabled_params: Optional[dict] = Field(
        title="disabled params", default={}
    )

class OpenAIChatConfig(BaseChatConfig):
    model: str = Field(
        title="Name of OpenAI model to use", default="gpt-4"
    )
    temperature: float = Field(
        title="Sampling temperature", default=0
    )
    max_tokens: Optional[int] = Field(
        title="Max number of tokens to generate", default=None
    )
    base_url : Optional[str] = Field(
        title="Base URL for API requests", default=None
    )   

class OllamaChatConfig(BaseChatConfig):
    model: str = Field(
        title="Name of OpenAI model to use", default="llama3.1:8b"
    )
    temperature: float = Field(
        title="Sampling temperature", default=0
    )
    num_predict: Optional[int] = Field(
        title="Max number of tokens to generate", default=None
    )
    base_url : Optional[str] = Field(
        title="Base URL for API requests", default=None
    )   


class AnthropicChatConfig(BaseChatConfig):
    model: str = Field(
        title="Name of Anthropic model to use", default="claude-3.5-sonnet"
    )
    temperature: float = Field(
        title="Sampling temperature", default=0
    )
    max_tokens: Optional[int] = Field(
        title="Max number of tokens to generate", default=None
    )
    base_url : Optional[str] = Field(
        title="Base URL for API requests", default=None
    )  

class GoogleChatConfig(BaseChatConfig):
    model: str = Field(
        title="Name of Google model to use", default="gemini-exp-1121"
    )
    temperature: float = Field(
        title="Sampling temperature", default=0
    )
    max_tokens: Optional[int] = Field(
        title="Max number of tokens to generate", default=None
    )
    base_url : Optional[str] = Field(
        title="Base URL for API requests", default=None
    )  
      

class GLHFChatConfig(BaseChatConfig):
    model: str = Field(
        # title="Name of GLHF model to use", default="hf:Qwen/Qwen2.5-72B-Instruct"
        title="Name of GLHF model to use", default="hf:Qwen/Qwen2.5-14B-Instruct"
    )
    base_url : str = Field(
        title="Base URL for API requests", default="https://glhf.chat/api/openai/v1/"
    )    
    temperature: float = Field(
        title="Sampling temperature", default=0
    )
    api_key: str = Field(
        title="API key for GLHF", default=settings.glhf_api_key
    )  
    disabled_params: Optional[dict] = Field(
        title="disabled params", default={"parallel_tool_calls": None}
    )





