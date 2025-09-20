
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_memorial_day(year: int) -> pendulum.Date:
    # Step 1: Create a pendulum.Date object for May 31st of the given year.
    # We use pendulum.date() to ensure the return type is pendulum.Date as specified.
    may_31st = pendulum.date(year, 5, 31)

    # Step 2: Determine the day of the week for May 31st.
    # pendulum.MONDAY is 1, TUESDAY is 2, ..., SUNDAY is 7.
    day_of_week_31st = may_31st.day_of_week

    # Step 3: Calculate how many days to subtract to get to the last Monday.
    # If May 31st is a Monday (1), subtract 0 days (1 - 1 = 0).
    # If May 31st is a Tuesday (2), subtract 1 day (2 - 1 = 1) to get Monday.
    # If May 31st is a Sunday (7), subtract 6 days (7 - 1 = 6) to get Monday.
    days_to_subtract = day_of_week_31st - pendulum.MONDAY

    # Step 4: Subtract these days from May 31st to find Memorial Day.
    memorial_day = may_31st.subtract(days=days_to_subtract)

    # Step 5: Return the resulting pendulum.Date object.
    return memorial_day

# Entry point: find_memorial_day(year: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_47_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_memorial_day(year):
    result = find_memorial_day(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
