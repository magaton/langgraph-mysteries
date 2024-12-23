import uuid
from rich.console import Console
from rich.syntax import Syntax
from rich.markdown import Markdown
from typing import Any, Literal, Optional, Union, List, Tuple
from fuzzywuzzy import fuzz
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from experimental.types import BaseChatConfig

def find_starting_line_and_indent(file_content: str, chunk: str) -> int:
    #Locate a chunk in the original content.#
    # Try exact match first
    start_pos = file_content.find(chunk)
    if start_pos != -1:
        print(f"@@@@@@@@@@@ find_starting_line_and_indent: {start_pos}")
        return (
            file_content.count("\n", 0, start_pos) + 1,
            file_content[:start_pos].split("\n")[-1]
        )
    
    # Fallback to fuzzy matching
    print("@@@@@@@@@@@ find_starting_line_and_indent: FALLBACK TO FUZZY MATCHING @@@@@@@@@@@")
    lines = file_content.splitlines()
    best_score = 0
    best_line = -1
    for i, line in enumerate(lines):
        score = fuzz.partial_ratio(chunk, line)
        if score > best_score:
            best_score = score
            best_line = i
    # Return the line number of the best match
    return (
        file_content.count("\n", 0, best_line) + 1,
        file_content[:best_line].split("\n")[-1],
    )


def load_chat_model(chat_config: BaseChatConfig) -> BaseChatModel:
    """Load a chat model from a fully specified name. Hardcoded to be locally hosted openai model

    Args:
        fully_specified_name (str): String in the format 'provider/model'.
    """
    return init_chat_model(model_provider="openai", **chat_config.model_dump())

def get_message_text(msg: BaseMessage) -> str:
    """Get the text content of a message."""
    content = msg.content
    if isinstance(content, str):
        return content
    elif isinstance(content, dict):
        return content.get("text", "")
    else:
        txts = [c if isinstance(c, str) else (c.get("text") or "") for c in content]
        return "".join(txts).strip()
    
def _format_doc(doc: Document) -> str:
    """Format a single document as XML.


    Args:
        doc (Document): The document to format.

    Returns:
        str: The formatted document as an XML string.
    """
    metadata = doc.metadata or {}
    meta = "".join(f" {k}={v!r}" for k, v in metadata.items())
    if meta:
        meta = f" {meta}"

    return f"<document{meta}>\n{doc.page_content}\n</document>"


def format_docs(docs: Optional[list[Document]]) -> str:
    """Format a list of documents as XML.

    This function takes a list of Document objects and formats them into a single XML string.

    Args:
        docs (Optional[list[Document]]): A list of Document objects to format, or None.

    Returns:
        str: A string containing the formatted documents in XML format.

    Examples:
        >>> docs = [Document(page_content="Hello"), Document(page_content="World")]
        >>> print(format_docs(docs))
        <documents>
        <document>
        Hello
        </document>
        <document>
        World
        </document>
        </documents>

        >>> print(format_docs(None))
        <documents></documents>
    """
    if not docs:
        return "<documents></documents>"
    formatted = "\n".join(_format_doc(doc) for doc in docs)
    return f"""<documents>
{formatted}
</documents>"""


def reduce_docs(
    existing: Optional[list[Document]],
    new: Union[
        list[Document],
        list[dict[str, Any]],
        list[str],
        str,
        Literal["delete"],
    ],
) -> list[Document]:
    """Reduce and process documents based on the input type.

    This function handles various input types and converts them into a sequence of Document objects.
    It also combines existing documents with the new one based on the document ID.

    Args:
        existing (Optional[Sequence[Document]]): The existing docs in the state, if any.
        new (Union[Sequence[Document], Sequence[dict[str, Any]], Sequence[str], str, Literal["delete"]]):
            The new input to process. Can be a sequence of Documents, dictionaries, strings, or a single string.
    """
    if new == "delete":
        return []

    existing_list = list(existing) if existing else []
    if isinstance(new, str):
        return existing_list + [
            Document(page_content=new, metadata={"uuid": str(uuid.uuid4())})
        ]

    new_list = []
    if isinstance(new, list):
        existing_ids = set(doc.metadata.get("uuid") for doc in existing_list)
        for item in new:
            if isinstance(item, str):
                item_id = str(uuid.uuid4())
                new_list.append(Document(page_content=item, metadata={"uuid": item_id}))
                existing_ids.add(item_id)

            elif isinstance(item, dict):
                metadata = item.get("metadata", {})
                item_id = metadata.get("uuid", str(uuid.uuid4()))

                if item_id not in existing_ids:
                    new_list.append(
                        Document(**item, metadata={**metadata, "uuid": item_id})
                    )
                    existing_ids.add(item_id)

            elif isinstance(item, Document):
                item_id = item.metadata.get("uuid")
                if item_id is None:
                    item_id = str(uuid.uuid4())
                    new_item = item.copy(deep=True)
                    new_item.metadata["uuid"] = item_id
                else:
                    new_item = item

                if item_id not in existing_ids:
                    new_list.append(new_item)
                    existing_ids.add(item_id)

    return existing_list + new_list    

def get_last_user_question(messages):
    # Iterate through messages in reverse to find the last user question
    for message in reversed(messages):
        if isinstance(message, dict) and message.get("type") == "human":
            return message.get("content")  # Return the content of the last user question
        elif isinstance(message, HumanMessage):
            return message.content  # Return the content if it's a HumanMessage instance
    
    return None  # Return None if no user question is found

def get_last_ai_message(messages):
    # Iterate through messages in reverse to find the last ai message
    for message in reversed(messages):
        if isinstance(message, dict) and message.get("type") == "ai":
            return message.get("content")  # Return the content of the last ai message
        elif isinstance(message, AIMessage):
            return message.content  # Return the content if it's a AIMessage instance
    
    return None  # Return None if no ai message is found

def display_search_result(state):
    console = Console()
    
    # Prepare a list to hold formatted messages for LangGraph
    formatted_messages = []
    
    id_docs = state["parent_document_map"]
    
    for doc in state["documents"]: 
        start_line, indentation = find_starting_line_and_indent(
            id_docs[doc.metadata["id"]], doc.page_content
        )
        
        syntax = Syntax(
            indentation + doc.page_content,
            doc.metadata.get("language", "unknown"),
            theme="monokai",
            line_numbers=True,
            start_line=start_line,
            indent_guides=True,
        ) 
  
        suffix = doc.metadata.get("method_name") if doc.metadata.get("method_name") is not None else doc.metadata.get("chunk")
        score = doc.metadata.get("relevance_score") if doc.metadata.get("relevance_score") is not None else 0.0
        
        # Create a formatted message for each document
        formatted_message = f"{doc.metadata['path']} -> {suffix} -> {score}"
        formatted_messages.append(formatted_message)
        
        # Print the syntax highlighting in the console
        console.print(formatted_message)
        console.print(syntax)
        console.print()  # Add a blank line for spacing

def display_messages(result):
    console = Console()
    for message in result["messages"] :
        console.print(f"{message.type}:")
        console.print(f"{message.content}")


def display_answer(result):
    markdown = Markdown(result["answer"])
    console = Console()
    console.print(markdown)        

