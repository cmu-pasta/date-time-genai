
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_working_hours_between(start_dt: pendulum.DateTime, end_dt: pendulum.DateTime) -> float:
    # Step 1: Ensure start_dt is always before end_dt
    if start_dt > end_dt:
        start_dt, end_dt = end_dt, start_dt

    total_working_hours = 0.0

    # Define standard daily working hours (e.g., 9 AM to 5 PM)
    WORKING_START_HOUR = 9
    WORKING_END_HOUR = 17

    current_day = start_dt.start_of('day')

    # Step 2: Iterate day by day from start_dt to end_dt
    while current_day <= end_dt.start_of('day'):
        # Step 3: Check if the current day is a weekday (Monday to Friday)
        # Pendulum's is_weekend() returns True for Saturday and Sunday
        if not current_day.is_weekend():
            # Define the working start and end for the current day
            daily_working_start = current_day.set(hour=WORKING_START_HOUR)
            daily_working_end = current_day.set(hour=WORKING_END_HOUR)

            # Determine the effective start and end for this specific day, considering the overall start_dt and end_dt
            effective_start_for_day = max(start_dt, daily_working_start)
            effective_end_for_day = min(end_dt, daily_working_end)

            # Step 4: Calculate the overlap between the effective range and the daily working hours
            if effective_start_for_day < effective_end_for_day:
                duration = effective_end_for_day - effective_start_for_day
                total_working_hours += duration.in_hours()
        
        # Move to the next day
        current_day = current_day.add(days=1).start_of('day')

    # Ensure the calculation doesn't go beyond end_dt if end_dt is not exactly at the start of a day
    # The loop condition `current_day <= end_dt.start_of('day')` handles this by including the day of end_dt.
    # The `min(end_dt, daily_working_end)` in `effective_end_for_day` makes sure we don't count past end_dt's time.

    return total_working_hours

# Entry point: calculate_working_hours_between(start_dt: pendulum.DateTime, end_dt: pendulum.DateTime) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_24_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_working_hours_between(start_dt, end_dt):
    result = calculate_working_hours_between(start_dt, end_dt)
    formatted_result = format_value_pd(result, start_dt, end_dt)
    log_file.write(formatted_result + "\n")
