
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_first_monday(year: int, month: int) -> pendulum.DateTime:
    # Step 1: Create a pendulum.DateTime object for the first day of the given month and year.
    first_day_of_month = pendulum.datetime(year, month, 1)

    # Step 2: Determine how many days to add to reach the first Monday.
    # pendulum.MONDAY is 1. dt.day_of_week is also 1 for Monday, 2 for Tuesday, etc.
    # If first_day_of_month is Monday (1), days_to_add will be (1 - 1 + 7) % 7 = 0.
    # If first_day_of_month is Tuesday (2), days_to_add will be (1 - 2 + 7) % 7 = 6.
    # If first_day_of_month is Sunday (7), days_to_add will be (1 - 7 + 7) % 7 = 1.
    days_to_add = (pendulum.MONDAY - first_day_of_month.day_of_week + 7) % 7

    # Step 3: Add the calculated number of days to find the first Monday.
    first_monday = first_day_of_month.add(days=days_to_add)

    # Step 4: Return the result as a pendulum.DateTime object.
    return first_monday

# Entry point: find_first_monday(year: int, month: int) -> pendulum.DateTime

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_5_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_find_first_monday(year, month):
    result = find_first_monday(year, month)
    formatted_result = format_value_pd(result, year, month)
    log_file.write(formatted_result + "\n")
