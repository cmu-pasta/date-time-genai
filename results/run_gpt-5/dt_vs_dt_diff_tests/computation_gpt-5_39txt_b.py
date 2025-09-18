
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def calculate_age_in_days(birth_date: date, reference_date: date) -> int:
    """
    Calculate the age in total days between a birth date and a reference date.

    Parameters:
    - birth_date (date): The date of birth.
    - reference_date (date): The date on which to calculate the age.

    Returns:
    - int: Total number of days between the two dates. This value will be negative
           if the reference_date is before the birth_date.
    """
    # Compute the difference between the reference date and the birth date
    delta = reference_date - birth_date

    # Return the difference in days as an integer
    return delta.days

# Entry point: calculate_age_in_days(birth_date: date, reference_date: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_39txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_age_in_days(birth_date, reference_date):
    result = calculate_age_in_days(birth_date, reference_date)
    formatted_result = format_value_dt(result, birth_date, reference_date)
    log_file.write(formatted_result + "\n")
