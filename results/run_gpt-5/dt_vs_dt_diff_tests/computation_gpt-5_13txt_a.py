
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def determine_quarter(d: date) -> int:
    """
    Determine the quarter of the year for a given date.
    
    Parameters:
        d (date): The date for which to determine the quarter.
    
    Returns:
        int: The quarter number (1 to 4).
    """
    # Step 1: Extract the month from the given date.
    month = d.month
    
    # Step 2: Compute the quarter using integer arithmetic.
    quarter = ((month - 1) // 3) + 1
    
    # Step 3: Return the quarter as an integer.
    return quarter

# Entry point: determine_quarter(d: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_13txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_determine_quarter(d):
    result = determine_quarter(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")
