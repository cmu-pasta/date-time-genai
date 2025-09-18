
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def next_friday_13th(after_dt: pendulum.DateTime) -> pendulum.Date:
    """
    Find the next occurrence of Friday the 13th strictly after the given datetime.

    Parameters:
        after_dt (pendulum.DateTime): The datetime after which to search.

    Returns:
        pendulum.Date: The date of the next Friday the 13th.
    """
    # Start from the date component of the provided datetime
    current_date = after_dt.date()
    year = current_date.year
    month = current_date.month

    # Choose the first candidate 13th strictly after the given date
    if current_date.day < 13:
        candidate = pendulum.date(year, month, 13)
    else:
        # Move to the 13th of the next month
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        candidate = pendulum.date(year, month, 13)

    # Iterate month-by-month until the 13th falls on a Friday
    while candidate.day_of_week != pendulum.FRIDAY:
        y = candidate.year
        m = candidate.month
        if m == 12:
            y += 1
            m = 1
        else:
            m += 1
        candidate = pendulum.date(y, m, 13)

    return candidate

# Entry point: next_friday_13th(after_dt: pendulum.DateTime) -> pendulum.Date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_38txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_next_friday_13th(after_dt):
    result = next_friday_13th(after_dt)
    formatted_result = format_value_pd(result, after_dt)
    log_file.write(formatted_result + "\n")
