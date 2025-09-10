import os
import sys
from enum import Enum

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class Languages(Enum):
    """Supported Languages"""

    Python = "python"


class PythonDatetimeLibraries(Enum):
    """Supported Libraries"""

    Datetime = "datetime"
    Arrow = "arrow"
    Pendulum = "pendulum"


# Naive prompt template
NAIVE_PROMPT_TEMPLATE = """
Your task is: {task}
"""

# Few-shot prompt template
FEW_SHOT_PROMPT_TEMPLATE = """
Here are a few examples for {language}:

{examples}

Your task:
{task}
"""


def environment_variables_set() -> bool:
    """Check if all required API keys are set in environment variables."""
    if "OPENAI_API_KEY" not in os.environ:
        print("Environment variable OPENAI_API_KEY not set.")
        return False

    if "GEMINI_API_KEY" not in os.environ:
        print("Environment variable GEMINI_API_KEY not set.")
        return False

    if "ANTHROPIC_API_KEY" not in os.environ:
        print("Environment variable ANTHROPIC_API_KEY not set.")
        return False

    return True
