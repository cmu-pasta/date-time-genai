
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_nth_weekday_in_month(date: pendulum.Date, weekday: int, occurrence: int) -> pendulum.Date:
    # Step 1: Get the first day of the month
    first_day = date.start_of('month')
    
    # Step 2: Initialize variables
    current_date = first_day
    count = 0
    
    # Step 3: Iterate through the month to find the nth occurrence
    while current_date.month == first_day.month:
        # Check if current day matches the target weekday
        if current_date.weekday() == weekday:
            count += 1
            if count == occurrence:
                return current_date
        
        # Move to the next day
        current_date = current_date.add(days=1)
    
    # If we exit the loop without finding the nth occurrence, it doesn't exist
    # Return None or raise an exception - but since we can only return pendulum types,
    # we'll return the last day of the month as a fallback
    return date.end_of('month')

# Entry point: find_nth_weekday_in_month(date: pendulum.Date, weekday: int, occurrence: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_17_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_nth_weekday_in_month(date, weekday, occurrence):
    result = find_nth_weekday_in_month(date, weekday, occurrence)
    formatted_result = format_value_pd(result, date, weekday, occurrence)
    log_file.write(formatted_result + "\n")
