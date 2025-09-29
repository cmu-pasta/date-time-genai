
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_autumnal_equinox(year: int) -> pendulum.Date:
    # Simplified approximation for autumnal equinox calculation
    # Base date is September 22, with adjustments based on the year
    
    # Calculate the day offset using a simplified astronomical formula
    # This accounts for the gradual shift of equinox dates over time
    day_offset = ((year - 2000) * 0.25) % 1
    
    # Determine if it's September 22 or 23
    if day_offset < 0.5:
        equinox_day = 22
    else:
        equinox_day = 23
    
    # Handle leap year adjustments for better accuracy
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        # Leap year adjustment
        if day_offset > 0.75:
            equinox_day = 23
    
    # Create and return the autumnal equinox date
    autumnal_equinox_date = pendulum.date(year, 9, equinox_day)
    
    return autumnal_equinox_date

# Entry point: find_autumnal_equinox(year: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_53_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_autumnal_equinox(year):
    result = find_autumnal_equinox(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
