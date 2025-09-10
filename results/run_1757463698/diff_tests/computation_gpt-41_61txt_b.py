
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime
def get_nth_day_of_year(dt: date) -> int:
    # Step 1: Use the timetuple method to access tm_yday
    nth_day = dt.timetuple().tm_yday
    
    # Step 2: Return the day of the year as an integer
    return nth_day

# Entry point: get_nth_day_of_year(dt: date) -> int

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_61txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_get_nth_day_of_year(dt):
    result = get_nth_day_of_year(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
