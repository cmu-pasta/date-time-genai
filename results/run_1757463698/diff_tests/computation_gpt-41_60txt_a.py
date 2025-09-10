
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def are_same_calendar_week(dt1: datetime, dt2: datetime) -> bool:
    # Step 1: Get ISO calendar info for both datetimes
    iso_year1, iso_week1, _ = dt1.isocalendar()
    iso_year2, iso_week2, _ = dt2.isocalendar()
    
    # Step 2: Compare ISO year and week for both datetimes
    same_week = (iso_year1 == iso_year2) and (iso_week1 == iso_week2)
    
    # Step 3: Return result as a boolean
    return same_week

# Entry point: are_same_calendar_week(dt1: datetime, dt2: datetime) -> bool

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_60txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_are_same_calendar_week(dt1, dt2):
    result = are_same_calendar_week(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
