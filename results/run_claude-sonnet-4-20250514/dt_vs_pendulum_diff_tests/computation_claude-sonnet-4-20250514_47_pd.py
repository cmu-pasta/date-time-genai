
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_memorial_day(year: int) -> pendulum.Date:
    # Step 1: Create May 31st of the given year
    may_31 = pendulum.date(year, 5, 31)
    
    # Step 2: Find what day of the week May 31st is (Monday=1, Sunday=7)
    day_of_week = may_31.day_of_week
    
    # Step 3: Calculate how many days to go back to get to the last Monday
    # If May 31st is Monday (1), go back 0 days
    # If May 31st is Tuesday (2), go back 1 day, etc.
    days_back = (day_of_week - 1) % 7
    
    # Step 4: Subtract the days to get to the last Monday of May
    memorial_day = may_31.subtract(days=days_back)
    
    return memorial_day

# Entry point: find_memorial_day(year: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_47_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_memorial_day(year):
    result = find_memorial_day(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
