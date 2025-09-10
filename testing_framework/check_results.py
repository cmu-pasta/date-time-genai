import os
import sys
from enum import Enum
from typing import Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


class Status(Enum):
    # The code ran successfully
    PASSED = "passed"

    # The code threw an error
    ERROR = "error"

    # The code did not execute within the time limit
    TIMEOUT = "timeout"


class DiffTestStatus(Enum):
    # The test ran successfully, but the results are the same
    NON_DIFFERENTIATING = "non-differentiating"

    # The test ran successfully, but the results are different
    DIFFERENTIATING = "differentiating"

    # The test is a false positive
    FALSE_POSITIVE = "false-positive"

    # The test ran successfully, but the inputs to the tests were not the same
    INPUT_ERROR = "input-error"

    # One of the tests ran and the other did not produce any results
    PROGRAM_ERROR = "program-error"

    # One of the tests timed out mid execution and produced partial results
    TIMEOUT = "timeout"


def compare_diff_test_results(file1, file2, file_name) -> Tuple[DiffTestStatus, float]:
    f1_lines = []
    f2_lines = []

    with open(file1, "r") as f1, open(file2, "r") as f2:
        f1_lines = f1.readlines()
        f2_lines = f2.readlines()

    if len(f1_lines) == 0:
        print(f"  \\_{file_name} had a runtime error.")
        return DiffTestStatus.PROGRAM_ERROR, 0.0

    # Check if the tests completed
    if len(f1_lines) != len(f2_lines):
        # Check if test 2 even ran?
        if len(f2_lines) == 0:
            print(f"  \\_{file_name} had a runtime error.")
            return DiffTestStatus.PROGRAM_ERROR, 0.0
        else:
            print(f"  \\_{file_name} timed out.")
            return DiffTestStatus.TIMEOUT, 0.0

    # If the tests completed, check if the results are the same
    else:
        differing_results = 0
        for line1, line2 in zip(f1_lines, f2_lines):
            # Check if the results are the same
            if line1 != line2:

                # Check if the inputs are the same
                if line1.split(",")[1:] != line2.split(",")[1:]:
                    print(f"  \\_**ATTENTION: {file_name} has an input error.**")
                    return DiffTestStatus.INPUT_ERROR, 0.0

                # Check if the outputs are the same
                if line1 != line2:
                    differing_results += 1

        total_lines = len(f1_lines)
        # No need for division by zero check here since we already checked if the tests completed.
        differing_percentage = (differing_results / total_lines) * 100

        if differing_percentage == 0.0:
            print(f"  \\_{file_name} is a non-differentiating test.")
            return DiffTestStatus.NON_DIFFERENTIATING, differing_percentage

        elif differing_percentage <= config.THRESHOLD:
            print(
                f"  \\_**ATTENTION: {file_name} is a differentiating test with {differing_percentage:.2f}% differing lines.**"
            )
            return DiffTestStatus.DIFFERENTIATING, differing_percentage

        else:
            print(
                f"  \\_{file_name} is probably a false positive with {differing_percentage:.2f}% differing lines."
            )
            return DiffTestStatus.FALSE_POSITIVE, differing_percentage
