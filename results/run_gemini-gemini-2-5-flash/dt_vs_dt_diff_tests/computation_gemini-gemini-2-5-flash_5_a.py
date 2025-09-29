
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_first_monday(year: int, month: int) -> datetime:
    # Step 3: Construct the first day of the given month and year
    first_day_of_month = datetime(year, month, 1)
    
    # Step 4: Calculate days to add to reach the first Monday
    # Monday is 0, Tuesday is 1, ..., Sunday is 6
    # We want to find the difference to the target weekday (Monday = 0)
    # The formula (target_weekday - current_weekday + 7) % 7 gives days to add
    days_to_add = (0 - first_day_of_month.weekday() + 7) % 7
    
    # Step 5: Add the calculated days to find the first Monday
    first_monday = first_day_of_month + timedelta(days=days_to_add)
    
    # Step 6: Return the resulting datetime object
    return first_monday

# Entry point: find_first_monday(year: int, month: int) -> datetime

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_5_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_find_first_monday(year, month):
    result = find_first_monday(year, month)
    formatted_result = format_value_dt(result, year, month)
    log_file.write(formatted_result + "\n")
