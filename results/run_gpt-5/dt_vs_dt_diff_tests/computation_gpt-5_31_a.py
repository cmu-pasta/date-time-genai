
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def determine_fiscal_year(given_date: date) -> int:
    """
    Determine the fiscal year for a given date, assuming the fiscal year starts on April 1.
    Fiscal year is labeled by its ending calendar year.
    Example: Dates from 2023-04-01 to 2024-03-31 return 2024.
    """
    # If month is April (4) or later, fiscal year ends next calendar year
    if given_date.month >= 4:
        return given_date.year + 1
    # Otherwise (Jan–Mar), fiscal year ends in the current calendar year
    return given_date.year

# Entry point: determine_fiscal_year(given_date: date) -> int

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_31_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_determine_fiscal_year(given_date):
    result = determine_fiscal_year(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")
