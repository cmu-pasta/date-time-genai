
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def find_nowruz_date(year: int) -> date:
    # Simplified calculation for spring equinox date
    # Base year 2000 had spring equinox on March 20
    # The equinox shifts by approximately 0.25 days per year
    
    # Calculate the shift from year 2000
    years_from_2000 = year - 2000
    
    # Basic calculation: starts with March 20 in year 2000
    # Each year shifts by about 6 hours (0.25 days)
    day_shift = (years_from_2000 * 0.25) % 1
    
    # Account for leap year corrections
    leap_corrections = years_from_2000 // 4
    
    # Determine if it's March 20 or March 21
    # This is a simplified approximation
    if (years_from_2000 + leap_corrections) % 4 < 2:
        nowruz_day = 20
    else:
        nowruz_day = 21
    
    # For more accuracy, we can use a pattern-based approach
    # Most years: March 20, but some years it's March 21
    # This simplified version uses the 4-year cycle pattern
    if year % 4 == 1 or year % 4 == 2:
        nowruz_day = 21
    else:
        nowruz_day = 20
    
    return date(year, 3, nowruz_day)

# Entry point: find_nowruz_date(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_89txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_nowruz_date(year):
    result = find_nowruz_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
