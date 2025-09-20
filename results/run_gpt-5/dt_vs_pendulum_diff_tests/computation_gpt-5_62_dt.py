
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, timedelta, timezone
from zoneinfo import ZoneInfo
def find_dst_start(year: int, tz: ZoneInfo) -> date:
    # Helper: DST active at given aware local datetime in tz?
    def is_dst_active(dt_local: datetime) -> bool:
        dst_delta = dt_local.dst()
        return (dst_delta is not None) and (dst_delta > timedelta(0))

    # Iterate over each day of the year checking local noon to find first DST day
    # Use local noon to avoid ambiguity around midnight transitions
    prev_noon = datetime(year, 1, 1, 12, 0, tzinfo=tz)
    prev_in_dst = is_dst_active(prev_noon)

    day = date(year, 1, 2)
    while day.year == year:
        curr_noon = datetime(day.year, day.month, day.day, 12, 0, tzinfo=tz)
        curr_in_dst = is_dst_active(curr_noon)

        # Detect transition into DST (from non-DST to DST)
        if (not prev_in_dst) and curr_in_dst:
            # Narrow down the first instant of DST activation on this calendar day
            # Search between local 00:00 and local 12:00 of the current day.
            day_start_local = datetime(day.year, day.month, day.day, 0, 0, tzinfo=tz)
            day_mid_local = datetime(day.year, day.month, day.day, 12, 0, tzinfo=tz)

            # Convert bounds to UTC to avoid ambiguity/non-existent local times
            low_utc = day_start_local.astimezone(timezone.utc)
            high_utc = day_mid_local.astimezone(timezone.utc)

            # Binary search in UTC to find first instant where local time is in DST
            while (high_utc - low_utc) > timedelta(seconds=1):
                mid_utc = low_utc + (high_utc - low_utc) / 2
                mid_local = mid_utc.astimezone(tz)
                if is_dst_active(mid_local):
                    high_utc = mid_utc
                else:
                    low_utc = mid_utc

            # The first instant in DST is approximately high_utc
            dst_start_local = high_utc.astimezone(tz)
            return dst_start_local.date()

        prev_noon = curr_noon
        prev_in_dst = curr_in_dst
        day = day + timedelta(days=1)

    # If we reach here, no DST start was found in the given year for the timezone
    raise ValueError("No DST start found for the given year and timezone.")

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_62_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timezone_strategy())
def test_find_dst_start(year, tz):
    result = find_dst_start(year, tz)
    formatted_result = format_value_dt(result, year, tz)
    log_file.write(formatted_result + "\n")
