from src.framework.tool_registry import ToolRegistry
from src.framework.tool_use import handle_request
from src.tool_plugins import load_plugins
from src.ai.llm_tooluse_chain import build_chain


if __name__ == "__main__":
    registry = ToolRegistry()
    load_plugins(registry)
    chain = build_chain()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        result = handle_request(user_input, registry, chain)
        print(f"Assistant: {result}")
