import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from genai.utils import sanitize_model_name_for_path

IDEAS_SYSTEM_PROMPT = """
You are an expert in the field of date and time computations.
Your goal is to help successfully perform the given task.
"""

GENERATE_IDEAS_TASK = """
GOAL:
Our goal is to generate a list of interesting ideas for date and time computations. 
We want to use these ideas to generate code that exercises various date and time operations.
We want the ideas to be diverse to maximize the coverage of date and time operations.

TASK:
Your task is to come up with a list of {n} interesting ideas for date and time computations.

NOTE:
a. Please only output ideas that involve these entities: **dates**, **datetimes**, **times**, **timezones**, or **timestamps**.
b. The result of the idea should be a single entity.
c. **Please note that the ideas should be unique and non-trivial**.
d. Output all your ideas as a list (one idea per line). Please output only the ideas and nothing else.

SPECIAL REQUESTS:
Since we will use these ideas to generate code later on, please make sure that the code accepts and outputs only the specified types.
Try to avoid non-determinism and randomness in the ideas. For example, an idea that involves the current time or date will have a different output when run multiple times.
Please make sure that the ideas will require the use of a variety of library APIs.

OUTPUT FORMAT:
1. <Idea 1>
2. <Idea 2>
...

EXAMPLE:
1. Calculate the number of business days between two dates.
2. Calculate the exact time difference between two timestamps considering daylight saving time.
3. Determine the day name (e.g., Monday, Tuesday) for a given date.
4. Determine the next leap year after a given date.
5. Convert timezones of two timestamps and compare them.
...
"""


def validate_ideas_list(output_path) -> bool:
    """Validate that LLM output contains the expected number of unique ideas."""

    with open(output_path, "r") as file:
        interesting_ideas = file.read()
        interesting_ideas = interesting_ideas.split("\n")

    # Ensure output has exactly the configured number of unique ideas
    return len(set(interesting_ideas)) == config.IDEAS


def sample_ideas(ai_model):
    print(f"Using model: {ai_model.model_name}")

    # Check if IDEAS_PATH variable exists in config
    if not hasattr(config, "IDEAS_PATH"):
        raise AttributeError(
            "Error: IDEAS_PATH variable is not set in config file. Please define IDEAS_PATH in config.py"
        )

    ideas_path = config.IDEAS_PATH

    # Check if the file exists at IDEAS_PATH
    if os.path.exists(ideas_path):
        print(
            f"  \\_Ideas file already exists at {ideas_path}. Returning existing file."
        )
        return ideas_path

    # File doesn't exist, so generate ideas
    print(
        f"  \\_Ideas file not found at {ideas_path}. Generating list of interesting ideas."
    )

    user_prompt = GENERATE_IDEAS_TASK.format(n=config.IDEAS)
    samples = ai_model.sample(IDEAS_SYSTEM_PROMPT, user_prompt, n=1)

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(ideas_path), exist_ok=True)

    # Write ideas to the specified path
    Path(ideas_path).write_text(samples[0])

    if not validate_ideas_list(ideas_path):
        print(
            f"Warning: Validation failed for the list of ideas from model {ai_model.model_name}."
        )

    return ideas_path
