
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_previous_friday(date: pendulum.Date) -> pendulum.Date:
    # Step 1: Get the day of the week (Monday=1, Tuesday=2, ..., Sunday=7)
    current_day = date.day_of_week
    
    # Step 2: Calculate how many days to subtract to get to the previous Friday
    if current_day <= 5:  # Monday to Friday
        days_to_subtract = current_day + 2
    else:  # Saturday or Sunday
        days_to_subtract = current_day - 5
    
    # Step 3: Subtract the calculated days to get the previous Friday
    previous_friday = date.subtract(days=days_to_subtract)
    
    # Step 4: Return the result as a pendulum.Date
    return previous_friday

# Entry point: find_previous_friday(date: pendulum.Date) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_20_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_find_previous_friday(date):
    result = find_previous_friday(date)
    formatted_result = format_value_pd(result, date)
    log_file.write(formatted_result + "\n")
