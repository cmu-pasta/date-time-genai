import os
import shutil
import sys
from typing import Any, Dict

# Add the parent directory to the path so we can import from config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    CODE_FILE_PATH,
    DEFAULT_OUTPUT_DIR,
    DEMO_DIR,
    DIFF_TEST_LOGS_DT_VS_PD,
    DIFF_TESTS_DT_VS_PD,
    LOG_FILE_DIR,
    LOG_FILE_PATH,
)

from .log_parser import parse_log_file

CREATE_STANDALONE_EXECUTABLE_PROMPT = """
Please create a standalone executable for these computations.

Test file 1:
{computation1}

Test file 2:
{computation2}

Please note that:
- You can drop all logging and output formatting methods.
- There should be only one main method that runs each of the test methods with four hardcoded inputs.
- Keep it as simple as possible while ensuring that the source code of the methods under test is not changed.
- Make sure that everything is contained in a single code block and that it is executable.

Here are the inputs for the test files:
(The inputs are comma separated values for the parameters of the methods under test. If they are set to None, then skip them.) 

Please use these, create appropriate objects when necessary and pass them to the methods under test. Assert that the results are the same for these inputs.
{input1}
{input2}

Assert that the results are not the same for these inputs:
{input3}
{input4}

Output Format:
Reasoning steps:
1. <Step 1 of reasoning>
2. <Step 2 of reasoning>
...

```{language}
<code with main method>
``` 
"""

# Get the absolute path to testing_framework directory
current_dir = os.path.dirname(os.path.abspath(__file__))  # Current directory (analyze)
parent_dir = os.path.dirname(current_dir)  # Parent directory (datetime_genai)
testing_framework_dir = os.path.join(parent_dir, "testing_framework")

sys.path.append(testing_framework_dir)
from common import find_most_recent_subdirectory
from prompts import FEW_SHOT_PROMPT_TEMPLATE, SYSTEM_PROMPT_TEMPLATE, Languages
from sample_llm import OpenAIModel


def copy_files(results: Dict[str, Any], output_dir: str = DEFAULT_OUTPUT_DIR):
    # Make a copy of the log file in the output directory
    shutil.copy(LOG_FILE_PATH, os.path.join(output_dir, "results_log.txt"))

    # Iterate over the results and copy the files where the status is DIFFERENTIATING
    for result in results["raw_results"]:
        if (
            result["status"] == "DIFFERENTIATING"
            or result["status"] == "FALSE_POSITIVE"
        ):
            print(
                f"Copying files for {result['computation_id']} with status {result['status']}"
            )
            # Make a new directory for the computation
            comp_dir = os.path.join(
                output_dir, f"computation_{result['computation_id']}"
            )
            os.makedirs(comp_dir)

            # Copy the log files
            shutil.copy(
                os.path.join(
                    LOG_FILE_DIR,
                    DIFF_TEST_LOGS_DT_VS_PD,
                    f"log_computations_{result['model']}_{result['computation_id']}_dt.txt",
                ),
                os.path.join(comp_dir, f"dt_log.txt"),
            )
            shutil.copy(
                os.path.join(
                    LOG_FILE_DIR,
                    DIFF_TEST_LOGS_DT_VS_PD,
                    f"log_computations_{result['model']}_{result['computation_id']}_pd.txt",
                ),
                os.path.join(comp_dir, f"pd_log.txt"),
            )

            # Copy the code files

            # Get run_id
            run_id = find_most_recent_subdirectory(CODE_FILE_PATH)
            code_files_location = os.path.join(run_id, DIFF_TESTS_DT_VS_PD)
            shutil.copy(
                os.path.join(
                    code_files_location,
                    f"computations_{result['model']}_{result['computation_id']}_dt.py",
                ),
                os.path.join(comp_dir, f"dt_code.py"),
            )
            shutil.copy(
                os.path.join(
                    code_files_location,
                    f"computations_{result['model']}_{result['computation_id']}_pd.py",
                ),
                os.path.join(comp_dir, f"pd_code.py"),
            )


