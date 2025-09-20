
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def working_hours_between(start: datetime, end: datetime) -> timedelta:
    """
    Calculate the working hours between two datetimes excluding weekends.
    Working hours here are defined as all time that falls on weekdays (Monday–Friday),
    with no specific daily business-hour window (i.e., any time on a weekday counts).
    
    Parameters:
        start (datetime): The starting datetime.
        end   (datetime): The ending datetime.
    
    Returns:
        timedelta: The total duration that falls on weekdays between start and end.
    """
    # Step 1: Normalize order to ensure start <= end
    if end < start:
        start, end = end, start

    # Quick exit for equality
    if start == end:
        return timedelta(0)

    total = timedelta(0)
    current = start

    while current < end:
        # Step 2: Determine the boundary at the next midnight in current's timezone
        start_of_day = current.replace(hour=0, minute=0, second=0, microsecond=0)
        next_midnight = start_of_day + timedelta(days=1)

        # Step 3: Clip the day's upper bound to the end datetime
        upper = next_midnight if next_midnight < end else end

        # Step 4: If it's a weekday (Mon-Fri), accumulate the overlap
        if current.weekday() < 5:
            if upper > current:
                total += (upper - current)

        # Step 5: Move to the next segment/day
        current = upper

    return total

# Entry point: working_hours_between(start: datetime, end: datetime) -> timedelta

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_24_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_working_hours_between(start, end):
    result = working_hours_between(start, end)
    formatted_result = format_value_dt(result, start, end)
    log_file.write(formatted_result + "\n")
