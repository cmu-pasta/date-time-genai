
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def get_first_day_of_fiscal_year(reference_date: date, fiscal_start_month: int, fiscal_start_day: int) -> date:
    """
    Returns the first day of the fiscal year for a specified reference date and fiscal year start.
    """
    # Step 1: Create a date object for the fiscal year start in the reference year
    try:
        fiscal_year_start = date(reference_date.year, fiscal_start_month, fiscal_start_day)
    except ValueError:
        # Invalid month/day (e.g., February 30), raise an error
        raise ValueError("Invalid fiscal start month and day combination.")
    
    # Step 2: Determine if the reference_date falls before the fiscal year start in that year
    if reference_date < fiscal_year_start:
        # Fiscal year started in the previous year
        fiscal_year_start = date(reference_date.year - 1, fiscal_start_month, fiscal_start_day)
    
    # Step 3: Return the fiscal year start date
    return fiscal_year_start

# Entry point: get_first_day_of_fiscal_year(reference_date: date, fiscal_start_month: int, fiscal_start_day: int) -> date

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_30txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy(), timestamp_strategy())
def test_get_first_day_of_fiscal_year(reference_date, fiscal_start_month, fiscal_start_day):
    result = get_first_day_of_fiscal_year(reference_date, fiscal_start_month, fiscal_start_day)
    formatted_result = format_value_dt(result, reference_date, fiscal_start_month, fiscal_start_day)
    log_file.write(formatted_result + "\n")
