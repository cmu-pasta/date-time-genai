
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_trading_days_in_year(year: int) -> int:
    # Step 1: Create the start and end dates for the given year
    start_date = pendulum.date(year, 1, 1)
    end_date = pendulum.date(year, 12, 31)
    
    # Step 2: Initialize counter for trading days
    trading_days_count = 0
    
    # Step 3: Iterate through all days in the year
    current_date = start_date
    while current_date <= end_date:
        # Step 4: Check if current day is a weekday (Monday=1 to Friday=5)
        if current_date.day_of_week >= 1 and current_date.day_of_week <= 5:
            trading_days_count += 1
        
        # Move to next day
        current_date = current_date.add(days=1)
    
    # Step 5: Return the total count
    return trading_days_count

# Entry point: calculate_trading_days_in_year(year: int) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_66_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_calculate_trading_days_in_year(year):
    result = calculate_trading_days_in_year(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
