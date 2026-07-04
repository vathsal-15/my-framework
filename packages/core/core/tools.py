class Tool:
    def __init__(self, name: str, description: str, func):
        self.name = name
        self.description = description
        self.func = func

    def run(self, **kwargs):
        return self.func(**kwargs)


def calculator(expression: str) -> str:
    """A simple, safe calculator tool for basic arithmetic."""
    try:
        allowed_chars = "0123456789+-*/(). "
        if not all(c in allowed_chars for c in expression):
            return "Error: invalid characters in expression"
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


calculator_tool = Tool(
    name="calculator",
    description="Evaluates a basic arithmetic expression, e.g. '2 + 2' or '15 * 3'.",
    func=calculator
)
from datetime import datetime

def current_datetime(format: str = "") -> str:
    """Returns the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


datetime_tool = Tool(
    name="current_datetime",
    description="Returns the current date and time. Takes no meaningful argument, pass an empty string.",
    func=current_datetime
)