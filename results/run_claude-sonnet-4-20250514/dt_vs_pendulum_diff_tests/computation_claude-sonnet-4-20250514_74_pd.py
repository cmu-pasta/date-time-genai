
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_next_new_moon(given_date: pendulum.DateTime) -> pendulum.DateTime:
    # Reference new moon date: January 6, 2000 at 18:14 UTC
    reference_new_moon = pendulum.parse("2000-01-06T18:14:00Z")
    
    # Average lunar cycle length in days
    lunar_cycle_days = 29.53059
    
    # Calculate days since reference new moon
    days_since_reference = given_date.diff(reference_new_moon).in_days()
    
    # Calculate number of complete cycles since reference
    cycles_passed = int(days_since_reference / lunar_cycle_days)
    
    # Calculate the most recent new moon before or at the given date
    recent_new_moon_days = cycles_passed * lunar_cycle_days
    recent_new_moon = reference_new_moon.add(days=recent_new_moon_days)
    
    # If the recent new moon is before the given date, get the next one
    if recent_new_moon < given_date:
        next_new_moon = recent_new_moon.add(days=lunar_cycle_days)
    else:
        next_new_moon = recent_new_moon
    
    return next_new_moon

# Entry point: find_next_new_moon(given_date: pendulum.DateTime) -> pendulum.DateTime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_74_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_new_moon(given_date):
    result = find_next_new_moon(given_date)
    formatted_result = format_value_pd(result, given_date)
    log_file.write(formatted_result + "\n")
