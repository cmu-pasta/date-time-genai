
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_age_in_seconds(birth_dt: datetime) -> int:
    """
    Calculate the chronological age in seconds for a given birth datetime.
    
    Args:
        birth_dt (datetime): The birth datetime.
        
    Returns:
        int: The age in seconds. Negative if birth_dt is in the future.
    """
    # Use timezone-aware 'now' if birth_dt has tzinfo; else use naive 'now'
    now = datetime.now(tz=birth_dt.tzinfo)
    delta = now - birth_dt
    return int(delta.total_seconds())

# Entry point: calculate_age_in_seconds(birth_dt: datetime) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_75_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_age_in_seconds(birth_dt):
    result = calculate_age_in_seconds(birth_dt)
    formatted_result = format_value_dt(result, birth_dt)
    log_file.write(formatted_result + "\n")
