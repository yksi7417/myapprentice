import importlib
import pkgutil


def load_plugins(registry):
    for finder, name, ispkg in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"src.tool_plugins.{name}")
        if hasattr(module, "register_tools"):
            module.register_tools(registry)
