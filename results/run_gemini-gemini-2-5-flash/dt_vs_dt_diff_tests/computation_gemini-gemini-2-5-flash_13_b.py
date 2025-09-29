
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def get_quarter_of_year(dt: datetime) -> int:
    # Step 1: Extract the month from the datetime object
    month = dt.month
    
    # Step 2: Calculate the quarter based on the month
    # Quarters are typically:
    # Q1: Jan-Mar (1-3)
    # Q2: Apr-Jun (4-6)
    # Q3: Jul-Sep (7-9)
    # Q4: Oct-Dec (10-12)
    # The formula (month - 1) // 3 + 1 correctly maps these ranges.
    quarter = (month - 1) // 3 + 1
    
    # Step 3: Return the quarter as an integer
    return quarter

# Entry point: get_quarter_of_year(dt: datetime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_13_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_quarter_of_year(dt):
    result = get_quarter_of_year(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
