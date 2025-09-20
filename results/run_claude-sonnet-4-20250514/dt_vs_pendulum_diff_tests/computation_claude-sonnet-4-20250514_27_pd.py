
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_leap_years_between(year1: int, year2: int) -> int:
    # Determine the start and end years (inclusive range)
    start_year = min(year1, year2)
    end_year = max(year1, year2)
    
    leap_count = 0
    
    # Iterate through each year in the range
    for year in range(start_year, end_year + 1):
        # Create a date object for the current year to check if it's a leap year
        date = pendulum.date(year, 1, 1)
        if date.is_leap_year():
            leap_count += 1
    
    return leap_count

# Entry point: calculate_leap_years_between(year1: int, year2: int) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_27_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_calculate_leap_years_between(year1, year2):
    result = calculate_leap_years_between(year1, year2)
    formatted_result = format_value_pd(result, year1, year2)
    log_file.write(formatted_result + "\n")
