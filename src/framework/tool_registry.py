# tool_registry.py

class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, func, description=""):
        self.tools[name] = {"func": func, "description": description}

    def list_tools(self):
        return self.tools

    def get(self, name):
        return self.tools.get(name)
