
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_first_monday_of_month(year: int, month: int) -> pendulum.Date:
    # Step 1: Create a pendulum.Date object for the first day of the given month and year.
    first_day_of_month = pendulum.date(year, month, 1)

    # Step 2: Determine the day of the week for this first day.
    # pendulum.day_of_week returns 1 for Monday, 2 for Tuesday, ..., 7 for Sunday.
    current_day_of_week = first_day_of_month.day_of_week

    # Step 3: Calculate the number of days to add to reach the first Monday.
    # We want to reach pendulum.MONDAY (which is 1).
    # The formula (desired_day_of_week - current_day_of_week + 7) % 7 gives the days to add.
    days_to_add = (pendulum.MONDAY - current_day_of_week + 7) % 7

    # Step 4: Add the calculated number of days to find the first Monday.
    first_monday = first_day_of_month.add(days=days_to_add)

    # Step 5: Return the result.
    return first_monday

# Entry point: find_first_monday_of_month(year: int, month: int) -> pendulum.Date

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
def test_find_first_monday_of_month(year, month):
    result = find_first_monday_of_month(year, month)
    formatted_result = format_value_pd(result, year, month)
    log_file.write(formatted_result + "\n")
