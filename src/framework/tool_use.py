import json
from pprint import pprint
from src.framework.tool_registry import ToolRegistry
from langchain.chains import LLMChain


def handle_request(user_input: str, registry: ToolRegistry, chain: LLMChain):
    tools = registry.list_tools()
    tool_descriptions = "\n".join(f"{name}: {info['description']}" for name, info in tools.items())

    system_prompt = f"""You are an assistant. You may only use the following tools:
{tool_descriptions}
If the user asks for anything outside this list, politely say it's not possible and suggest what you can do instead.
Respond ONLY with the tool name and the arguments as JSON if applicable.
"""

    llm_output = chain.invoke({"query": user_input,
                            "system_prompt": system_prompt})
    pprint(llm_output)

    try:
        if "```json" in llm_output:
            llm_output = llm_output.split("```json")[-1].split("```")[-2].strip()
        elif llm_output.startswith("```"):
            llm_output = llm_output.strip("`\n")

        result = json.loads(llm_output)
        if isinstance(result, dict) and "tool" in result:
            tool = registry.get(result["tool"])
        if tool:
            args = result.get("args") or result.get("arguments") or {}
            if isinstance(args, dict):
                return tool["func"](**args)
            elif isinstance(args, list):
                return tool["func"](*args)
            else:
                return "Error: Invalid argument format."
        else:
            return "Sorry, that tool is not available."

    except Exception as e:
        return f"Error: {str(e)}\n\nRaw output: {llm_output}"
