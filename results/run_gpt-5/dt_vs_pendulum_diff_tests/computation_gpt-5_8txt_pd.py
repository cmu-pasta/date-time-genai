
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def last_day_of_month(date_input: pendulum.Date) -> pendulum.Date:
    """
    Find the last day of the month for the given pendulum.Date.
    """
    # Convert to DateTime to use end_of('month'), then get the date part
    last_day = pendulum.datetime(date_input.year, date_input.month, date_input.day).end_of('month').date()
    return last_day

# Entry point: last_day_of_month(date_input: pendulum.Date) -> pendulum.Date

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_8txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_last_day_of_month(date_input):
    result = last_day_of_month(date_input)
    formatted_result = format_value_pd(result, date_input)
    log_file.write(formatted_result + "\n")
