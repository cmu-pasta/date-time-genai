
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_labor_day(year: int) -> pendulum.Date:
    # Step 1: Create a pendulum.Date object for September 1st of the given year.
    first_september = pendulum.date(year, 9, 1)

    # Step 2: Determine the day of the week for September 1st.
    # pendulum.MONDAY is 1, Tuesday is 2, ..., Sunday is 7.
    current_day_of_week = first_september.day_of_week

    # Step 3: Calculate how many days to add to reach the first Monday.
    # If September 1st is already a Monday, days_to_add will be 0.
    # Otherwise, it calculates the difference to the next Monday.
    # The '+ 7) % 7' ensures the result is always positive and correct for week wrapping.
    days_to_add = (pendulum.MONDAY - current_day_of_week + 7) % 7

    # Step 4: Add the calculated days to September 1st to find Labor Day.
    labor_day_date = first_september.add(days=days_to_add)

    # Step 5: Return the resulting pendulum.Date object.
    return labor_day_date

# Entry point: find_labor_day(year: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_68_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_labor_day(year):
    result = find_labor_day(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
