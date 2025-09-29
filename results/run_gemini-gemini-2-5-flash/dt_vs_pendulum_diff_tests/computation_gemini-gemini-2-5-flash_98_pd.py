
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_indigenous_peoples_day(year: int) -> pendulum.Date:
    # Step 1: Create a date object for the first day of October in the given year.
    # We use pendulum.date for just the date component.
    october_first = pendulum.date(year, 10, 1)

    # Step 2: Find the first Monday of October using first_of_month(pendulum.MONDAY).
    first_monday_of_october = october_first.first_of_month(pendulum.MONDAY)

    # Step 3: Add 7 days to the first Monday to get the second Monday.
    indigenous_peoples_day = first_monday_of_october.add(days=7)

    # Step 4: Return the calculated date.
    return indigenous_peoples_day

# Entry point: find_indigenous_peoples_day(year: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_98_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_indigenous_peoples_day(year):
    result = find_indigenous_peoples_day(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
