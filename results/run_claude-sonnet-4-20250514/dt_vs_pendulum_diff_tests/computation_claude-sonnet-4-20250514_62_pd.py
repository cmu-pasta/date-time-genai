
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_dst_start_date(year: int, timezone: pendulum.Timezone) -> pendulum.DateTime:
    # Start from January 1st of the given year
    current_date = pendulum.datetime(year, 1, 1, tz=timezone)
    
    # Check if DST is active at the start of the year
    prev_dst_active = current_date.dst().total_seconds() > 0
    
    # Iterate through each day of the year
    for day_offset in range(1, 366):  # Up to 365 days (366 for leap years)
        try:
            current_date = pendulum.datetime(year, 1, 1, tz=timezone).add(days=day_offset)
            current_dst_active = current_date.dst().total_seconds() > 0
            
            # If DST just became active (transition from False to True)
            if not prev_dst_active and current_dst_active:
                return current_date
            
            prev_dst_active = current_dst_active
            
        except:
            # Handle potential edge cases like invalid dates
            continue
    
    # If no DST start found, return None as DateTime (this shouldn't happen for valid timezones with DST)
    # For the constraint, we'll return the start of year if no DST transition is found
    return pendulum.datetime(year, 1, 1, tz=timezone)

# Entry point: find_dst_start_date(year: int, timezone: pendulum.Timezone) -> pendulum.DateTime

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_62_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timezone_strategy())
def test_find_dst_start_date(year, timezone):
    result = find_dst_start_date(year, timezone)
    formatted_result = format_value_pd(result, year, timezone)
    log_file.write(formatted_result + "\n")
