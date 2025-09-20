
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def find_middle_date(dt1: datetime, dt2: datetime) -> datetime:
    # Step 1: Determine which date is earlier and which is later
    if dt1 < dt2:
        earlier = dt1
        later = dt2
    else:
        earlier = dt2
        later = dt1
    
    # Step 2: Calculate the difference between the two dates
    difference = later - earlier
    
    # Step 3: Find the middle point by dividing the difference by 2
    middle_difference = difference / 2
    
    # Step 4: Add the middle difference to the earlier date
    middle_date = earlier + middle_difference
    
    return middle_date

# Entry point: find_middle_date(dt1: datetime, dt2: datetime) -> datetime

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_32_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_find_middle_date(dt1, dt2):
    result = find_middle_date(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
