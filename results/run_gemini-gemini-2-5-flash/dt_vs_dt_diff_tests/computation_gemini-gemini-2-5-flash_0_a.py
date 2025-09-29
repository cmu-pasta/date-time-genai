
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_business_days_difference(dt1: datetime, dt2: datetime) -> int:
    # Step 1: Ensure dt_start is earlier than or equal to dt_end.
    # We only care about the date part for counting days.
    date_start = dt1.date()
    date_end = dt2.date()

    if date_start > date_end:
        date_start, date_end = date_end, date_start

    # Step 2: Initialize a counter for business days.
    business_days_count = 0
    current_date = date_start

    # Step 3: Iterate from the start date up to and including the end date.
    while current_date <= date_end:
        # Step 4: Check if the current day is a weekday (Monday to Friday).
        # weekday() returns 0 for Monday, 1 for Tuesday, ..., 6 for Sunday.
        # Business days are 0, 1, 2, 3, 4.
        if current_date.weekday() < 5:
            business_days_count += 1
        
        # Step 5: Move to the next day.
        current_date += timedelta(days=1)
    
    # Step 6: Return the total number of business days.
    return business_days_count

# Entry point: calculate_business_days_difference(dt1: datetime, dt2: datetime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_0_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_business_days_difference(dt1, dt2):
    result = calculate_business_days_difference(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
