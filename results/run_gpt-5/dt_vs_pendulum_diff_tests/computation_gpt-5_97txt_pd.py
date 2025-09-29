
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def to_buddhist_year(gregorian_date: pendulum.Date) -> int:
    """
    Convert a Gregorian date (CE) to its Thai Buddhist Era (BE) year number.
    Note:
    - The Thai Buddhist calendar is 543 years ahead of the Gregorian calendar.
    - Month and day are identical to the Gregorian date.
    - Returning the BE year as an integer avoids invalid constructions like BE 2555-02-29
      under proleptic Gregorian rules, while still fully determining the Buddhist date.
    """
    # Validate that the input is a pendulum.Date
    if not isinstance(gregorian_date, pendulum.Date):
        # If someone passes a DateTime, we can safely convert to Date
        if isinstance(gregorian_date, pendulum.DateTime):
            gregorian_date = gregorian_date.date()
        else:
            raise TypeError("Input must be a pendulum.Date or pendulum.DateTime")

    be_year = gregorian_date.year + 543
    return be_year

# Entry point: to_buddhist_year(gregorian_date: pendulum.Date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_97txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_to_buddhist_year(gregorian_date):
    result = to_buddhist_year(gregorian_date)
    formatted_result = format_value_pd(result, gregorian_date)
    log_file.write(formatted_result + "\n")
