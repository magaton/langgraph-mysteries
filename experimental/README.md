# Welcome to Experimental

## Create .env

Copy `.env.sample` to `.env` and set the env variables.
If you do not have all the values, leave defaults from sample.

## How to install?
`poetry install` or `pip install`

## How to run?

### In cli:
`poetry run experimental --graph chat_langchain`

or if you use pip for installation
`experimental --graph chat_langchain`

### In langgraph studio
`poetry run langgraph dev`

or if you used pip:
`langgraph dev`

## Configuration

### How to change LLM provider:
Change ChatConfig implementation in `experimental/{EXPERIMENT}/configuration.py`
For example:

```
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
```    

### How to change model for the selected provider:
Modify: `experimental/types.py`  

For example:
```
    class GLHFChatConfig(BaseChatConfig):
        model: str = Field(
        # title="Name of GLHF model to use", default="hf:Qwen/Qwen2.5-72B-Instruct"
        title="Name of GLHF model to use", default="hf:Qwen/Qwen2.5-14B-Instruct"
    )
```