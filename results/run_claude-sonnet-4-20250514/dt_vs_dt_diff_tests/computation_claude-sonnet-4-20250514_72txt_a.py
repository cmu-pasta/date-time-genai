
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_biweekly_payroll_periods(year: int) -> int:
    # Step 1: Define the start and end of the year
    year_start = datetime(year, 1, 1)
    year_end = datetime(year, 12, 31)
    
    # Step 2: Define bi-weekly period length (14 days)
    biweekly_period = timedelta(days=14)
    
    # Step 3: Count bi-weekly periods starting from January 1st
    current_date = year_start
    period_count = 0
    
    # Step 4: Count periods that start within the calendar year
    while current_date <= year_end:
        period_count += 1
        current_date += biweekly_period
    
    # Step 5: Return the total count
    return period_count

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_72txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_calculate_biweekly_payroll_periods(year):
    result = calculate_biweekly_payroll_periods(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
