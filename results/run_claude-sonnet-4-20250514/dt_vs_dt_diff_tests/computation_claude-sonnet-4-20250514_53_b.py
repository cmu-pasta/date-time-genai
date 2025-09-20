
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def find_autumnal_equinox(year: int) -> datetime:
    # Step 1: Use simplified astronomical approximation
    # Base calculation: autumnal equinox typically falls around September 22-23
    
    # Step 2: Calculate offset from reference year 2000
    # The equinox shifts approximately 0.25 days per year due to leap year cycle
    base_day = 22.5  # Base day in September (22.5 means between 22nd and 23rd)
    
    # Step 3: Apply year-based adjustment
    # Account for leap year cycle (shifts about 6 hours per year, resets every 4 years)
    year_offset = (year - 2000) * 0.25
    
    # Step 4: Calculate the day, accounting for leap year resets
    adjusted_day = base_day + year_offset - ((year - 2000) // 4) * 1.0
    
    # Step 5: Determine if it falls on September 22 or 23
    if adjusted_day < 23:
        equinox_day = 22
    else:
        equinox_day = 23
    
    # Step 6: Create and return the datetime object
    # Set to noon for the equinox time
    return datetime(year, 9, equinox_day, 12, 0, 0)

# Entry point: find_autumnal_equinox(year: int) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_53_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_autumnal_equinox(year):
    result = find_autumnal_equinox(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
