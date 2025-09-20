
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def determine_fiscal_year(date_obj: datetime) -> int:
    """
    Determines the fiscal year for a given date, assuming an April start.

    Args:
        date_obj: The input date as a datetime object.

    Returns:
        The fiscal year as an integer.
    """
    # Fiscal year starts in April (month 4)
    fiscal_start_month = 4

    # If the month is before April, the fiscal year is the previous calendar year
    if date_obj.month < fiscal_start_month:
        fiscal_year = date_obj.year - 1
    # Otherwise (month is April or later), the fiscal year is the current calendar year
    else:
        fiscal_year = date_obj.year
        
    return fiscal_year

# Entry point: determine_fiscal_year(date_obj: datetime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_31_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_determine_fiscal_year(date_obj):
    result = determine_fiscal_year(date_obj)
    formatted_result = format_value_dt(result, date_obj)
    log_file.write(formatted_result + "\n")
