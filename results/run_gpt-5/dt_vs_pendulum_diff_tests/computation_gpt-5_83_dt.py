
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo
def find_dst_end_date(year: int, tz: ZoneInfo) -> date:
    # Start at the first moment of the year in the given timezone
    start_of_year = datetime(year, 1, 1, 0, 0, tzinfo=tz)
    start_of_next_year = datetime(year + 1, 1, 1, 0, 0, tzinfo=tz)

    current = start_of_year
    # Iterate through each day of the year
    while current < start_of_next_year:
        next_day = current + timedelta(days=1)
        # Compare DST offsets at local midnight for consecutive days
        dst_current = tz.dst(current)
        dst_next = tz.dst(next_day)

        # Detect DST end: a decrease in DST offset between consecutive midnights
        if dst_current is not None and dst_next is not None and dst_next < dst_current:
            return current.date()

        current = next_day

    # If no DST end is detected in the year for this timezone, signal this condition
    raise ValueError("No daylight saving time end found for the given year and timezone.")

# Entry point: find_dst_end_date(year: int, tz: ZoneInfo) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_83_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timezone_strategy())
def test_find_dst_end_date(year, tz):
    result = find_dst_end_date(year, tz)
    formatted_result = format_value_dt(result, year, tz)
    log_file.write(formatted_result + "\n")
