
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def calculate_biweekly_payroll_periods(year: int) -> int:
    # Create date objects for the start of the given year and the start of the next year
    start_of_year = date(year, 1, 1)
    start_of_next_year = date(year + 1, 1, 1)
    
    # Calculate the total number of days in the given year
    days_in_year = (start_of_next_year - start_of_year).days
    
    # Calculate the number of bi-weekly periods (14 days each)
    # Using integer division to get complete periods only
    periods = days_in_year // 14
    
    return periods

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_72txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_calculate_biweekly_payroll_periods(year):
    result = calculate_biweekly_payroll_periods(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
