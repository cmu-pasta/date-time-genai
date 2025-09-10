
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def get_fiscal_year_start(
    current_date: date, 
    fiscal_year_start_month: int, 
    fiscal_year_start_day: int
) -> date:
    """
    Returns the first day of the fiscal year for a given organization.
    
    Args:
        current_date (date): The date for which to find the fiscal year start.
        fiscal_year_start_month (int): The starting month of the fiscal year (1-12).
        fiscal_year_start_day (int): The starting day of the fiscal year (1-31).
        
    Returns:
        date: The first day of the corresponding fiscal year.
    """
    # Step 1: Construct this year's fiscal year start date
    fy_start_this_year = date(
        year=current_date.year,
        month=fiscal_year_start_month,
        day=fiscal_year_start_day
    )
    
    # Step 2: Determine if the fiscal year starts this year or last year
    if current_date >= fy_start_this_year:
        return fy_start_this_year
    else:
        # Fiscal year started last year
        return date(
            year=current_date.year - 1,
            month=fiscal_year_start_month,
            day=fiscal_year_start_day
        )

# Entry point: get_fiscal_year_start(current_date: date, fiscal_year_start_month: int, fiscal_year_start_day: int) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_30txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy(), timestamp_strategy())
def test_get_fiscal_year_start(current_date, fiscal_year_start_month, fiscal_year_start_day):
    result = get_fiscal_year_start(current_date, fiscal_year_start_month, fiscal_year_start_day)
    formatted_result = format_value_dt(result, current_date, fiscal_year_start_month, fiscal_year_start_day)
    log_file.write(formatted_result + "\n")
