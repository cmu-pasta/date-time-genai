
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def find_nowruz_date(year: int) -> datetime:
    # Persian New Year (Nowruz) typically falls on March 20 or March 21
    # This is based on the spring equinox
    
    # Simplified calculation: 
    # For leap years and the year after leap years, Nowruz is often March 21
    # For other years, it's typically March 20
    
    # Check if the year is a leap year in Gregorian calendar
    is_leap_year = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    # Check if the previous year was a leap year
    prev_year_leap = ((year - 1) % 4 == 0 and (year - 1) % 100 != 0) or ((year - 1) % 400 == 0)
    
    # Nowruz date calculation
    # Generally March 20, but March 21 for leap years and years after leap years
    if is_leap_year or prev_year_leap:
        nowruz_date = datetime(year, 3, 21)
    else:
        nowruz_date = datetime(year, 3, 20)
    
    return nowruz_date

# Entry point: find_nowruz_date(year: int) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_89_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_nowruz_date(year):
    result = find_nowruz_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
