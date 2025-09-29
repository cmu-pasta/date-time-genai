
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def find_vernal_equinox(year: int) -> datetime:
    # Step 1: Calculate the approximate day in March using astronomical formula
    # This is a commonly used approximation for the vernal equinox
    day_of_march = 20.25 - (year - 2000) / 128
    
    # Step 2: Extract the day and fractional part
    day = int(day_of_march)
    fractional_day = day_of_march - day
    
    # Step 3: Convert fractional day to hours
    hours = fractional_day * 24
    hour = int(hours)
    minutes = int((hours - hour) * 60)
    
    # Step 4: Create and return the datetime object
    # March is month 3, and we use the calculated day and time
    vernal_equinox = datetime(year, 3, day, hour, minutes)
    
    return vernal_equinox

# Entry point: find_vernal_equinox(year: int) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_71_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_vernal_equinox(year):
    result = find_vernal_equinox(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
