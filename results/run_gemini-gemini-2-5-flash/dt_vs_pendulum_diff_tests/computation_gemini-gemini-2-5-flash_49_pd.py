
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def count_february_sundays(year: int) -> int:
    # Step 3: Initialize a counter for Sundays
    sunday_count = 0

    # Step 4: Determine the first day of February
    # pendulum automatically handles leap years for the last day of February
    current_date = pendulum.date(year, 2, 1)

    # Step 5: Loop through February
    # Continue as long as the current_date is still in February of the given year
    while current_date.month == 2:
        # Step 6: Check if the current day is a Sunday (day_of_week 7)
        if current_date.day_of_week == pendulum.SUNDAY: # pendulum.SUNDAY is a constant for 7
            # Step 7: Increment the counter if it's a Sunday
            sunday_count += 1
        
        # Step 8: Advance to the next day
        current_date = current_date.add(days=1)
    
    # Step 9: Return the total count of Sundays in February
    return sunday_count

# Entry point: count_february_sundays(year: int) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_49_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_count_february_sundays(year):
    result = count_february_sundays(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
