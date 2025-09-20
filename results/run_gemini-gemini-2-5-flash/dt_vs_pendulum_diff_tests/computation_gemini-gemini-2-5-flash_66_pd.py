
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_trading_days_in_year(year: int) -> int:
    # Step 1: Establish the start and end dates for the given year
    start_of_year = pendulum.datetime(year, 1, 1)
    end_of_year = pendulum.datetime(year, 12, 31)
    
    # Step 2: Initialize a counter for trading days
    trading_days_count = 0
    
    # Step 3: Iterate through each day in the year
    # A trading day is considered any weekday (Monday to Friday).
    # This definition does not account for public holidays as pendulum
    # does not inherently provide holiday calendars.
    for day in pendulum.period(start_of_year, end_of_year):
        # Step 4: Check if the current day is a weekday
        if day.is_weekday():
            trading_days_count += 1
            
    # Step 5: Return the total count of trading days
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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_66_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_calculate_trading_days_in_year(year):
    result = calculate_trading_days_in_year(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
