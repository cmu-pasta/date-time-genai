
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def _binary_search_dst_start(start_dt: pendulum.DateTime, end_dt: pendulum.DateTime) -> pendulum.DateTime:
    """
    Given a window [start_dt, end_dt] where is_dst flips from False to True,
    binary search to find the exact transition instant (to the second).
    """
    # Ensure start is non-DST and end is DST
    if not (start_dt.is_dst() is False and end_dt.is_dst() is True):
        raise ValueError("Search window must start in standard time and end in daylight saving time.")

    # Use timestamps to avoid issues around nonexistent/ambiguous local times
    lo = start_dt.int_timestamp
    hi = end_dt.int_timestamp

    # Binary search for the first timestamp where is_dst becomes True
    while lo < hi:
        mid = (lo + hi) // 2
        mid_dt = pendulum.from_timestamp(mid, tz=start_dt.timezone)
        if mid_dt.is_dst():
            hi = mid
        else:
            lo = mid + 1

    # lo (== hi) is the first second where DST is True
    transition_dt = pendulum.from_timestamp(lo, tz=start_dt.timezone)
    return transition_dt

def find_dst_start_date(year: int, tz: pendulum.Timezone) -> pendulum.Date:
    """
    Find the date when daylight saving time starts for a given year and timezone.

    Inputs:
      - year: int (target calendar year)
      - tz: pendulum.Timezone

    Output:
      - pendulum.Date representing the date of DST start within the given year.

    Raises:
      - ValueError if the timezone has no DST start within the given year.
    """
    # Start at the very beginning of the year in the given timezone
    current = pendulum.datetime(year, 1, 1, 0, 0, 0, tz=tz)
    end_of_year = pendulum.datetime(year, 12, 31, 23, 59, 59, tz=tz)

    one_day = pendulum.duration(days=1)

    # Iterate day by day to find a window where DST flips from False to True
    while current <= end_of_year:
        next_day = current + one_day
        # Clamp next_day to end_of_year + 1s window if needed
        if next_day > end_of_year:
            next_day = end_of_year

        # Check is_dst at the start of 'current' day and the start of the following day
        start_is_dst = current.is_dst()
        # Use midnight of the next day (or end_of_year if clamped)
        next_midnight = pendulum.datetime(current.year, current.month, current.day, 0, 0, 0, tz=tz) + one_day
        if next_midnight > end_of_year:
            next_midnight = end_of_year

        end_is_dst = next_midnight.is_dst()

        # Detect a False -> True transition inside this day
        if start_is_dst is False and end_is_dst is True:
            # Binary search between current midnight and next midnight
            transition_dt = _binary_search_dst_start(current, next_midnight)
            return transition_dt.date()

        # Advance to next day
        current = current + one_day

    # If we finish the loop without finding a start of DST
    raise ValueError("No DST start found in the specified year for the given timezone.")

# Entry point: find_dst_start_date(year: int, tz: pendulum.Timezone) -> pendulum.Date

def format_value_pd(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, pendulum.DateTime):
            formatted_values.append(value.to_iso8601_string()[:-1])
        elif isinstance(value, pendulum.Date):
            formatted_values.append(value.to_date_string())
        elif isinstance(value, pendulum.Time):
            # Format time in the same way as datetime.time.isoformat() does
            formatted_time = (
                str(value.hour).zfill(2)
                + ":"
                + str(value.minute).zfill(2)
                + ":"
                + str(value.second).zfill(2)
            )
            if value.microsecond:
                # Padding microseconds to 6 digits
                formatted_time += "." + str(value.microsecond).zfill(6)
            formatted_values.append(formatted_time)
        elif isinstance(value, pendulum.Duration):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_62_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timezone_strategy())
def test_find_dst_start_date(year, tz):
    result = find_dst_start_date(year, tz)
    formatted_result = format_value_pd(result, year, tz)
    log_file.write(formatted_result + "\n")
