
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_next_full_moon(given_date: pendulum.DateTime) -> pendulum.DateTime:
    # Reference full moon date: January 6, 2023 (known full moon)
    reference_full_moon = pendulum.datetime(2023, 1, 6, 18, 8, 0, tz='UTC')
    
    # Average lunar cycle length in days (synodic month)
    lunar_cycle_days = 29.530588853
    
    # Calculate the difference in days from reference to given date
    days_diff = given_date.diff(reference_full_moon).total_seconds() / 86400
    
    # Calculate how many complete cycles have passed
    cycles_passed = days_diff / lunar_cycle_days
    
    # Find the next full moon
    if cycles_passed < 0:
        # Given date is before reference, find the previous full moon first
        next_cycle = int(cycles_passed) 
    else:
        # Given date is after reference, find the next full moon
        next_cycle = int(cycles_passed) + 1
    
    # Calculate the next full moon date
    next_full_moon_days = next_cycle * lunar_cycle_days
    next_full_moon = reference_full_moon.add(days=next_full_moon_days)
    
    # If the calculated full moon is not after the given date, add one more cycle
    if next_full_moon <= given_date:
        next_full_moon = next_full_moon.add(days=lunar_cycle_days)
    
    return next_full_moon

# Entry point: find_next_full_moon(given_date: pendulum.DateTime) -> pendulum.DateTime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_23_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_full_moon(given_date):
    result = find_next_full_moon(given_date)
    formatted_result = format_value_pd(result, given_date)
    log_file.write(formatted_result + "\n")
