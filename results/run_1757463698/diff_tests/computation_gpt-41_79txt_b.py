
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def first_day_of_iso_week(year: int, iso_week: int) -> date:
    # Step 1: Calculate the Monday (first day) of the specific ISO week using fromisocalendar
    first_day = date.fromisocalendar(year, iso_week, 1)
    
    # Step 2: Return the computed date
    return first_day

# Entry point: first_day_of_iso_week(year: int, iso_week: int) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_79txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_first_day_of_iso_week(year, iso_week):
    result = first_day_of_iso_week(year, iso_week)
    formatted_result = format_value_dt(result, year, iso_week)
    log_file.write(formatted_result + "\n")
