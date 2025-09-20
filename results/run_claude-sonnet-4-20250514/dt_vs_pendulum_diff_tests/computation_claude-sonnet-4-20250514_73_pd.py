
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def is_within_business_hours(dt: pendulum.DateTime) -> bool:
    # Step 1: Extract the time portion from the datetime
    time_part = dt.time()
    
    # Step 2: Define business hours (9 AM to 5 PM)
    business_start = pendulum.time(9, 0, 0)  # 9:00 AM
    business_end = pendulum.time(17, 0, 0)   # 5:00 PM (17:00 in 24-hour format)
    
    # Step 3: Check if the time falls within business hours
    # Business hours are from 9 AM (inclusive) to 5 PM (exclusive)
    return business_start <= time_part < business_end

# Entry point: is_within_business_hours(dt: pendulum.DateTime) -> bool

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_73_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_is_within_business_hours(dt):
    result = is_within_business_hours(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
