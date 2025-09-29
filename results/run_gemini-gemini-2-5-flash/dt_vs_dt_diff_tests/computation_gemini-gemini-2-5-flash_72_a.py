
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
from datetime import timedelta # Although not strictly necessary if using date(year+1,1,1) - date(year,1,1)
def calculate_biweekly_payroll_periods(year: int) -> int:
    # Step 1: Determine the start and end points to calculate the total days in the year.
    # We use January 1st of the given year and January 1st of the next year.
    start_of_year = date(year, 1, 1)
    start_of_next_year = date(year + 1, 1, 1)
    
    # Step 2: Calculate the total number of days in the given year.
    # Subtracting two date objects results in a timedelta object.
    days_in_year_timedelta = start_of_next_year - start_of_year
    days_in_year = days_in_year_timedelta.days
    
    # Step 3: Define the length of a bi-weekly period.
    bi_weekly_period_days = 14
    
    # Step 4: Calculate the number of full bi-weekly payroll periods.
    # We use integer division to get the count of full periods.
    number_of_periods = days_in_year // bi_weekly_period_days
    
    # Step 5: Return the result as an integer.
    return number_of_periods

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_72_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_calculate_biweekly_payroll_periods(year):
    result = calculate_biweekly_payroll_periods(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
