
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta, time
def calculate_working_hours_between_datetimes(start_dt: datetime, end_dt: datetime) -> float:
    # Handle cases where start_dt is after end_dt
    if start_dt > end_dt:
        return 0.0

    # Define working hours (9 AM to 5 PM, inclusive, so 8 hours total)
    working_start_time = time(9, 0, 0)
    working_end_time = time(17, 0, 0) # 5 PM
    
    # Calculate daily working hours (e.g., 17 - 9 = 8 hours)
    daily_working_hours = (working_end_time.hour - working_start_time.hour)

    total_working_hours = 0.0

    current_dt = start_dt

    # Loop day by day
    while current_dt.date() <= end_dt.date():
        # Check if the current day is a weekday (Monday=0, Sunday=6)
        if 0 <= current_dt.weekday() <= 4: # Monday to Friday
            
            # Create datetime objects for the start and end of working hours for the current day
            day_working_start_dt = datetime(current_dt.year, current_dt.month, current_dt.day,
                                            working_start_time.hour, working_start_time.minute, working_start_time.second)
            day_working_end_dt = datetime(current_dt.year, current_dt.month, current_dt.day,
                                          working_end_time.hour, working_end_time.minute, working_end_time.second)

            # Determine the effective start and end for calculating hours on this specific day
            effective_day_start = max(start_dt, day_working_start_dt)
            effective_day_end = min(end_dt, day_working_end_dt)

            # Only add hours if the effective period has a positive duration
            if effective_day_end > effective_day_start:
                duration_on_day = effective_day_end - effective_day_start
                total_working_hours += duration_on_day.total_seconds() / 3600.0 # Convert timedelta to hours

        # Move to the next day
        current_dt += timedelta(days=1)
        # Reset time to start of day to avoid issues with time skipping, especially if we iterate `current_dt`
        # However, the `current_dt` in the loop needs to preserve its time component if it's the `start_dt`
        # For subsequent days, we effectively process full days or the `end_dt` part.
        # A safer iteration method is to iterate dates and construct datetime for calculations.

    # Corrected iteration: iterate through dates, construct datetimes for calculations
    current_date = start_dt.date()
    while current_date <= end_dt.date():
        if 0 <= current_date.weekday() <= 4: # Monday to Friday
            # Define the working window for the current_date
            day_working_start_dt_calc = datetime(current_date.year, current_date.month, current_date.day,
                                                 working_start_time.hour, working_start_time.minute, working_start_time.second)
            day_working_end_dt_calc = datetime(current_date.year, current_date.month, current_date.day,
                                               working_end_time.hour, working_end_time.minute, working_end_time.second)

            # Calculate the intersection of the given time range with the working hours window for this day
            segment_start = max(start_dt, day_working_start_dt_calc)
            segment_end = min(end_dt, day_working_end_dt_calc)

            if segment_end > segment_start:
                total_working_hours += (segment_end - segment_start).total_seconds() / 3600.0

        current_date += timedelta(days=1)

    return total_working_hours

# Entry point: calculate_working_hours_between_datetimes(start_dt: datetime, end_dt: datetime) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_24_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_working_hours_between_datetimes(start_dt, end_dt):
    result = calculate_working_hours_between_datetimes(start_dt, end_dt)
    formatted_result = format_value_dt(result, start_dt, end_dt)
    log_file.write(formatted_result + "\n")
