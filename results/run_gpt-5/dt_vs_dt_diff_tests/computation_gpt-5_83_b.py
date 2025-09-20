
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo
def find_dst_end_date(year: int, tz: ZoneInfo) -> date:
    """
    Returns the calendar date in the given year when daylight saving time ends
    for the specified timezone. If the timezone does not observe a DST end in
    that year, returns date.min.
    """
    # Start from January 2 to allow checking the previous day
    d = date(year, 1, 2)
    end = date(year, 12, 31)

    # Helper to get DST offset at local noon for a given date
    def dst_at_noon(day: date) -> timedelta:
        local_noon = datetime.combine(day, time(12, 0), tzinfo=tz)
        return local_noon.dst() or timedelta(0)

    prev_day = d - timedelta(days=1)
    prev_dst = dst_at_noon(prev_day)

    while d <= end:
        cur_dst = dst_at_noon(d)
        # Detect a drop from positive DST offset to zero: DST ended on 'd'
        if prev_dst > timedelta(0) and cur_dst == timedelta(0):
            return d
        prev_dst = cur_dst
        d += timedelta(days=1)

    # No DST end found for this year in this timezone
    return date.min

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_83_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timezone_strategy())
def test_find_dst_end_date(year, tz):
    result = find_dst_end_date(year, tz)
    formatted_result = format_value_dt(result, year, tz)
    log_file.write(formatted_result + "\n")
