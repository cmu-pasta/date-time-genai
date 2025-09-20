
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_weekends_between_dates(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int:
    # Step 1: Determine the start and end dates for iteration
    start_date = min(dt1, dt2).start_of('day') # Ensure we start from the beginning of the day
    end_date = max(dt1, dt2).start_of('day')   # Ensure we end at the beginning of the day for consistent daily checks

    # Step 2: Initialize a counter for weekend days
    weekend_count = 0
    
    # Step 3: Iterate through each day between start_date and end_date (inclusive)
    current_date = start_date
    while current_date <= end_date:
        # Step 4: Check if the current day is a Saturday (6) or Sunday (7)
        # Pendulum's day_of_week follows ISO 8601 (Monday=1, Sunday=7)
        if current_date.day_of_week == pendulum.SATURDAY or current_date.day_of_week == pendulum.SUNDAY:
            weekend_count += 1
        
        # Step 5: Move to the next day
        current_date = current_date.add(days=1)
        
    # Step 6: Return the total number of weekend days
    return weekend_count

# Entry point: calculate_weekends_between_dates(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_15_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_weekends_between_dates(dt1, dt2):
    result = calculate_weekends_between_dates(dt1, dt2)
    formatted_result = format_value_pd(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
