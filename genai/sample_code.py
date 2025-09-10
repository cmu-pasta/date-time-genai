import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

from .utils import FEW_SHOT_PROMPT_TEMPLATE

COMPUTATION_SYSTEM_PROMPT = """
You are an expert in the field of date and time computations.
Your goal is to help successfully implement the given computation task.
"""

# Task to generate random computations using the datetime libraries
GENERATE_COMPUTATION_TASK = """
GOAL:
Our goal is to generate a code that implements the given idea.

IDEA:
Here is an interesting idea for a date/time computation:
{idea}

TASK:
Your task is to write a correct and complete code snippet that implements this computation using the {library} library. 

NOTE:
a. Please write a code snippet that implements this computation using the {library} library. 
b. Make sure to include all the necessary imports and highlight the code using the ```{language} ... ``` tag.
c. Please output the entires solution in a single code block in the end.
d. Make sure that the method accepts the necessary inputs and returns the expected output. 
e. Only use input and output types from the standard datetime library from this list: [booleans, dates, datetimes, floats, integers, timedeltas, times, zoneinfo]. 
f. Do not input or output any complex data types like lists, tuples, sets, or dictionaries.
g. Always specify the entry point of the code snippet.

OUTPUT FORMAT:
Let's think step by step to solve this problem.
1. <Step 1 of reasoning>
2. <Step 2 of reasoning>
...

```{language}
<Code Block>
...
# Entry point: <function signature>
``` 
"""


def validate_computations(output_path) -> bool:
    """Validate that LLM output is properly formatted with code blocks and entry point."""

    with open(output_path, "r") as file:
        computation = file.read()

    # Check only one code block exists (two backticks)
    code_block = computation.count("```") == 2

    # Ensure entry point is clearly marked
    entry_point = "# Entry point:" in computation

    return code_block and entry_point


def sample_interesting_computations(
    ai_model, programming_lang, py_library_a, py_library_b, ideas_file
):
    print(f"\nUsing model: {ai_model.model_name}")
    print(f"  \\_Generating code snippets that implement the given ideas.")

    # Read the list of interesting computations:
    with open(ideas_file, "r") as file:
        interesting_ideas = file.read()
        interesting_ideas = interesting_ideas.split("\n")

    # Read example for Few-shot prompt
    example = ""
    with open(config.GENERATION_DEMONSTRATION, "r") as file:
        example = file.read()

    # TODO: Refactor this later.
    # Sample SET A
    print(f"\n  \\_Sampling SET A")
    for i in range(min(config.IDEAS, len(interesting_ideas))):
        user_prompt = FEW_SHOT_PROMPT_TEMPLATE.format(
            language=programming_lang,
            examples=example,
            task=GENERATE_COMPUTATION_TASK.format(
                idea=interesting_ideas[i],
                library=py_library_a,
                language=programming_lang,
            ),
        )
        sampled_code = ai_model.sample(COMPUTATION_SYSTEM_PROMPT, user_prompt)

        result_dir = os.path.join(config.OUTPUT_DIR, config.OUTPUT_DIR_A)
        os.makedirs(result_dir, exist_ok=True)
        output_path = os.path.join(
            result_dir,
            config.COMPUTATION_PATH.format(
                model=ai_model.model_name,
                i=i,
            ),
        )

        Path(output_path).write_text(sampled_code[0])

        if not validate_computations(output_path):
            print(
                f"    \\_Warning: Validation failed for the computation {i} from model {ai_model.model_name}."
            )
            os.remove(output_path)
        else:
            print(
                f"    \\_Computation {i} from model {ai_model.model_name} generated successfully."
            )

    # Sample SET B
    print(f"\n  \\_Sampling SET B")
    for i in range(min(config.IDEAS, len(interesting_ideas))):
        user_prompt = FEW_SHOT_PROMPT_TEMPLATE.format(
            language=programming_lang,
            examples=example,
            task=GENERATE_COMPUTATION_TASK.format(
                idea=interesting_ideas[i],
                library=py_library_b,
                language=programming_lang,
            ),
        )
        sampled_code = ai_model.sample(COMPUTATION_SYSTEM_PROMPT, user_prompt)

        result_dir = os.path.join(config.OUTPUT_DIR, config.OUTPUT_DIR_B)
        os.makedirs(result_dir, exist_ok=True)
        output_path = os.path.join(
            result_dir,
            config.COMPUTATION_PATH.format(
                model=ai_model.model_name,
                i=i,
            ),
        )

        Path(output_path).write_text(sampled_code[0])

        if not validate_computations(output_path):
            print(
                f"    \\_Warning: Validation failed for the computation {i} from model {ai_model.model_name}."
            )
            os.remove(output_path)
        else:
            print(
                f"    \\_Computation {i} from model {ai_model.model_name} generated successfully."
            )
