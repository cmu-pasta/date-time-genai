
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def age_in_total_days(birth_date: date, reference_date: date) -> int:
    """
    Calculate the total number of days between a birth date and a reference date.

    Args:
        birth_date (date): The birth date.
        reference_date (date): The date to measure the age against.

    Returns:
        int: The total number of days of age (non-negative).
    """
    # Compute the difference as a timedelta
    delta = reference_date - birth_date
    # Return absolute number of days to ensure non-negative age
    return abs(delta.days)

# Entry point: age_in_total_days(birth_date: date, reference_date: date) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_39_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_age_in_total_days(birth_date, reference_date):
    result = age_in_total_days(birth_date, reference_date)
    formatted_result = format_value_dt(result, birth_date, reference_date)
    log_file.write(formatted_result + "\n")
