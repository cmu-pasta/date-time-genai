DATETIME_DIFF_TEMPLATE_PENDULUM = """
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

{function_source}

def format_value_pd(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, pendulum.DateTime):
            formatted_values.append(value.to_iso8601_string()[:-1])
        elif isinstance(value, pendulum.Date):
            formatted_values.append(value.to_date_string())
        elif isinstance(value, pendulum.Time):
            # Format time in the same way as datetime.time.isoformat() does
            formatted_time = (
                str(value.hour).zfill(2)
                + ":"
                + str(value.minute).zfill(2)
                + ":"
                + str(value.second).zfill(2)
            )
            if value.microsecond:
                # Padding microseconds to 6 digits
                formatted_time += "." + str(value.microsecond).zfill(6)
            formatted_values.append(formatted_time)
        elif isinstance(value, pendulum.Duration):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists("{DIFF_TEST_LOGS_DIR}"):
    os.makedirs("{DIFF_TEST_LOGS_DIR}")
log_file = open(os.path.join("{DIFF_TEST_LOGS_DIR}", "log_{file_name}_pendulum.txt"), "w")

@seed({seed})
@settings(max_examples={max_examples}, deadline=None, derandomize=True)
@given({generators})
def test_{function_name}({args}):
    result = {function_name}({args})
    formatted_result = format_value_pd(result, {args})
    log_file.write(formatted_result + "\\n")
"""
