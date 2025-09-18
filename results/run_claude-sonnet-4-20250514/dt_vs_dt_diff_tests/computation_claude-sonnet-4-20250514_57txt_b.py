
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_work_weeks(start_date: datetime, end_date: datetime) -> float:
    # Ensure start_date is before end_date
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    
    # Initialize working days counter
    working_days = 0
    current_date = start_date
    
    # Count working days (Monday=0 to Sunday=6, so weekdays are 0-4)
    while current_date < end_date:
        if current_date.weekday() < 5:  # Monday to Friday (0-4)
            working_days += 1
        current_date += timedelta(days=1)
    
    # Convert working days to work weeks (5 working days per work week)
    work_weeks = working_days / 5.0
    
    return work_weeks

# Entry point: calculate_work_weeks(start_date: datetime, end_date: datetime) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_57txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_work_weeks(start_date, end_date):
    result = calculate_work_weeks(start_date, end_date)
    formatted_result = format_value_dt(result, start_date, end_date)
    log_file.write(formatted_result + "\n")
