
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def convert_julian_to_gregorian(julian_date: datetime) -> datetime:
    # Extract the year from the Julian date
    year = julian_date.year
    
    # Calculate the century
    century = year // 100
    
    # Calculate the offset between Julian and Gregorian calendars
    # This formula gives the number of days Julian is behind Gregorian
    if year >= 1582:  # Gregorian calendar was introduced in 1582
        offset = century - century // 4 - 2
    else:
        offset = 0  # Before 1582, no adjustment needed as both would be Julian
    
    # Add the offset to convert Julian to Gregorian
    gregorian_date = julian_date + timedelta(days=offset)
    
    return gregorian_date

# Entry point: convert_julian_to_gregorian(julian_date: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_70_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_julian_to_gregorian(julian_date):
    result = convert_julian_to_gregorian(julian_date)
    formatted_result = format_value_dt(result, julian_date)
    log_file.write(formatted_result + "\n")
