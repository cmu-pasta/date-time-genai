
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_sundays_in_february(year: int) -> int:
    """
    Determine the number of Sundays in February for a given year.

    Parameters:
        year (int): The year for which to compute the number of Sundays in February.

    Returns:
        int: The count of Sundays in February of the given year.
    """
    # Step 1: Determine the first day of February for the given year
    feb_start = date(year, 2, 1)
    
    # Step 2: Determine the last day of February by taking March 1st and subtracting one day
    march_first = date(year, 3, 1)
    feb_end = march_first - timedelta(days=1)
    
    # Step 3: Iterate through all days in February and count Sundays (weekday() == 6)
    count = 0
    current = feb_start
    one_day = timedelta(days=1)
    while current <= feb_end:
        if current.weekday() == 6:  # Monday=0 ... Sunday=6
            count += 1
        current += one_day
    
    # Step 4: Return the number of Sundays
    return count

# Entry point: count_sundays_in_february(year: int) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_49txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_count_sundays_in_february(year):
    result = count_sundays_in_february(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
