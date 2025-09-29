
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_february_sundays(year: int) -> int:
    sunday_count = 0
    
    # Step 1: Set the starting date to February 1st of the given year
    current_date = date(year, 2, 1)
    
    # Step 2: Iterate through each day of February
    # The loop continues as long as the current_date is still in February
    while current_date.month == 2:
        # Step 3: Check if the current day is a Sunday (weekday() returns 6 for Sunday)
        if current_date.weekday() == 6:
            sunday_count += 1
        
        # Step 4: Move to the next day
        current_date += timedelta(days=1)
        
    # Step 5: Return the total count of Sundays
    return sunday_count

# Entry point: count_february_sundays(year: int) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_49_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_count_february_sundays(year):
    result = count_february_sundays(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
