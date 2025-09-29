
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_age_in_seconds(birth: datetime) -> int:
    # Get current datetime aligned with the timezone awareness of the input
    now = datetime.now(tz=birth.tzinfo)
    # Compute the time difference
    delta = now - birth
    # Convert to total seconds and ensure non-negative age
    seconds = int(delta.total_seconds())
    return seconds if seconds >= 0 else 0

# Entry point: calculate_age_in_seconds(birth: datetime) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_75_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_age_in_seconds(birth):
    result = calculate_age_in_seconds(birth)
    formatted_result = format_value_dt(result, birth)
    log_file.write(formatted_result + "\n")
