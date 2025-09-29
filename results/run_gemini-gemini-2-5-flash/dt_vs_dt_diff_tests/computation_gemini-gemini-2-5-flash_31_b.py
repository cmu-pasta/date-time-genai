
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def determine_fiscal_year(dt: datetime) -> int:
    # Step 1: Get the calendar year and month from the input datetime object
    calendar_year = dt.year
    month = dt.month
    
    # Step 2: Apply the fiscal year logic (April start)
    # If the month is April (4) or later, the fiscal year is the current calendar year.
    # Otherwise (Jan, Feb, Mar), it's the previous calendar year.
    if month >= 4:
        fiscal_year = calendar_year
    else:
        fiscal_year = calendar_year - 1
        
    # Step 3: Return the calculated fiscal year as an integer
    return fiscal_year

# Entry point: determine_fiscal_year(dt: datetime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_31_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_determine_fiscal_year(dt):
    result = determine_fiscal_year(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
