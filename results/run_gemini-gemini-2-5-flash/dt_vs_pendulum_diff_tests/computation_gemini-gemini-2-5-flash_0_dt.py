
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_business_days(date1: datetime, date2: datetime) -> int:
    # Step 1: Determine the start and end dates to ensure chronological order
    start_date = min(date1, date2)
    end_date = max(date1, date2)

    business_days_count = 0
    current_date = start_date

    # Step 2: Iterate through each day from start_date to end_date (inclusive)
    # The loop continues as long as current_date is less than or equal to end_date
    while current_date <= end_date:
        # Step 3: Check if the current_date is a business day
        # datetime.weekday() returns 0 for Monday, 1 for Tuesday, ..., 6 for Sunday.
        # Business days are Monday (0) through Friday (4).
        if 0 <= current_date.weekday() <= 4:
            business_days_count += 1
        
        # Step 4: Move to the next day
        current_date += timedelta(days=1)
    
    # Step 5: Return the total count of business days
    return business_days_count

# Entry point: calculate_business_days(date1: datetime, date2: datetime) -> int

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_0_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_business_days(date1, date2):
    result = calculate_business_days(date1, date2)
    formatted_result = format_value_dt(result, date1, date2)
    log_file.write(formatted_result + "\n")
