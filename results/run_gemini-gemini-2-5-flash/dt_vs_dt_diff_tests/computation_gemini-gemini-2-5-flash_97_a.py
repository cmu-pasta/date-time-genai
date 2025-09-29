
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, time, timezone, timedelta, tzinfo
def get_thai_buddhist_date(gregorian_dt: datetime) -> datetime:
    # Thai Buddhist calendar year is Gregorian year + 543
    thai_buddhist_year = gregorian_dt.year + 543
    
    # Construct a new datetime object with the Thai Buddhist year
    # All other components (month, day, hour, minute, second, microsecond, tzinfo)
    # remain the same as the input Gregorian date.
    thai_buddhist_dt = gregorian_dt.replace(year=thai_buddhist_year)
    
    return thai_buddhist_dt

# Entry point: get_thai_buddhist_date(gregorian_dt: datetime) -> datetime

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_97_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_thai_buddhist_date(gregorian_dt):
    result = get_thai_buddhist_date(gregorian_dt)
    formatted_result = format_value_dt(result, gregorian_dt)
    log_file.write(formatted_result + "\n")
