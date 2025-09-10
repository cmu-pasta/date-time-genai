
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def get_iso_week_start(dt: datetime) -> datetime:
    # Step 1: Find the weekday (Monday=0, Sunday=6 according to ISO standard)
    weekday = dt.weekday()
    
    # Step 2: Subtract the number of days since Monday to move to the start of the ISO week
    iso_week_start_date = dt - timedelta(days=weekday)
    
    # Step 3: Replace time to midnight (00:00:00) while keeping the original timezone (if any)
    iso_week_start = iso_week_start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Step 4: Return the result
    return iso_week_start

# Entry point: get_iso_week_start(dt: datetime) -> datetime

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_58txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_iso_week_start(dt):
    result = get_iso_week_start(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