def create_standalone_executables(
    output_dir: str = DEFAULT_OUTPUT_DIR,
    demonstration_dir: str = DEMO_DIR,
):
    for subdir in os.listdir(output_dir):
        print(f"\nProcessing {subdir}")
        if os.path.isdir(os.path.join(output_dir, subdir)):
            # Get the log file
            log_file_dt = os.path.join(output_dir, subdir, "dt_log.txt")
            log_file_pd = os.path.join(output_dir, subdir, "pd_log.txt")
            if not os.path.exists(log_file_dt) or not os.path.exists(log_file_pd):
                print(f"  \\_ Unexpected Error: Log file not found for {subdir}")
                continue

            # step 1: find out the differentiating inputs for each computation
            differentiating_inputs = []
            non_differentiating_inputs = []
            with open(log_file_dt, "r") as f_dt, open(log_file_pd, "r") as f_pd:
                # Check these files and find lines that differ
                for line_dt, line_pd in zip(f_dt, f_pd):
                    if line_dt != line_pd and len(differentiating_inputs) < 2:
                        print(f"  \\_ Different line in {subdir}")

                        # Split the lines into parts for better comparison
                        parts_dt = line_dt.strip().split(", ")
                        parts_pd = line_pd.strip().split(", ")

                        # ANSI color codes
                        RED = "\033[91m"  # Bright red
                        GREEN = "\033[92m"  # Bright green
                        RESET = "\033[0m"  # Reset color

                        # Print the lines with colored differences
                        print("DT: ", end="")
                        for i, part in enumerate(parts_dt):
                            if i < len(parts_pd) and part != parts_pd[i]:
                                print(
                                    f"{RED}{part}{RESET}",
                                    end=", " if i < len(parts_dt) - 1 else "\n",
                                )
                            else:
                                print(part, end=", " if i < len(parts_dt) - 1 else "\n")

                        print("PD: ", end="")
                        for i, part in enumerate(parts_pd):
                            if i < len(parts_dt) and part != parts_dt[i]:
                                print(
                                    f"{GREEN}{part}{RESET}",
                                    end=", " if i < len(parts_pd) - 1 else "\n",
                                )
                            else:
                                print(part, end=", " if i < len(parts_pd) - 1 else "\n")

                        print("-" * 80)  # Separator line

                        # Add the inputs to the list
                        differentiating_inputs.append(line_dt.strip().split(",")[1:])
                    elif line_dt == line_pd and len(non_differentiating_inputs) < 2:
                        print(f"  \\_ Same line in {subdir}")

                        # print the inputs
                        print(line_dt.strip().split(",")[1:])
                        print("-" * 80)  # Separator line
                        non_differentiating_inputs.append(
                            line_dt.strip().split(",")[1:]
                        )

            # step 2: create a standalone execution file for each computation
            # read the demonstration file
            demonstration_file = os.path.join(
                demonstration_dir, "create_standalone_executable.txt"
            )
            with open(demonstration_file, "r") as f:
                demonstration = f.read()

            # system prompt
            system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
                language=Languages.Python.value
            )

            model_gpt_4o = OpenAIModel(system_prompt, "gpt-4o")

            # read datetime code
            dt_code = os.path.join(output_dir, subdir, "dt_code.py")
            with open(dt_code, "r") as f:
                dt_code = f.read()

            # read pendulum code
            pd_code = os.path.join(output_dir, subdir, "pd_code.py")
            with open(pd_code, "r") as f:
                pd_code = f.read()

            # Instead of skipping, prepare inputs with None values for missing ones
            non_diff_input1 = (
                non_differentiating_inputs[0]
                if len(non_differentiating_inputs) > 0
                else None
            )
            non_diff_input2 = (
                non_differentiating_inputs[1]
                if len(non_differentiating_inputs) > 1
                else None
            )
            diff_input1 = (
                differentiating_inputs[0] if len(differentiating_inputs) > 0 else None
            )
            diff_input2 = (
                differentiating_inputs[1] if len(differentiating_inputs) > 1 else None
            )

            if len(differentiating_inputs) < 2 or len(non_differentiating_inputs) < 2:
                print(f"  \\_ Warning: Insufficient inputs for {subdir}")
                print(
                    f"    Found {len(differentiating_inputs)} differentiating inputs (need 2)"
                )
                print(
                    f"    Found {len(non_differentiating_inputs)} non-differentiating inputs (need 2)"
                )
                print("    Using None for missing inputs")

            prompt = FEW_SHOT_PROMPT_TEMPLATE.format(
                language=Languages.Python.value,
                examples=demonstration,
                task=CREATE_STANDALONE_EXECUTABLE_PROMPT.format(
                    language=Languages.Python.value,
                    computation1=dt_code,
                    computation2=pd_code,
                    input1=non_diff_input1,
                    input2=non_diff_input2,
                    input3=diff_input1,
                    input4=diff_input2,
                ),
            )

            for _ in range(3):
                # generate the standalone execution file
                response = model_gpt_4o.sample(prompt, n=1)
                standalone_code = response[0]

                # extract the code from the ```python``` tags
                standalone_code = standalone_code.split("```python")[1].split("```")[0]

                # create a standalone execution file
                standalone_file = os.path.join(output_dir, f"standalone_{subdir}.py")
                # save the standalone execution file
                with open(standalone_file, "w") as f:
                    f.write(standalone_code)

                # run the standalone execution file and check if it runs successfully
                try:
                    os.system(f"python {standalone_file}")
                    print(f"  \\_ Standalone file ran successfully for {subdir}")
                    break
                except Exception as e:
                    print(f"  \\_ Error: {e}")
                    print(f"  \\_ Standalone file failed to run for {subdir}")
                    continue

            print(f"  \\_ Standalone file saved to {standalone_file}")


def analyze_results(output_dir: str = DEFAULT_OUTPUT_DIR):
    # Delete the output directory if it exists
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    results = parse_log_file()
    copy_files(results, output_dir)
    print("Copied files to output directory")

    create_standalone_executables()
    print("Created standalone executables")
