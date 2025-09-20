
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_nth_weekday_in_month(year: int, month: int, weekday: int, n: int) -> date:
    # Step 1: Create the first day of the given month and year
    first_day = date(year, month, 1)
    
    # Step 2: Find what weekday the first day is (0=Monday, 1=Tuesday, etc.)
    first_weekday = first_day.weekday()
    
    # Step 3: Calculate days to add to get to the first occurrence of target weekday
    days_to_first_occurrence = (weekday - first_weekday) % 7
    
    # Step 4: Calculate the date of the first occurrence of the target weekday
    first_occurrence = first_day + timedelta(days=days_to_first_occurrence)
    
    # Step 5: Calculate the nth occurrence by adding (n-1) weeks
    nth_occurrence = first_occurrence + timedelta(days=(n-1) * 7)
    
    # Step 6: Return the result as a date object
    return nth_occurrence

# Entry point: find_nth_weekday_in_month(year: int, month: int, weekday: int, n: int) -> date

def format_value_dt(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, datetime):
            formatted_values.append(value.isoformat())
        elif isinstance(value, date):
            # Use strftime to format the date similar to to_date_string()
            formatted_values.append(value.strftime("%Y-%m-%d"))
        elif isinstance(value, time):
            formatted_values.append(value.isoformat())
        elif isinstance(value, timedelta):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_17_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_nth_weekday_in_month(year, month, weekday, n):
    result = find_nth_weekday_in_month(year, month, weekday, n)
    formatted_result = format_value_dt(result, year, month, weekday, n)
    log_file.write(formatted_result + "\n")
