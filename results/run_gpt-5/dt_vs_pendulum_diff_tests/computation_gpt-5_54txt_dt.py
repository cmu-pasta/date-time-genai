
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_year_progress(dt: datetime) -> float:
    """
    Calculate the percentage of the year that has passed for a given datetime.

    Args:
        dt (datetime): The datetime for which to calculate the year's progress.

    Returns:
        float: The percentage (0.0 to 100.0) of the year that has passed.
    """
    # Start of the current year (preserve timezone awareness)
    start_of_year = datetime(dt.year, 1, 1, tzinfo=dt.tzinfo)
    # Start of the next year
    start_of_next_year = datetime(dt.year + 1, 1, 1, tzinfo=dt.tzinfo)

    # Total seconds in the year (handles leap years and timezone offsets)
    total_seconds = (start_of_next_year - start_of_year).total_seconds()
    # Seconds elapsed since the start of the year
    elapsed_seconds = (dt - start_of_year).total_seconds()

    # Calculate percentage and clamp to [0.0, 100.0]
    percentage = (elapsed_seconds / total_seconds) * 100.0 if total_seconds > 0 else 0.0
    if percentage < 0.0:
        percentage = 0.0
    elif percentage > 100.0:
        percentage = 100.0

    return percentage

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_54txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_year_progress(dt):
    result = calculate_year_progress(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
