import os
import sys
from enum import Enum
from typing import List, Tuple

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


#########################################################################
"""Class to store the generated computation"""


class Computation:
    def __init__(
        self,
        entry_point_name: str,
        arguments_count: int,
        argument_names: List[str],
        argument_types: List,
        return_type,
        code: str,
        imports: str,
    ):
        self.entry_point_name = entry_point_name
        self.arguments_count = arguments_count
        self.argument_names = argument_names
        self.argument_types = argument_types
        self.return_type = return_type
        self.code = code
        self.imports = imports


#########################################################################
""" Data Structures for datetime library"""


class VariableType(Enum):
    DATE = "date"
    DATETIME = "datetime"
    TIMEDELTA = "timedelta"
    TIMESTAMP = "int"
    TIMEZONE = "ZoneInfo"
    TIME = "time"
    STRING = "str"
    BOOL = "bool"
    FLOAT = "float"


type_mapping = {
    VariableType.DATETIME.value: VariableType.DATETIME,
    VariableType.STRING.value: VariableType.STRING,
    VariableType.TIMESTAMP.value: VariableType.TIMESTAMP,
    VariableType.TIMEZONE.value: VariableType.TIMEZONE,
    VariableType.TIME.value: VariableType.TIME,
    VariableType.DATE.value: VariableType.DATE,
    VariableType.BOOL.value: VariableType.BOOL,
    VariableType.FLOAT.value: VariableType.FLOAT,
    VariableType.TIMEDELTA.value: VariableType.TIMEDELTA,
}

generator_mapping = {
    VariableType.DATETIME: "datetime_strategy()",
    VariableType.STRING: "string_strategy()",
    VariableType.TIMESTAMP: "timestamp_strategy()",
    VariableType.TIMEZONE: "timezone_strategy()",
    VariableType.TIMEDELTA: "duration_strategy()",
    VariableType.TIME: "time_strategy()",
    VariableType.DATE: "date_strategy()",
    VariableType.BOOL: "bool_strategy()",
    VariableType.FLOAT: "float_strategy()",
}


#########################################################################
""" Data Structures for pendulum library """


class VariableTypePD(Enum):
    DATE = "pendulum.Date"
    DATETIME = "pendulum.DateTime"
    TIMEDELTA = "pendulum.Duration"
    TIMESTAMP = "int"
    TIMEZONE = "pendulum.Timezone"
    TIME = "pendulum.Time"
    STRING = "str"
    BOOL = "bool"
    FLOAT = "float"


type_mapping_pd = {
    VariableTypePD.DATETIME.value: VariableTypePD.DATETIME,
    VariableTypePD.TIMESTAMP.value: VariableTypePD.TIMESTAMP,
    VariableTypePD.STRING.value: VariableTypePD.STRING,
    VariableTypePD.BOOL.value: VariableTypePD.BOOL,
    VariableTypePD.FLOAT.value: VariableTypePD.FLOAT,
    VariableTypePD.DATE.value: VariableTypePD.DATE,
    VariableTypePD.TIMEZONE.value: VariableTypePD.TIMEZONE,
    VariableTypePD.TIME.value: VariableTypePD.TIME,
    VariableTypePD.TIMEDELTA.value: VariableTypePD.TIMEDELTA,
}

generator_mapping_pd = {
    VariableTypePD.DATETIME: "datetime_strategy()",
    VariableTypePD.TIMESTAMP: "timestamp_strategy()",
    VariableTypePD.STRING: "string_strategy()",
    VariableTypePD.BOOL: "bool_strategy()",
    VariableTypePD.FLOAT: "float_strategy()",
    VariableTypePD.DATE: "date_strategy()",
    VariableTypePD.TIMEZONE: "timezone_strategy()",
    VariableTypePD.TIME: "time_strategy()",
    VariableTypePD.TIMEDELTA: "duration_strategy()",
}


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
