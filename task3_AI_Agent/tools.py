
import ast
import operator
from datetime import datetime
from collections import Counter
import re


# Safe calculator
def calculate(expression):
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in allowed_operators:
                raise ValueError("Operator not allowed")

            if isinstance(node.op, ast.Pow) and abs(node.right.value) > 100:
                raise ValueError("Exponent is too large")

            return allowed_operators[op_type](
                evaluate(node.left),
                evaluate(node.right)
            )

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in allowed_operators:
                raise ValueError("Operator not allowed")
            return allowed_operators[op_type](evaluate(node.operand))

        raise ValueError("Enter a valid arithmetic expression")

    try:
        tree = ast.parse(expression, mode="eval")
        result = evaluate(tree.body)

        if isinstance(result, complex) or abs(result) > 1e100:
            return "Error: Result is too large."

        return result
    except (ValueError, SyntaxError, TypeError, ZeroDivisionError,
            OverflowError, AttributeError):
        return "Error: Please enter a valid calculation."


# Current date and time
def get_datetime():
    now = datetime.now()
    return now.strftime("%A, %d %B %Y | %I:%M:%S %p")


# Text analyzer
def analyze_text(text):
    words = re.findall(r"\b[\w'-]+\b", text)
    sentences = re.findall(r"[^.!?]+(?:[.!?]+|$)", text)
    characters = len(text)
    characters_without_spaces = len(
        re.sub(r"\s", "", text)
    )

    word_counts = Counter(word.lower() for word in words)
    common_words = word_counts.most_common(5)

    return {
        "words": len(words),
        "characters": characters,
        "characters_without_spaces": characters_without_spaces,
        "sentences": len([s for s in sentences if s.strip()]),
        "most_common_words": common_words,
    }


# Simple rule-based agent
def run_agent(user_input):
    message = user_input.strip()
    lower = message.lower()

    if not message:
        return "Please enter a message."

    if any(word in lower for word in ["hello", "hi", "hey"]):
        return (
            "Hello! I am Astra, your multi-tool AI agent. "
            "I can calculate expressions, show the date and time, "
            "and analyze text. How can I help you?"
        )

    if any(term in lower for term in [
        "date", "time", "today", "current day"
    ]):
        return f"The current date and time is: {get_datetime()}"

    if lower.startswith("calculate "):
        expression = message[len("calculate "):].strip()
        return f"Calculation result: {calculate(expression)}"

    if lower.startswith("calc "):
        expression = message[len("calc "):].strip()
        return f"Calculation result: {calculate(expression)}"

    if lower.startswith("analyze:"):
        text = message.split(":", 1)[1].strip()
        if not text:
            return "Please provide text after 'analyze:'."

        result = analyze_text(text)
        return (
            f"Text Analysis Results\n\n"
            f"Words: {result['words']}\n\n"
            f"Characters: {result['characters']}\n\n"
            f"Characters without spaces: "
            f"{result['characters_without_spaces']}\n\n"
            f"Sentences: {result['sentences']}\n\n"
            f"Most common words: {result['most_common_words']}"
        )

    if "help" in lower:
        return (
            "Here is what I can do:\n\n"
            "1. Calculate: calculate 25 * 4\n"
            "2. Date and time: What is the current time?\n"
            "3. Analyze text: analyze: Python is easy to learn.\n"
            "4. Chat: Say hello or ask a general question."
        )

    return (
        "I understood your message, but I do not have a specialized "
        "tool for that request yet. Type 'help' to see available "
        "commands. I can also respond to simple greetings."
    )
