
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_weekends_between_dates(dt1: datetime, dt2: datetime) -> int:
    # Ensure dt1 is the earlier date
    if dt1 > dt2:
        dt1, dt2 = dt2, dt1
    
    # Find the first Saturday on or after dt1
    # weekday() returns 0=Monday, 1=Tuesday, ..., 5=Saturday, 6=Sunday
    days_to_first_saturday = (5 - dt1.weekday()) % 7
    first_saturday = dt1 + timedelta(days=days_to_first_saturday)
    
    # Find the last Saturday on or before dt2
    days_from_last_saturday = (dt2.weekday() - 5) % 7
    last_saturday = dt2 - timedelta(days=days_from_last_saturday)
    
    # If first Saturday is after last Saturday, no complete weekends exist
    if first_saturday > last_saturday:
        return 0
    
    # Calculate number of complete weekends
    # Each weekend is 7 days apart
    weekends = ((last_saturday - first_saturday).days // 7) + 1
    
    return weekends

# Entry point: calculate_weekends_between_dates(dt1: datetime, dt2: datetime) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_15_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_weekends_between_dates(dt1, dt2):
    result = calculate_weekends_between_dates(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
