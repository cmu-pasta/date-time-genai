
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def julian_to_gregorian(julian_date: datetime) -> datetime:
    """
    Convert a Julian calendar date to Gregorian calendar date.
    
    Args:
        julian_date: A datetime object representing a date in the Julian calendar
    
    Returns:
        A datetime object representing the equivalent date in the Gregorian calendar
    """
    
    year = julian_date.year
    
    # Calculate the offset between Julian and Gregorian calendars
    # Formula: (year // 100) - (year // 400) - 2
    # This accounts for the different leap year rules
    if year >= 300:
        offset = (year // 100) - (year // 400) - 2
    else:
        # For years before 300 CE, use a simpler calculation
        offset = 0
    
    # Convert Julian date to Gregorian by adding the offset
    gregorian_date = julian_date + timedelta(days=offset)
    
    return gregorian_date

# Entry point: julian_to_gregorian(julian_date: datetime) -> datetime

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_70txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_julian_to_gregorian(julian_date):
    result = julian_to_gregorian(julian_date)
    formatted_result = format_value_dt(result, julian_date)
    log_file.write(formatted_result + "\n")
