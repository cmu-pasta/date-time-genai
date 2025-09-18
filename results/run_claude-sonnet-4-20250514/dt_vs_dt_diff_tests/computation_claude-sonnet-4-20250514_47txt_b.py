
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_memorial_day(year: int) -> date:
    # Step 1: Find May 31st of the given year
    may_31 = date(year, 5, 31)
    
    # Step 2: Find what day of the week May 31st is (0=Monday, 6=Sunday)
    weekday = may_31.weekday()
    
    # Step 3: Calculate how many days to go back to get to the last Monday
    days_back = weekday
    
    # Step 4: Calculate Memorial Day by going back the required number of days
    memorial_day = may_31 - timedelta(days=days_back)
    
    return memorial_day

# Entry point: find_memorial_day(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_47txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_memorial_day(year):
    result = find_memorial_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
