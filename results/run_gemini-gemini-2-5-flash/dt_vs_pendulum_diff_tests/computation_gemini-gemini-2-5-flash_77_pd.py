
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_columbus_day(year: int) -> pendulum.Date:
    # Step 1: Create a pendulum.Date object for October 1st of the given year.
    october_first = pendulum.date(year, 10, 1)

    # Step 2: Find the first Monday of October.
    # We calculate the difference in days from October 1st to the next (or current) Monday.
    # pendulum.MONDAY is 0, Tuesday is 1, ..., Sunday is 6.
    # (0 - current_day_of_week + 7) % 7 gives days to add to reach the *next* Monday,
    # or 0 if current day is Monday.
    
    # Calculate days to add to get to the first Monday on or after october_first
    # Example: If october_first.day_of_week (e.g., Tuesday=1), then (0 - 1 + 7) % 7 = 6 days.
    # If october_first.day_of_week (e.g., Monday=0), then (0 - 0 + 7) % 7 = 0 days.
    days_to_add_for_first_monday = (pendulum.MONDAY - october_first.day_of_week + 7) % 7
    first_monday_of_october = october_first.add(days=days_to_add_for_first_monday)

    # Step 3: Add one week (7 days) to get the second Monday of October.
    columbus_day = first_monday_of_october.add(weeks=1)

    # Step 4: Return the result as a pendulum.Date object.
    return columbus_day

# Entry point: find_columbus_day(year: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_77_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_columbus_day(year):
    result = find_columbus_day(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
