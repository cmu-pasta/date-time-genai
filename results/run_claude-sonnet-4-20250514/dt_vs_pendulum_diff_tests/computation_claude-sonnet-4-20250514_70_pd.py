
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def convert_julian_to_gregorian(julian_date: pendulum.Date) -> pendulum.Date:
    # Calculate the offset between Julian and Gregorian calendars
    # The offset depends on the century
    year = julian_date.year
    
    # Calculate the number of centuries since year 1
    centuries = year // 100
    
    # The offset is calculated as: centuries - centuries//4 - 2
    # This accounts for the different leap year rules
    if year >= 1582:  # Gregorian calendar was introduced in 1582
        offset = centuries - centuries // 4 - 2
    else:
        offset = 0  # No offset before Gregorian calendar introduction
    
    # Add the offset to convert Julian to Gregorian
    gregorian_date = julian_date.add(days=offset)
    
    return gregorian_date

# Entry point: convert_julian_to_gregorian(julian_date: pendulum.Date) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_70_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_convert_julian_to_gregorian(julian_date):
    result = convert_julian_to_gregorian(julian_date)
    formatted_result = format_value_pd(result, julian_date)
    log_file.write(formatted_result + "\n")
