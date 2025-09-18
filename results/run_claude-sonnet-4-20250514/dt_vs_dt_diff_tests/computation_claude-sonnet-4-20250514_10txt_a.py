
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def date_to_julian_day(input_date: date) -> float:
    # Step 1: Get the ordinal day number (days since January 1, 0001 CE)
    ordinal_day = input_date.toordinal()
    
    # Step 2: Convert to Julian day number
    # Julian day number for January 1, 0001 CE at noon is 1721426
    # Since toordinal() returns 1 for January 1, 0001 CE, we add 1721425
    julian_day = ordinal_day + 1721425
    
    # Step 3: Return as float (Julian day numbers are typically expressed as floats)
    return float(julian_day)

# Entry point: date_to_julian_day(input_date: date) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_10txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_date_to_julian_day(input_date):
    result = date_to_julian_day(input_date)
    formatted_result = format_value_dt(result, input_date)
    log_file.write(formatted_result + "\n")
