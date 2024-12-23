"""Define the configurable parameters for the agent."""

from pydantic import Field
from experimental.configuration import BaseConfiguration
from experimental.types import BaseChatConfig, OllamaChatConfig, OpenAIChatConfig, GLHFChatConfig
from experimental.chat_langchain import prompts

class AgentConfiguration(BaseConfiguration):
    """The configuration for the agent."""

    # models
    """
    query_model: OpenAIChatConfig = Field(
        default=OpenAIChatConfig(),
        title="The language model used for processing and refining queries",
        description= "The language model used for processing and refining queries. Should be in the form: provider/model-name." 
    )
    """
    query_model: GLHFChatConfig = Field(
        default=GLHFChatConfig(),
        title="The language model used for processing and refining queries",
        description= "The language model used for processing and refining queries. Should be in the form: provider/model-name." 
    )
    
    response_model: GLHFChatConfig = Field(
        default=GLHFChatConfig(),
        #default=VLLMChatConfig(),
        title="The language model used for processing and refining queries",
        description= "The language model used for processing and refining queries. Should be in the form: provider/model-name." 
    )

    # prompts
    router_system_prompt: str = Field(
        title="Router System Prompt", 
        description="The system prompt used for classifying user questions to route them to the correct node.",
        default=prompts.ROUTER_SYSTEM_PROMPT,
    )

    more_info_system_prompt: str = Field(
        title="More Info System Prompt", 
        description="The system prompt used for asking for more information from the user.",
        default=prompts.MORE_INFO_SYSTEM_PROMPT,
    )

    general_system_prompt: str = Field(
        title="General System Prompt", 
        description="The system prompt used for responding to general questions.",
        default=prompts.GENERAL_SYSTEM_PROMPT
    )

    research_plan_system_prompt: str = Field(
        title="Research Plan System Prompt", 
        description="The system prompt used for generating a research plan based on the user's question.",
        default=prompts.RESEARCH_PLAN_SYSTEM_PROMPT,
    )

    generate_queries_system_prompt: str = Field(
        title="Generate Queries System Prompt", 
        description="The system prompt used by the researcher to generate queries based on a step in the research plan.",
        default=prompts.GENERATE_QUERIES_SYSTEM_PROMPT,
    )

    response_system_prompt: str = Field(
        title="Response System Prompt", 
        description="The system prompt used for generating responses.",
        default=prompts.RESPONSE_SYSTEM_PROMPT
    )