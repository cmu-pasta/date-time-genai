
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def find_first_day_of_spring(year: int) -> datetime:
    # Simplified calculation for vernal equinox
    # This approximation works well for years 1900-2100
    
    # Base calculation: March 20th + fractional adjustment
    # The vernal equinox cycles roughly every 4 years due to leap years
    day_offset = (year - 2000) // 4
    
    # For most years in the 21st century, it falls on March 20th
    base_day = 20
    
    # Adjust for the specific year within the 4-year cycle
    year_in_cycle = year % 4
    if year_in_cycle == 0:  # Leap years
        adjusted_day = base_day
    elif year_in_cycle == 1:
        adjusted_day = base_day
    elif year_in_cycle == 2:
        adjusted_day = base_day
    else:  # year_in_cycle == 3
        adjusted_day = base_day + 1  # Often March 21st
    
    # Handle century adjustments (simplified)
    if year >= 2000 and year < 2100:
        if year <= 2011:
            spring_day = 20
        elif year >= 2012 and year <= 2015:
            spring_day = 20
        elif year >= 2016 and year <= 2019:
            spring_day = 20
        elif year >= 2020 and year <= 2023:
            spring_day = 20
        else:
            # For years after 2023, use the calculated adjustment
            spring_day = adjusted_day
    else:
        # For years outside 2000-2099, use March 20th as default
        spring_day = 20
    
    # Create and return the datetime object for the first day of spring
    return datetime(year, 3, spring_day)

# Entry point: find_first_day_of_spring(year: int) -> datetime

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_44_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_first_day_of_spring(year):
    result = find_first_day_of_spring(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
