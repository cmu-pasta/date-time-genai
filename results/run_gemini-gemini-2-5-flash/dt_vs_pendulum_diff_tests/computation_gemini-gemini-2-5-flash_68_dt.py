
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_labor_day(year: int) -> date:
    # Step 3: Establish the starting point as September 1st of the given year
    september_first = date(year, 9, 1)
    
    # Step 4: Determine the day of the week for September 1st
    # isoweekday() returns 1 for Monday, 2 for Tuesday, ..., 7 for Sunday
    day_of_week_sept_1st = september_first.isoweekday()
    
    # Step 5: Calculate days to add to reach the first Monday
    # If September 1st is Monday (1), days_to_add = 0
    # If September 1st is Tuesday (2), (7 - 2 + 1) % 7 = 6 % 7 = 6 days
    # If September 1st is Sunday (7), (7 - 7 + 1) % 7 = 1 % 7 = 1 day
    days_to_add = (7 - day_of_week_sept_1st + 1) % 7
    
    # Step 6: Compute Labor Day date by adding the calculated days
    labor_day = september_first + timedelta(days=days_to_add)
    
    # Step 7: Return the result
    return labor_day

# Entry point: find_labor_day(year: int) -> date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_68_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_labor_day(year):
    result = find_labor_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
