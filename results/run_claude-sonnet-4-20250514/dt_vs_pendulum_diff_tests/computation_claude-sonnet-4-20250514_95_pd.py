
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_next_solar_eclipse(latitude: float, longitude: float, start_date: pendulum.DateTime) -> pendulum.DateTime:
    # Simplified approximation using the Saros cycle (18 years, 11 days, 8 hours)
    # This is not accurate for real-world use and serves as a basic approximation
    
    # Known eclipse reference point (approximate)
    reference_eclipse = pendulum.datetime(2024, 4, 8, 18, 0, 0, tz='UTC')
    
    # Saros cycle duration in days (approximately 6585.32 days)
    saros_days = 6585
    saros_hours = 8
    
    # Calculate how many Saros cycles have passed since reference
    days_since_reference = start_date.diff(reference_eclipse).in_days()
    
    if days_since_reference < 0:
        # Start date is before reference, use the reference eclipse
        next_eclipse = reference_eclipse
    else:
        # Calculate next eclipse after start_date
        cycles_passed = days_since_reference // saros_days
        next_cycle = cycles_passed + 1
        
        # Calculate next eclipse date
        next_eclipse = reference_eclipse.add(days=next_cycle * saros_days, hours=next_cycle * saros_hours)
    
    # Ensure we return a date after the start_date
    while next_eclipse <= start_date:
        next_eclipse = next_eclipse.add(days=saros_days, hours=saros_hours)
    
    return next_eclipse

# Entry point: find_next_solar_eclipse(latitude: float, longitude: float, start_date: pendulum.DateTime) -> pendulum.DateTime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_95_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(float_strategy(), float_strategy(), datetime_strategy())
def test_find_next_solar_eclipse(latitude, longitude, start_date):
    result = find_next_solar_eclipse(latitude, longitude, start_date)
    formatted_result = format_value_pd(result, latitude, longitude, start_date)
    log_file.write(formatted_result + "\n")
