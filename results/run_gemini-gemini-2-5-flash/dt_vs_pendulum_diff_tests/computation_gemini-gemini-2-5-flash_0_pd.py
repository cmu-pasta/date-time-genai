
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_business_days(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int:
    # Step 1 & 2: Determine the start and end dates to ensure iteration goes forward
    start_date = dt1.start_of('day') if dt1 <= dt2 else dt2.start_of('day')
    end_date = dt2.start_of('day') if dt1 <= dt2 else dt1.start_of('day')

    # Step 3: Initialize a counter for business days
    business_days_count = 0

    # Step 4 & 5: Iterate through each day from start_date to end_date (inclusive)
    current_date = start_date
    while current_date <= end_date:
        # Step 6: Check if the current day is a weekday (Monday to Friday)
        # Pendulum's day_of_week: 1 (Monday) ... 7 (Sunday)
        if 1 <= current_date.day_of_week <= 5:
            business_days_count += 1 # Step 7: Increment if it's a business day
        
        # Move to the next day
        current_date = current_date.add(days=1)
        
    # Step 8: Return the total count of business days
    return business_days_count

# Entry point: calculate_business_days(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_0_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_business_days(dt1, dt2):
    result = calculate_business_days(dt1, dt2)
    formatted_result = format_value_pd(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
