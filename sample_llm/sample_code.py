import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from genai.utils import FEW_SHOT_PROMPT_TEMPLATE, sanitize_model_name_for_path

COMPUTATION_SYSTEM_PROMPT = """
You are an expert in the field of date and time computations.
Your goal is to help successfully implement the given computation task.
"""

DT_PROMPT_RULE = "Only use input and output types from this list of standard library types: [booleans, dates, datetimes, floats, integers, timedeltas, times, ZoneInfo]."
PENDULUM_PROMPT_RULE = "Only use input and output types from this list of pendulum library types: [booleans, pendulum.Date, pendulum.DateTime, floats, integers, pendulum.Duration, pendulum.Time, pendulum.Timezone]."

# Task to generate random computations using the datetime libraries
GENERATE_COMPUTATION_TASK = """
GOAL:
Our goal is to generate a code that implements the given idea.

IDEA:
Here is an interesting idea for a computation:
{idea}

TASK:
Your task is to write a correct and complete code snippet that implements this computation using the {library} library only. 

NOTE:
a. Please write a code snippet that implements this computation using the {library} library. 
b. Make sure to include all the necessary imports and highlight the code using the ```{language} ... ``` tag.
c. Please output the entires solution in a single code block in the end.
d. Make sure that the method accepts the necessary inputs and returns the expected output.  
e. Do not input or output any complex data types like lists, tuples, sets, or dictionaries.
f. Always specify the entry point of the code snippet.
g. {rule}
h. Avoid having default values for the arguments.

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


def sample_code_set(
    ai_model, programming_lang, py_library, ideas_file, code_set_dir, example, rule
):
    print(f"\nUsing model: {ai_model.model_name}")
    print(f"  \\_Generating code snippets that implement the given ideas.")

    # Create the output directory if it doesn't exist
    os.makedirs(code_set_dir, exist_ok=True)

    with open(ideas_file, "r") as file:
        interesting_ideas = file.read()
        interesting_ideas = interesting_ideas.split("\n")

    for i in range(min(config.IDEAS, len(interesting_ideas))):
        user_prompt = FEW_SHOT_PROMPT_TEMPLATE.format(
            language=programming_lang,
            examples=example,
            task=GENERATE_COMPUTATION_TASK.format(
                idea=interesting_ideas[i],
                library=py_library,
                language=programming_lang,
                rule=rule,
            ),
        )

        output_path = os.path.join(
            code_set_dir,
            config.COMPUTATION_PATH.format(
                model=sanitize_model_name_for_path(ai_model.model_name),
                i=i,
            ),
        )

        # Retry logic: attempt up to MAX_RETRIES times
        success = False
        for attempt in range(config.MAX_RETRIES):
            try:
                sampled_code = ai_model.sample(COMPUTATION_SYSTEM_PROMPT, user_prompt)
                Path(output_path).write_text(sampled_code[0])

                if validate_computations(output_path):
                    print(
                        f"    \\_Computation {i} from model {ai_model.model_name} generated successfully."
                    )
                    success = True
                    break
                else:
                    print(
                        f"    \\_Attempt {attempt + 1}/{config.MAX_RETRIES}: Validation failed for computation {i} from model {ai_model.model_name}."
                    )
                    if os.path.exists(output_path):
                        os.remove(output_path)
            except Exception as e:
                print(
                    f"    \\_Attempt {attempt + 1}/{config.MAX_RETRIES}: Error generating computation {i} from model {ai_model.model_name}: {e}"
                )
                if os.path.exists(output_path):
                    os.remove(output_path)

        if not success:
            print(
                f"    \\_Warning: Failed to generate valid computation {i} from model {ai_model.model_name} after {config.MAX_RETRIES} attempts."
            )


def sample_dt_vs_dt_code_sets(
    ai_model,
    programming_lang,
    ideas_file,
):
    print(f"\nSampling DT vs DT Code Sets")

    # Read example for Few-shot prompt
    example = ""
    with open(config.DT_GENERATION_DEMONSTRATION, "r") as file:
        example = file.read()

    # Sample DT vs DT Code Set A
    sample_code_set(
        ai_model,
        programming_lang,
        config.PythonDatetimeLibraries.Datetime,
        ideas_file,
        os.path.join(config.OUTPUT_DIR, config.OUTPUT_DIR_DT_A),
        example,
        DT_PROMPT_RULE,
    )

    # Sample DT vs DT Code Set B
    sample_code_set(
        ai_model,
        programming_lang,
        config.PythonDatetimeLibraries.Datetime,
        ideas_file,
        os.path.join(config.OUTPUT_DIR, config.OUTPUT_DIR_DT_B),
        example,
        DT_PROMPT_RULE,
    )


# PRECONDITION: DT_A is already sampled.
def sample_pendulum_code_sets(
    ai_model,
    programming_lang,
    ideas_file,
):
    print(f"\nSampling Pendulum Code Set")

    # Read example for Few-shot prompt
    example = ""
    with open(config.PENDULUM_GENERATION_DEMONSTRATION, "r") as file:
        example = file.read()

    # Sample Pendulum Code Set
    sample_code_set(
        ai_model,
        programming_lang,
        config.PythonDatetimeLibraries.Pendulum,
        ideas_file,
        os.path.join(config.OUTPUT_DIR, config.OUTPUT_DIR_PENDULUM),
        example,
        PENDULUM_PROMPT_RULE,
    )
