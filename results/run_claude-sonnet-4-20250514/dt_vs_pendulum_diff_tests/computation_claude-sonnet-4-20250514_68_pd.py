
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_labor_day(year: int) -> pendulum.Date:
    # Step 1: Create September 1st of the given year
    sept_first = pendulum.date(year, 9, 1)
    
    # Step 2: Get the day of the week (1=Monday, 2=Tuesday, ..., 7=Sunday)
    day_of_week = sept_first.day_of_week
    
    # Step 3: Calculate days to add to get to the first Monday
    # If September 1st is Monday (1), add 0 days
    # If it's Tuesday (2), add 6 days, etc.
    days_to_add = (8 - day_of_week) % 7
    
    # Step 4: Add the calculated days to get Labor Day
    labor_day = sept_first.add(days=days_to_add)
    
    # Step 5: Return the result as pendulum.Date
    return labor_day

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_68_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_labor_day(year):
    result = find_labor_day(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
