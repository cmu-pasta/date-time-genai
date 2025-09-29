
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def convert_to_julian_day_number(dt: datetime) -> int:
    # Step 1: Get the ordinal day number from the datetime object
    ordinal_day = dt.toordinal()
    
    # Step 2: Convert to Julian Day Number by adding the offset
    # January 1, year 1 CE has ordinal 1 and Julian Day Number 1721426
    julian_day_number = ordinal_day + 1721425
    
    # Step 3: Return the Julian day number as an integer
    return julian_day_number

# Entry point: convert_to_julian_day_number(dt: datetime) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_10_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_to_julian_day_number(dt):
    result = convert_to_julian_day_number(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
