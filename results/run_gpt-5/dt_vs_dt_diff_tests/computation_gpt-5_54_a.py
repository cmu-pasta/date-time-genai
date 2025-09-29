
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_year_progress(dt: datetime) -> float:
    """
    Calculate the percentage of the year that has passed for the given datetime.
    
    Args:
        dt (datetime): A datetime object representing the moment to evaluate.
        
    Returns:
        float: Percentage of the year that has passed (0.0 to 100.0).
    """
    # Start of the year in the same tzinfo as dt
    start_of_year = dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    # Start of the next year
    start_next_year = start_of_year.replace(year=start_of_year.year + 1)
    
    # Elapsed and total seconds
    elapsed_seconds = (dt - start_of_year).total_seconds()
    total_seconds = (start_next_year - start_of_year).total_seconds()
    
    # Percentage of the year elapsed
    return (elapsed_seconds / total_seconds) * 100.0

# Entry point: calculate_year_progress(dt: datetime) -> float

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_54_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_year_progress(dt):
    result = calculate_year_progress(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
