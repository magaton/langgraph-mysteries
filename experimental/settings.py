import os
from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings
from typing import Optional

# load .env from parent directory
DOTENV = ".env"

class Settings(BaseSettings):


    openai_api_key: Optional[str] = Field(
        title="openai_api_key"
    )

    anthropic_api_key: Optional[str] = Field(
        title="anthropic_api_key"
    )

    google_api_key: Optional[str] = Field(
        title="google_api_key"
    )

    tavily_api_key: Optional[str] = Field(
        title="tavily_api_key"
    )

    e2b_api_key: Optional[str] = Field(
        title="e2b_api_key"
    )

    sambanova_api_key: Optional[str] = Field(
        title="sambanova_api_key"
    )

    glhf_api_key: Optional[str] = Field(
        title="glhf_api_key"
    )

    langchain_api_key: Optional[str] = Field(
        title="langchain_api_key"
    )

    langchain_tracing_v2: Optional[str] = Field(
        title="langchain_tracing_v2", default=True
    )

    langchain_endpoint: Optional[str] = Field(
        title="langchain_endpoint", default="https://api.smith.langchain.com"
    )


    # Pydantic automatically populates these from environment variables
    class Config:
        env_file = DOTENV

# set global instance of settings
settings = Settings()

def set_settings_to_env(settings_instance: Settings):
    # Iterate over each field and set it as an environment variable
    for field_name, field_value in settings_instance.model_dump().items():
        if field_value is not None:
            # Set each attribute as an environment variable
            os.environ[field_name.upper()] = str(field_value)

# Call the function to set environment variables
set_settings_to_env(settings)