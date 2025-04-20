def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def register_tools(registry):
    registry.register("add", add, "Add two numbers")
    registry.register("subtract", subtract, "Subtract two numbers")
