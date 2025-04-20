import json


def mock_llm(user_input, system_prompt):
    if "add" in user_input:
        return json.dumps({
            "tool": "add",
            "args": {"x": 3, "y": 4}
        })
    elif "subtract" in user_input:
        return json.dumps({
            "tool": "subtract",
            "args": {"x": 10, "y": 2}
        })
    else:
        return json.dumps({
            "tool": None,
            "message": "Sorry, I can only help with 'add' or 'subtract'."
        })
