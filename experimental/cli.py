import argparse
import asyncio
from typing import Callable
from langchain.globals import set_debug
from langchain_core.messages import HumanMessage

from experimental.utils import display_answer
# implementations
from experimental.chat_langchain.graph import get_graph as get_chat_langchain_graph

set_debug(True)


LANGGRAPH_REGISTRY={
   "chat_langchain": get_chat_langchain_graph
}


def get_langgraph(type: str) -> Callable :
    if type not in LANGGRAPH_REGISTRY:
        raise ValueError(f"No langgraph registered with name {type}")
    else:
        print(f"Constructing langgraph with type: {type}")
        return LANGGRAPH_REGISTRY[type]()


def run():
    print("Started Experimental CLI...")
    parser = argparse.ArgumentParser(
        description="Playground for Langgraph based experiments",
        formatter_class=argparse.RawTextHelpFormatter  # Preserves line breaks in help text
    )
    parser.add_argument(
        "--graph",
        nargs="?",
        choices=[
                 "chat_langchain"
                ]
    )
    args = parser.parse_args()
         
    if any(args.graph == item.lower() for item in LANGGRAPH_REGISTRY.keys()):
        graph_name = args.graph.lower()
        langgraph = get_langgraph(graph_name)
        query = input("🔎 Enter the query:\n")
        print()
        print()
        result = asyncio.run(langgraph.ainvoke({"messages": [HumanMessage(content=query)]}))  
        display_answer(result)
    else:
        print(f"Invalid graph name: {args.graph}.")
        exit()
 
