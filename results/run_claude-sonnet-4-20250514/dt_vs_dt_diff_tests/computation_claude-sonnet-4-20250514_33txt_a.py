
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, time, date
def calculate_minutes_difference(time1: time, time2: time) -> int:
    # Step 1: Use a reference date (any date works since we're on the same day)
    reference_date = date.today()
    
    # Step 2: Convert time objects to datetime objects using the reference date
    dt1 = datetime.combine(reference_date, time1)
    dt2 = datetime.combine(reference_date, time2)
    
    # Step 3: Calculate the difference in minutes
    difference = abs((dt2 - dt1).total_seconds() / 60)
    
    # Step 4: Return the result as an integer
    return int(difference)

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_33txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_calculate_minutes_difference(time1, time2):
    result = calculate_minutes_difference(time1, time2)
    formatted_result = format_value_dt(result, time1, time2)
    log_file.write(formatted_result + "\n")
