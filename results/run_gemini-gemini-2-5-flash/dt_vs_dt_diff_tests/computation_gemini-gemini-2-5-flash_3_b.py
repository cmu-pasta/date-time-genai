
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def determine_next_leap_year(dt: datetime) -> int:
    """
    Determines the next leap year after a given date.

    Args:
        dt: The given date as a datetime object.

    Returns:
        An integer representing the next leap year after the given date.
    """
    # Start checking from the year immediately after the given date's year.
    # This ensures we always find a leap year strictly after the input date.
    current_year = dt.year + 1

    while True:
        # Step 1 & 2: Implement the leap year check
        # A year is a leap year if it is divisible by 4,
        # unless it is divisible by 100 but not by 400.
        is_leap_year = (current_year % 4 == 0 and current_year % 100 != 0) or \
                       (current_year % 400 == 0)

        if is_leap_year:
            # Step 3: Return the found leap year
            return current_year
        
        # Move to the next year if the current_year is not a leap year
        current_year += 1

# Entry point: determine_next_leap_year(dt: datetime) -> int

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_3_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_determine_next_leap_year(dt):
    result = determine_next_leap_year(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
