
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def count_sundays_in_february(year: int) -> int:
    # Step 1: Create a date for February 1st of the given year
    feb_first = pendulum.date(year, 2, 1)
    
    # Step 2: Determine the number of days in February for this year
    days_in_february = feb_first.days_in_month
    
    # Step 3: Initialize counter for Sundays
    sunday_count = 0
    
    # Step 4: Iterate through each day in February
    for day in range(1, days_in_february + 1):
        current_date = pendulum.date(year, 2, day)
        
        # Step 5: Check if the current day is Sunday (day_of_week == 0)
        if current_date.day_of_week == 0:
            sunday_count += 1
    
    # Step 6: Return the count of Sundays
    return sunday_count

# Entry point: count_sundays_in_february(year: int) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_49_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_count_sundays_in_february(year):
    result = count_sundays_in_february(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
