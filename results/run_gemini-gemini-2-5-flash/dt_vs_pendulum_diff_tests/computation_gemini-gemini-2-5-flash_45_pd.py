
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_business_days_remaining_in_month(given_date: pendulum.DateTime) -> int:
    # Step 1: Get the last day of the month for the given date.
    last_day_of_month = given_date.end_of('month')
    
    # Step 2: Initialize a counter for business days.
    business_days_remaining = 0
    
    # Step 3: Start iterating from the day after the given_date.
    # We use add(days=1) to get the next day.
    current_day = given_date.add(days=1)
    
    # Step 4: Loop through each day until the end of the month.
    while current_day <= last_day_of_month:
        # Step 5: Check if the current_day is a weekday (Monday to Friday).
        if current_day.is_weekday():
            business_days_remaining += 1
        
        # Step 6: Move to the next day.
        current_day = current_day.add(days=1)
        
    # Step 7: Return the total number of business days remaining.
    return business_days_remaining

# Entry point: calculate_business_days_remaining_in_month(given_date: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_45_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_business_days_remaining_in_month(given_date):
    result = calculate_business_days_remaining_in_month(given_date)
    formatted_result = format_value_pd(result, given_date)
    log_file.write(formatted_result + "\n")
