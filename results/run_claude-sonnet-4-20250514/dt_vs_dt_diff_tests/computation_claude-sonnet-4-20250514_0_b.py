
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_business_days(dt1: datetime, dt2: datetime) -> int:
    # Get the earlier and later dates
    start_date = min(dt1, dt2).date()
    end_date = max(dt1, dt2).date()
    
    # Initialize counter for business days
    business_days = 0
    current_date = start_date
    
    # Iterate through each day (exclusive of end date)
    while current_date < end_date:
        # Check if it's a weekday (Monday=0 to Friday=4, Saturday=5, Sunday=6)
        if current_date.weekday() < 5:  # 0-4 are business days
            business_days += 1
        current_date += timedelta(days=1)
    
    return business_days

# Entry point: calculate_business_days(dt1: datetime, dt2: datetime) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_0_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_business_days(dt1, dt2):
    result = calculate_business_days(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
