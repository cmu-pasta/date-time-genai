
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_working_hours(start_dt: datetime, end_dt: datetime) -> float:
    # Ensure start is before end
    if start_dt > end_dt:
        start_dt, end_dt = end_dt, start_dt
    
    total_hours = 0.0
    current_dt = start_dt
    
    while current_dt < end_dt:
        # Check if current day is a weekday (Monday=0 to Friday=4)
        if current_dt.weekday() < 5:  # 0-4 are weekdays, 5-6 are weekend
            # Calculate end of current day
            end_of_day = current_dt.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            # Determine the end time for this day (either end of day or end_dt)
            day_end = min(end_of_day, end_dt)
            
            # Calculate hours for this day
            if current_dt < day_end:
                day_hours = (day_end - current_dt).total_seconds() / 3600
                total_hours += day_hours
        
        # Move to the start of next day
        next_day = (current_dt + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        current_dt = next_day
    
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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_24txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_working_hours(start_dt, end_dt):
    result = calculate_working_hours(start_dt, end_dt)
    formatted_result = format_value_dt(result, start_dt, end_dt)
    log_file.write(formatted_result + "\n")
