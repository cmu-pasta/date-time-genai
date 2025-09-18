
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta, date
def find_first_monday(year: int, month: int) -> date:
    # Step 1: Create the first day of the given month and year
    first_day = date(year, month, 1)
    
    # Step 2: Find what day of the week the first day is (Monday = 0, Sunday = 6)
    first_day_weekday = first_day.weekday()
    
    # Step 3: Calculate how many days to add to get to the first Monday
    days_to_add = (7 - first_day_weekday) % 7
    
    # Step 4: Add the calculated days to get the first Monday
    first_monday = first_day + timedelta(days=days_to_add)
    
    # Step 5: Return the date of the first Monday
    return first_monday

# Entry point: find_first_monday(year: int, month: int) -> date

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_5txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_find_first_monday(year, month):
    result = find_first_monday(year, month)
    formatted_result = format_value_dt(result, year, month)
    log_file.write(formatted_result + "\n")
