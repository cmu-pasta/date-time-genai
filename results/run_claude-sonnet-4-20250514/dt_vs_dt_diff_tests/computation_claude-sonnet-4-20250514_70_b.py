
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def julian_to_gregorian(julian_date: datetime) -> datetime:
    # Extract year, month, day from the Julian date
    year = julian_date.year
    month = julian_date.month
    day = julian_date.day
    
    # Convert Julian date to Julian Day Number
    # Julian Day Number calculation for Julian calendar
    if month <= 2:
        year -= 1
        month += 12
    
    # Julian calendar Julian Day Number calculation
    a = year // 100
    b = 2 - a + (a // 4)  # This is 0 for Julian calendar
    b = 0  # For Julian calendar, we don't apply the Gregorian correction
    
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524
    
    # Convert Julian Day Number back to Gregorian date
    # Gregorian calendar conversion from Julian Day Number
    a = jd + 32044
    b = (4 * a + 3) // 146097
    c = a - (146097 * b) // 4
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    
    greg_day = e - (153 * m + 2) // 5 + 1
    greg_month = m + 3 - 12 * (m // 10)
    greg_year = 100 * b + d - 4800 + m // 10
    
    # Create and return the Gregorian datetime object
    gregorian_date = datetime(greg_year, greg_month, greg_day, 
                            julian_date.hour, julian_date.minute, 
                            julian_date.second, julian_date.microsecond)
    
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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_70_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_julian_to_gregorian(julian_date):
    result = julian_to_gregorian(julian_date)
    formatted_result = format_value_dt(result, julian_date)
    log_file.write(formatted_result + "\n")
