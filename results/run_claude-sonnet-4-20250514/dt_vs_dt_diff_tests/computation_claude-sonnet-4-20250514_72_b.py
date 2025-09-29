
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_biweekly_payroll_periods(year: int) -> int:
    # Step 1: Create datetime objects for the start and end of the year
    year_start = datetime(year, 1, 1)
    year_end = datetime(year, 12, 31)
    
    # Step 2: Calculate the total number of days in the year
    total_days = (year_end - year_start).days + 1  # +1 to include both start and end dates
    
    # Step 3: Calculate the number of complete bi-weekly periods (14 days each)
    biweekly_periods = total_days // 14
    
    # Step 4: Return the result
    return biweekly_periods

# Entry point: calculate_biweekly_payroll_periods(year: int) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_72_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_calculate_biweekly_payroll_periods(year):
    result = calculate_biweekly_payroll_periods(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
