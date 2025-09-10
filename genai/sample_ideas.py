import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

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
a. Please only output ideas that involve entities such as dates, datetimes, times, timezones, or timestamps.
b. The result of the idea should be a single entity.
c. Please note that the ideas should be unique and non-trivial.
d. Output all your ideas as a list (one idea per line).
e. Please output only the ideas and nothing else.

OUTPUT FORMAT:
1. <Idea 1>
2. <Idea 2>
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
    print(f"  \\_Generating list of interesting ideas.")

    user_prompt = GENERATE_IDEAS_TASK.format(n=config.IDEAS)
    samples = ai_model.sample(IDEAS_SYSTEM_PROMPT, user_prompt, n=1)

    result_dir = config.OUTPUT_DIR
    os.makedirs(result_dir, exist_ok=True)
    result_output_path = os.path.join(
        result_dir, config.IDEAS_PATH.format(model=ai_model.model_name)
    )
    Path(result_output_path).write_text(samples[0])

    if not validate_ideas_list(result_output_path):
        print(
            f"Warning: Validation failed for the list of ideas from model {ai_model.model_name}."
        )

    return result_output_path
