
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date
def find_persian_new_year(year: int) -> date:
    # Persian New Year (Nowruz) typically falls on March 20 or 21
    # Based on the vernal equinox, which varies slightly year to year
    # For a simplified calculation using only datetime library:
    # Most years: March 20
    # Some years (especially around leap years): March 21
    
    # This is a simplified approximation since exact calculation requires
    # astronomical data not available in datetime library
    # Generally, March 21 occurs more frequently in leap years and surrounding years
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        # Leap year - more likely to be March 21
        nowruz_date = date(year, 3, 21)
    elif (year + 1) % 4 == 0 or (year - 1) % 4 == 0:
        # Year before or after leap year - also more likely March 21
        nowruz_date = date(year, 3, 21)
    else:
        # Most common case - March 20
        nowruz_date = date(year, 3, 20)
    
    return nowruz_date

# Entry point: find_persian_new_year(year: int) -> date

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_89_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_persian_new_year(year):
    result = find_persian_new_year(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
