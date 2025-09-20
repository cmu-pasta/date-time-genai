
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def _is_in_dst(dt: pendulum.DateTime) -> bool:
    # A non-zero DST offset indicates DST is in effect
    return dt.dst().in_seconds() != 0

def find_dst_end_date(year: int, tz: pendulum.Timezone) -> pendulum.Date:
    # Start at the beginning of the year in the given timezone
    current = pendulum.datetime(year, 1, 1, 0, 0, 0, tz=tz)
    end_of_year = pendulum.datetime(year, 12, 31, 23, 59, 59, tz=tz)

    prev = current
    prev_in_dst = _is_in_dst(prev)

    # Iterate hour by hour to find a True -> False DST transition
    while prev <= end_of_year:
        nxt = prev.add(hours=1)
        nxt_in_dst = _is_in_dst(nxt)

        # DST ends when we move from DST (True) to Standard Time (False)
        if prev_in_dst and not nxt_in_dst:
            # The transition occurs within this hour; return the date of the transition
            return nxt.date()

        prev = nxt
        prev_in_dst = nxt_in_dst

    # If no DST end was found for this timezone/year, raise an error
    raise ValueError("No DST end found for the specified year and timezone.")

# Entry point: find_dst_end_date(year: int, tz: pendulum.Timezone) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_83_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timezone_strategy())
def test_find_dst_end_date(year, tz):
    result = find_dst_end_date(year, tz)
    formatted_result = format_value_pd(result, year, tz)
    log_file.write(formatted_result + "\n")
