
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
def find_dst_start(year: int, tz: ZoneInfo) -> date:
    # Define the start and end of the interval to search (local time in given tz)
    start = datetime(year, 1, 1, 0, 0, tzinfo=tz)
    end = datetime(year + 1, 1, 1, 0, 0, tzinfo=tz)

    # Use local noon to avoid ambiguous/non-existent local times around transitions
    one_day = timedelta(days=1)
    probe_time = timedelta(hours=12)

    # Initialize previous probe
    prev_dt = start + probe_time
    if prev_dt >= end:
        raise ValueError("Empty search interval for the given year.")
    prev_off = prev_dt.utcoffset()

    # Scan day-by-day to find the first increase in offset (DST start)
    cur_day_start = start + one_day
    while cur_day_start <= end:
        cur_dt = cur_day_start + probe_time
        if cur_dt >= end:
            break
        cur_off = cur_dt.utcoffset()

        # DST start: offset increases compared to previous day
        if cur_off is not None and prev_off is not None and cur_off > prev_off:
            # Binary search between previous day noon-window to locate the exact transition instant
            low = cur_day_start - one_day  # previous day start
            high = cur_day_start           # current day start
            # Expand search window to 24 hours around the suspected boundary
            low_dt = low
            high_dt = high

            # Ensure the transition is within [low_dt, high_dt)
            # Binary search for the earliest datetime where offset equals the "increased" offset
            target_off = cur_off
            # Narrow down to second precision
            while (high_dt - low_dt) > timedelta(seconds=1):
                mid = low_dt + (high_dt - low_dt) / 2
                # mid is aware due to arithmetic on aware datetimes
                mid_off = mid.utcoffset()
                if mid_off is not None and mid_off >= target_off:
                    high_dt = mid
                else:
                    low_dt = mid

            # The transition instant is approximately high_dt
            transition_local_date = high_dt.date()
            return transition_local_date

        # Advance to next day
        prev_dt = cur_dt
        prev_off = cur_off
        cur_day_start += one_day

    # If we reach here, no DST start occurred within the year
    raise ValueError("No DST start found for the given year and time zone.")

# Entry point: find_dst_start(year: int, tz: ZoneInfo) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_62_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timezone_strategy())
def test_find_dst_start(year, tz):
    result = find_dst_start(year, tz)
    formatted_result = format_value_dt(result, year, tz)
    log_file.write(formatted_result + "\n")
