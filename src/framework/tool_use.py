import json
from pprint import pprint
from src.framework.tool_registry import ToolRegistry
from src.ai.llm_chain import build_chain
# from mock_llm import mock_llm


def handle_request(user_input: str, registry: ToolRegistry):
    tools = registry.list_tools()
    tool_descriptions = "\n".join(f"{name}: {info['description']}" for name, info in tools.items())

    system_prompt = f"""You are an assistant. You may only use the following tools:
{tool_descriptions}
If the user asks for anything outside this list, politely say it's not possible and suggest what you can do instead.
Respond ONLY with the tool name and the arguments as JSON if applicable.
"""

    # response = mock_llm(user_input, system_prompt)  # Replace with local LLM later
    chain = build_chain()
    response = chain.invoke({"query": user_input,
                             "system_prompt": system_prompt})

    try:
        pprint(response)
        result = response["result"]
        tool = registry.get(result["tool"])
        if tool:
            return tool["func"](**result.get("args", {}))
        else:
            return "Sorry, that tool is not available."
    except Exception as e:
        return f"Error: {str(e)}"
