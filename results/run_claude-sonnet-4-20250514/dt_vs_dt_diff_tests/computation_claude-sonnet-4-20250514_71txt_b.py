
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def find_vernal_equinox(year: int) -> date:
    # Base reference: March 20, 2000 (a known vernal equinox date)
    base_year = 2000
    base_month = 3
    base_day = 20
    
    # Calculate year difference from base year
    year_diff = year - base_year
    
    # Approximate shift: 0.2422 days per year minus leap day corrections
    day_shift = year_diff * 0.2422
    
    # Subtract leap day corrections (every 4 years)
    leap_corrections = year_diff // 4
    day_shift -= leap_corrections
    
    # Calculate the approximate day in March
    equinox_day = base_day + int(round(day_shift))
    
    # Ensure the day falls within valid March dates (19-22 typical range)
    if equinox_day < 19:
        equinox_day = 19
    elif equinox_day > 22:
        equinox_day = 22
    
    return date(year, base_month, equinox_day)

# Entry point: find_vernal_equinox(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_71txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_vernal_equinox(year):
    result = find_vernal_equinox(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
