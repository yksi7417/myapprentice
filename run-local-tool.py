from src.framework.tool_registry import ToolRegistry
from src.framework.tool_use import handle_request
from src.tool_plugins import load_plugins


if __name__ == "__main__":
    registry = ToolRegistry()
    load_plugins(registry)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        result = handle_request(user_input, registry)
        print(f"Assistant: {result}")
