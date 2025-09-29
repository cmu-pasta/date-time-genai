
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_last_weekday_in_month(year: int, month: int, weekday: int) -> pendulum.Date:
    # Step 1: Create the last day of the given month
    # We do this by going to the first day of next month and subtracting 1 day
    if month == 12:
        next_month = pendulum.date(year + 1, 1, 1)
    else:
        next_month = pendulum.date(year, month + 1, 1)
    
    last_day_of_month = next_month.subtract(days=1)
    
    # Step 2: Find the weekday of the last day (1=Monday, 7=Sunday)
    last_day_weekday = last_day_of_month.day_of_week
    
    # Step 3: Calculate how many days to go back to find the target weekday
    days_back = (last_day_weekday - weekday) % 7
    
    # Step 4: Find the target date by going back the calculated days
    target_date = last_day_of_month.subtract(days=days_back)
    
    return target_date

# Entry point: find_last_weekday_in_month(year: int, month: int, weekday: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_80_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_last_weekday_in_month(year, month, weekday):
    result = find_last_weekday_in_month(year, month, weekday)
    formatted_result = format_value_pd(result, year, month, weekday)
    log_file.write(formatted_result + "\n")
