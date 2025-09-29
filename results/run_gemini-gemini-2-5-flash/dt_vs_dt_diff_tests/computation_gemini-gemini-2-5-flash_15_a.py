
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_weekends_between_dates(dt1: datetime, dt2: datetime) -> int:
    # Step 1: Ensure dt1 is the earlier date to simplify iteration
    if dt1 > dt2:
        dt1, dt2 = dt2, dt1

    weekend_count = 0
    
    # Step 2: Extract the date part and initialize current_date for iteration
    current_date = dt1.date()
    end_date_limit = dt2.date()

    # Step 3: Iterate through each day from the start_date to the end_date (inclusive)
    while current_date <= end_date_limit:
        # Step 4: Check if the current day is a Saturday (weekday 5) or a Sunday (weekday 6)
        if current_date.weekday() == 5 or current_date.weekday() == 6:
            weekend_count += 1
        
        # Step 5: Move to the next day
        current_date += timedelta(days=1)
            
    # Step 6: Return the total count of weekend days
    return weekend_count

# Entry point: calculate_weekends_between_dates(dt1: datetime, dt2: datetime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_15_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_weekends_between_dates(dt1, dt2):
    result = calculate_weekends_between_dates(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
