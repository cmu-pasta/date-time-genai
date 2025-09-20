
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_business_days_after(start_date: pendulum.Date, n: int) -> pendulum.Date:
    # Start with the given date
    current_date = start_date
    business_days_counted = 0
    
    # Keep adding days until we count N business days
    while business_days_counted < n:
        # Move to the next day
        current_date = current_date.add(days=1)
        
        # Check if current day is a business day (Monday=1 to Friday=5)
        if current_date.weekday() <= 5:
            business_days_counted += 1
    
    return current_date

# Entry point: find_business_days_after(start_date: pendulum.Date, n: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_14_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy())
def test_find_business_days_after(start_date, n):
    result = find_business_days_after(start_date, n)
    formatted_result = format_value_pd(result, start_date, n)
    log_file.write(formatted_result + "\n")
