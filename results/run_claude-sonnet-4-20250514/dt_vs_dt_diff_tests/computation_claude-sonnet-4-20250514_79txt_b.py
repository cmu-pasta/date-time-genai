
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def gregorian_to_buddhist_year(gregorian_date: datetime) -> int:
    # Step 1: Extract the Gregorian year from the datetime object
    gregorian_year = gregorian_date.year
    
    # Step 2: Convert to Buddhist calendar year by adding 543
    # The Buddhist Era (BE) traditionally starts 543 years before the Common Era
    buddhist_year = gregorian_year + 543
    
    # Step 3: Return the Buddhist calendar year as an integer
    return buddhist_year

# Entry point: gregorian_to_buddhist_year(gregorian_date: datetime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_79txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_gregorian_to_buddhist_year(gregorian_date):
    result = gregorian_to_buddhist_year(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")
