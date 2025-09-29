
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_working_hours_between(dt_start: datetime, dt_end: datetime) -> timedelta:
    """
    Calculate the total duration that falls on weekdays (Monday-Friday)
    between two datetimes, excluding all time that falls on Saturdays and Sundays.

    The result is returned as a timedelta representing the working hours (here defined
    as all hours on weekdays). If dt_end is earlier than dt_start, the duration is computed
    using the absolute interval.
    """
    # Ensure dt_start <= dt_end
    if dt_start == dt_end:
        return timedelta(0)
    if dt_start > dt_end:
        dt_start, dt_end = dt_end, dt_start

    total = timedelta(0)
    current = dt_start

    while current < dt_end:
        # Start and end boundaries for the current day
        day_start = current.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        # The end of the interval within the current day
        interval_end = dt_end if dt_end < day_end else day_end

        # Weekday check: Monday=0 ... Sunday=6
        if day_start.weekday() < 5:
            total += interval_end - current

        # Move to the next segment
        current = interval_end

    return total

# Entry point: calculate_working_hours_between(dt_start: datetime, dt_end: datetime) -> timedelta

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_24txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_working_hours_between(dt_start, dt_end):
    result = calculate_working_hours_between(dt_start, dt_end)
    formatted_result = format_value_dt(result, dt_start, dt_end)
    log_file.write(formatted_result + "\n")
