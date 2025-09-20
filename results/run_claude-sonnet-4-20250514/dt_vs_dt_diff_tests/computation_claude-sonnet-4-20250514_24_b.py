
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_working_hours(start_dt: datetime, end_dt: datetime) -> float:
    # Define standard working hours (9 AM to 5 PM)
    work_start_hour = 9
    work_end_hour = 17
    
    # Ensure start_dt is before end_dt
    if start_dt > end_dt:
        start_dt, end_dt = end_dt, start_dt
    
    total_working_hours = 0.0
    current_date = start_dt.date()
    end_date = end_dt.date()
    
    # Iterate through each day in the date range
    while current_date <= end_date:
        # Check if it's a weekday (Monday=0 to Friday=4)
        if current_date.weekday() < 5:
            # Create datetime objects for work start and end on this day
            work_start = datetime.combine(current_date, datetime.min.time().replace(hour=work_start_hour))
            work_end = datetime.combine(current_date, datetime.min.time().replace(hour=work_end_hour))
            
            # Find the overlap between the given datetime range and working hours
            overlap_start = max(start_dt, work_start)
            overlap_end = min(end_dt, work_end)
            
            # If there's an overlap, calculate the hours
            if overlap_start < overlap_end:
                overlap_duration = overlap_end - overlap_start
                total_working_hours += overlap_duration.total_seconds() / 3600
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    return total_working_hours

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_24_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_working_hours(start_dt, end_dt):
    result = calculate_working_hours(start_dt, end_dt)
    formatted_result = format_value_dt(result, start_dt, end_dt)
    log_file.write(formatted_result + "\n")
