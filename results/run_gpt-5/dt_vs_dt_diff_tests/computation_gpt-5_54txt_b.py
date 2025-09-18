
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date
def calculate_year_percentage(dt: datetime) -> float:
    """
    Calculate the percentage of the year that has passed for the given datetime.
    
    - The calculation preserves tzinfo if present on the input.
    - The result is a float percentage in the range [0.0, 100.0].
    """
    # Start and end of the year in the same timezone context as dt
    start_of_year = datetime(dt.year, 1, 1, tzinfo=dt.tzinfo)
    start_of_next_year = datetime(dt.year + 1, 1, 1, tzinfo=dt.tzinfo)

    total_seconds_in_year = (start_of_next_year - start_of_year).total_seconds()
    elapsed_seconds = (dt - start_of_year).total_seconds()

    # Compute percentage and clamp to [0, 100] to be robust
    percentage = (elapsed_seconds / total_seconds_in_year) * 100.0
    if percentage < 0.0:
        return 0.0
    if percentage > 100.0:
        return 100.0
    return percentage

def calculate_year_percentage_for_date(d: date) -> float:
    """
    Convenience function to accept a date input (assumes midnight at the start of the day).
    """
    dt = datetime(d.year, d.month, d.day)  # naive midnight
    return calculate_year_percentage(dt)

# Entry point: calculate_year_percentage(dt: datetime) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_54txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_year_percentage(dt):
    result = calculate_year_percentage(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
