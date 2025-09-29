
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_labor_day(year: int) -> datetime:
    # Step 1: Create a datetime object for September 1st of the given year.
    september_first = datetime(year, 9, 1)
    
    # Step 2: Determine the day of the week for September 1st.
    # Monday is 0, Sunday is 6.
    day_of_week = september_first.weekday()
    
    # Step 3: Calculate the number of days to add to reach the first Monday.
    # If September 1st is Monday (0), add 0 days: (7 - 0) % 7 = 0
    # If September 1st is Tuesday (1), add 6 days: (7 - 1) % 7 = 6
    # If September 1st is Sunday (6), add 1 day: (7 - 6) % 7 = 1
    days_to_add = (7 - day_of_week) % 7
    
    # Step 4: Add the calculated days to September 1st to get Labor Day.
    labor_day = september_first + timedelta(days=days_to_add)
    
    # Step 5: Return the resulting datetime object.
    return labor_day

# Entry point: find_labor_day(year: int) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_68_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_labor_day(year):
    result = find_labor_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
