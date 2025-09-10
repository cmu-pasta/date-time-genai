import os
from enum import Enum
from typing import List

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
    # TIMEZONE = "zoneinfo"
    TIME = "time"
    STRING = "str"
    BOOL = "bool"
    FLOAT = "float"


type_mapping = {
    VariableType.DATETIME.value: VariableType.DATETIME,
    VariableType.STRING.value: VariableType.STRING,
    VariableType.TIMESTAMP.value: VariableType.TIMESTAMP,
    # VariableType.TIMEZONE.value: VariableType.TIMEZONE,
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
    # VariableType.TIMEZONE: "timezones()",
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
    # TIMEZONE = "pendulum.Timezone"
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
    # VariableTypePD.TIMEZONE.value: VariableTypePD.TIMEZONE,
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
    # VariableTypePD.TIMEZONE: "pendulum_timezones()",
    VariableTypePD.TIME: "time_strategy()",
    VariableTypePD.TIMEDELTA: "duration_strategy()",
}


#########################################################################
""" Helper functions """


def find_most_recent_subdirectory(parent_directory):
    if not os.path.isdir(parent_directory):
        raise ValueError(f"The path {parent_directory} is not a valid directory.")

    subdirs = [
        os.path.join(parent_directory, d)
        for d in os.listdir(parent_directory)
        if os.path.isdir(os.path.join(parent_directory, d))
    ]

    if not subdirs:
        return None
    most_recent_subdir = max(subdirs, key=os.path.getctime)
    return most_recent_subdir
