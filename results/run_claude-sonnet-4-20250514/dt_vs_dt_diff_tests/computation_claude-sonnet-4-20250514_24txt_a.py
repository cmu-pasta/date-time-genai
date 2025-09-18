
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_working_hours(start_dt: datetime, end_dt: datetime) -> float:
    # Ensure start_dt is before end_dt
    if start_dt > end_dt:
        start_dt, end_dt = end_dt, start_dt
    
    total_hours = 0.0
    current_dt = start_dt
    
    # Iterate through each day between start and end
    while current_dt.date() <= end_dt.date():
        # Check if current day is a weekday (0=Monday, 6=Sunday)
        if current_dt.weekday() < 5:  # Monday to Friday are working days
            # Calculate the start and end times for this specific day
            day_start = max(current_dt, current_dt.replace(hour=0, minute=0, second=0, microsecond=0))
            day_end = min(end_dt, current_dt.replace(hour=23, minute=59, second=59, microsecond=999999))
            
            # If this is the first day, use the actual start time
            if current_dt.date() == start_dt.date():
                day_start = start_dt
            
            # If this is the last day, use the actual end time
            if current_dt.date() == end_dt.date():
                day_end = end_dt
            
            # Calculate hours for this working day
            if day_end > day_start:
                day_hours = (day_end - day_start).total_seconds() / 3600
                total_hours += day_hours
        
        # Move to the next day
        current_dt = (current_dt + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    
    return total_hours

# Entry point: calculate_working_hours(start_dt: datetime, end_dt: datetime) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_24txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_working_hours(start_dt, end_dt):
    result = calculate_working_hours(start_dt, end_dt)
    formatted_result = format_value_dt(result, start_dt, end_dt)
    log_file.write(formatted_result + "\n")
