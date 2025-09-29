
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_working_hours(dt1: datetime, dt2: datetime) -> float:
    # Step 1: Ensure dt1 is always the earlier datetime for consistent calculation
    if dt1 > dt2:
        dt1, dt2 = dt2, dt1

    total_working_hours = 0.0
    current_dt = dt1

    # Loop through each day from dt1's date up to dt2's date
    while current_dt < dt2:
        # Check if the current day is a weekday (Monday=0 to Friday=4)
        if current_dt.weekday() < 5:  # 0-4 are weekdays
            # Determine the start and end of the relevant time window for the current day
            
            # This day's effective start time is the later of current_dt or the beginning of this calendar day
            day_start_time = max(current_dt, datetime(current_dt.year, current_dt.month, current_dt.day, 0, 0, 0))
            
            # This day's effective end time is the earlier of dt2 or the end of this calendar day
            day_end_time = min(dt2, datetime(current_dt.year, current_dt.month, current_dt.day, 23, 59, 59, 999999))
            
            # Only add hours if the start time is before the end time for this day
            if day_start_time < day_end_time:
                duration = day_end_time - day_start_time
                total_working_hours += duration.total_seconds() / 3600.0

        # Move to the next day, ensuring we don't skip over dt2
        # If current_dt has passed into the next day already due to day_end_time calculation,
        # we still need to make sure we advance correctly.
        # A simple way to advance day-by-day is to get to the start of the next day.
        next_day_start = datetime(current_dt.year, current_dt.month, current_dt.day) + timedelta(days=1)
        current_dt = next_day_start

    # The loop condition `current_dt < dt2` needs careful handling for the final segment.
    # The current approach iterates full days and handles partial start/end.
    # Let's refine the loop to ensure the span between dt1 and dt2 is fully covered.
    
    # Reset and use a simpler loop for day iteration
    total_working_hours = 0.0
    
    # Iterate day by day, starting from the date of dt1
    current_date = dt1.date()
    end_date = dt2.date()

    while current_date <= end_date:
        # If it's a weekday
        if current_date.weekday() < 5:
            # Determine the specific datetime range for this weekday
            day_start = datetime.combine(current_date, datetime.min.time())
            day_end = datetime.combine(current_date, datetime.max.time())

            # Clip the day's range by the overall dt1 and dt2
            segment_start = max(dt1, day_start)
            segment_end = min(dt2, day_end)
            
            # If there's an actual time segment on this day, add its duration
            if segment_start < segment_end:
                duration = segment_end - segment_start
                total_working_hours += duration.total_seconds() / 3600.0
        
        # Move to the next calendar day
        current_date += timedelta(days=1)
        
    return total_working_hours

# Entry point: calculate_working_hours(dt1: datetime, dt2: datetime) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_24_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_working_hours(dt1, dt2):
    result = calculate_working_hours(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
