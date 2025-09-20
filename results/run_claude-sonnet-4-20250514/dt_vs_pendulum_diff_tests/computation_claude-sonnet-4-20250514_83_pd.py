
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_dst_end_date(year: int, timezone: pendulum.Timezone) -> pendulum.DateTime:
    # Create a datetime at the beginning of the year in the given timezone
    start_of_year = pendulum.datetime(year, 1, 1, tz=timezone)
    end_of_year = pendulum.datetime(year, 12, 31, 23, 59, 59, tz=timezone)
    
    # Get timezone transitions for the year
    transitions = timezone.transitions(start_of_year, end_of_year)
    
    # Find the DST end transition (when offset decreases - fall back)
    for transition in transitions:
        # Check if this is a "fall back" transition (DST ending)
        # This happens when the UTC offset decreases
        before_transition = transition.at.subtract(hours=1)
        after_transition = transition.at.add(hours=1)
        
        if before_transition.utc_offset() > after_transition.utc_offset():
            return transition.at
    
    # If no DST end transition found, return None converted to start of year
    # (This handles timezones that don't observe DST)
    return start_of_year

# Entry point: find_dst_end_date(year: int, timezone: pendulum.Timezone) -> pendulum.DateTime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_83_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timezone_strategy())
def test_find_dst_end_date(year, timezone):
    result = find_dst_end_date(year, timezone)
    formatted_result = format_value_pd(result, year, timezone)
    log_file.write(formatted_result + "\n")
