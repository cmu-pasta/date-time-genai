
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, time
import calendar
def end_of_month_timestamp(dt: datetime) -> datetime:
    # Step 1: Find the last day in the month
    last_day = calendar.monthrange(dt.year, dt.month)[1]
    # Step 2: Construct a datetime for the last second of the last day
    end_of_month = datetime(
        year=dt.year,
        month=dt.month,
        day=last_day,
        hour=23,
        minute=59,
        second=59,
        tzinfo=dt.tzinfo  # Preserve timezone info, if present
    )
    return end_of_month

# Entry point: end_of_month_timestamp(dt: datetime) -> datetime

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_82txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_end_of_month_timestamp(dt):
    result = end_of_month_timestamp(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
