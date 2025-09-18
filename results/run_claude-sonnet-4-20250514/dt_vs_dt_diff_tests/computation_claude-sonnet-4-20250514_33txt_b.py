
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, time
def calculate_minutes_difference(time1: time, time2: time) -> int:
    # Step 1: Convert times to datetime objects using a common date (today)
    today = datetime.today().date()
    dt1 = datetime.combine(today, time1)
    dt2 = datetime.combine(today, time2)
    
    # Step 2: Calculate the difference in seconds and convert to minutes
    difference_seconds = abs((dt2 - dt1).total_seconds())
    difference_minutes = difference_seconds / 60
    
    # Step 3: Return the result as an integer
    return int(difference_minutes)

# Entry point: calculate_minutes_difference(time1: time, time2: time) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_33txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_calculate_minutes_difference(time1, time2):
    result = calculate_minutes_difference(time1, time2)
    formatted_result = format_value_dt(result, time1, time2)
    log_file.write(formatted_result + "\n")
