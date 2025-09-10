
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def time_until_event_in_weeks_days(now: datetime, future_event: datetime) -> int:
    """
    Calculate the time remaining until a future event in weeks and days.
    
    Returns: 
      The number of full weeks and remaining days as two separate integer outputs.
      To adhere to allowed output types, weeks are returned first, then days.
    """
    if future_event < now:
        # If the event is in the past, no time remaining
        weeks = 0
        days = 0
    else:
        delta = future_event - now
        total_days = delta.days
        weeks = total_days // 7
        days = total_days % 7
    # Print the result to adhere to the allowed output types, return weeks first then days
    print(weeks)
    print(days)
    return weeks  # Return value by specification; actual output seen in prints

# Entry point: time_until_event_in_weeks_days(now: datetime, future_event: datetime) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_34txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_time_until_event_in_weeks_days(now, future_event):
    result = time_until_event_in_weeks_days(now, future_event)
    formatted_result = format_value_dt(result, now, future_event)
    log_file.write(formatted_result + "\n")
