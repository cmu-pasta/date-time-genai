
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def convert_to_modified_julian_date(dt: datetime) -> float:
    # Extract year, month, day from datetime
    year = dt.year
    month = dt.month
    day = dt.day
    
    # Add fractional day based on time
    hour_fraction = dt.hour / 24.0
    minute_fraction = dt.minute / (24.0 * 60.0)
    second_fraction = dt.second / (24.0 * 60.0 * 60.0)
    microsecond_fraction = dt.microsecond / (24.0 * 60.0 * 60.0 * 1000000.0)
    
    fractional_day = day + hour_fraction + minute_fraction + second_fraction + microsecond_fraction
    
    # Julian Date calculation algorithm
    if month <= 2:
        year = year - 1
        month = month + 12
    
    # Calculate A and B for Gregorian calendar correction
    a = int(year / 100)
    b = 2 - a + int(a / 4)
    
    # Calculate Julian Date
    julian_date = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + fractional_day + b - 1524.5
    
    # Convert to Modified Julian Date
    modified_julian_date = julian_date - 2400000.5
    
    return modified_julian_date

# Entry point: convert_to_modified_julian_date(dt: datetime) -> float

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_94_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_to_modified_julian_date(dt):
    result = convert_to_modified_julian_date(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
