
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_business_days(dt1: datetime, dt2: datetime) -> int:
    # Step 1: Determine the start and end dates (ensure proper ordering)
    start_date = min(dt1, dt2).date()
    end_date = max(dt1, dt2).date()
    
    # Step 2: Initialize counter for business days
    business_days = 0
    
    # Step 3: Iterate through each day in the range
    current_date = start_date
    while current_date < end_date:
        # Step 4: Check if current day is a weekday (Monday=0 to Friday=4)
        if current_date.weekday() < 5:  # 0-4 are weekdays, 5-6 are weekends
            business_days += 1
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    # Step 5: Return the count of business days
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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_0txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_business_days(dt1, dt2):
    result = calculate_business_days(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
