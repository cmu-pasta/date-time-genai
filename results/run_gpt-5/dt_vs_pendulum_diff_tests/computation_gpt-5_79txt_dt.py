
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def buddhist_calendar_year(gregorian_date: date) -> int:
    """
    Determine the Buddhist calendar year (BE) for a given Gregorian date.

    Assumption:
    - Uses the common conversion: BE = CE + 543 for all Gregorian dates.
      This applies the proleptic Gregorian calendar uniformly.

    Parameters:
    - gregorian_date: A datetime.date representing the Gregorian date.

    Returns:
    - An integer representing the Buddhist Era year.
    """
    # Step 1: Extract the Gregorian year
    ce_year: int = gregorian_date.year

    # Step 2: Convert to Buddhist Era year
    be_year: int = ce_year + 543

    # Step 3: Return the BE year
    return be_year

# Entry point: buddhist_calendar_year(gregorian_date: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_79txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_buddhist_calendar_year(gregorian_date):
    result = buddhist_calendar_year(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")
