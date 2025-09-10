
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def time_until_event_in_weeks_and_days(current_time: datetime, future_event_time: datetime) -> int:
    """
    Calculates the time remaining until a future event in weeks and days.
    Returns the number of weeks and days as two integers, separated by a comma.
    If the event is in the past, both values will be zero.
    """
    # Step 1: Calculate the timedelta between now and the event
    delta = future_event_time - current_time

    # Step 2: If the event is in the past, return 0 weeks and 0 days
    if delta.days <= 0:
        print(0)
        print(0)
        return

    # Step 3: Convert days to weeks and remaining days
    weeks = delta.days // 7
    days = delta.days % 7

    # Step 4: Return the result: weeks and days as integers, each on its own line
    print(weeks)
    print(days)

# Entry point: time_until_event_in_weeks_and_days(current_time: datetime, future_event_time: datetime) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_34txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_time_until_event_in_weeks_and_days(current_time, future_event_time):
    result = time_until_event_in_weeks_and_days(current_time, future_event_time)
    formatted_result = format_value_dt(result, current_time, future_event_time)
    log_file.write(formatted_result + "\n")
