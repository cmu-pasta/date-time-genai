DATETIME_DIFF_TEMPLATE = """
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

{function_source}

def format_value_dt(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, datetime):
            formatted_values.append(value.isoformat())
        elif isinstance(value, date):
            # Use strftime to format the date similar to to_date_string()
            formatted_values.append(value.strftime("%Y-%m-%d"))
        elif isinstance(value, time):
            formatted_values.append(value.isoformat())
        elif isinstance(value, timedelta):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists("{DIFF_TEST_LOGS_DIR}"):
    os.makedirs("{DIFF_TEST_LOGS_DIR}")
log_file = open(os.path.join("{DIFF_TEST_LOGS_DIR}", "log_{file_name}_{test_a_or_b}.txt"), "w")

@seed({seed})
@settings(max_examples={max_examples}, deadline=None, derandomize=True)
@given({generators})
def test_{function_name}({args}):
    result = {function_name}({args})
    formatted_result = format_value_dt(result, {args})
    log_file.write(formatted_result + "\\n")
"""
