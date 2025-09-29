
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_nth_weekday_of_month(
    month_start_date: pendulum.DateTime, 
    weekday: int, 
    n: int
) -> pendulum.DateTime:
    """
    Finds the nth occurrence of a specific weekday in a given month.

    Args:
        month_start_date: A pendulum.DateTime object representing any day in the target month.
                          Only its year and month components will be used.
        weekday: An integer representing the target weekday (e.g., pendulum.MONDAY).
        n: The desired occurrence number (e.g., 1 for the first, 2 for the second).

    Returns:
        A pendulum.DateTime object representing the nth occurrence of the weekday
        in the month. If the nth occurrence does not exist, it returns
        pendulum.datetime(1, 1, 1) as an indicator.
    """
    if n <= 0:
        # Invalid occurrence number, return the indicator date
        return pendulum.datetime(1, 1, 1)

    # Normalize month_start_date to the first day of the month
    current_day = month_start_date.start_of("month")
    
    found_count = 0
    
    # Iterate through the days of the month
    while current_day.month == month_start_date.month:
        if current_day.weekday() == weekday:
            found_count += 1
            if found_count == n:
                return current_day
        
        # Move to the next day
        current_day = current_day.add(days=1)
        
    # If the loop finishes, the nth occurrence was not found
    return pendulum.datetime(1, 1, 1)

# Entry point: find_nth_weekday_of_month(month_start_date: pendulum.DateTime, weekday: int, n: int) -> pendulum.DateTime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_17_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_nth_weekday_of_month(month_start_date, weekday, n):
    result = find_nth_weekday_of_month(month_start_date, weekday, n)
    formatted_result = format_value_pd(result, month_start_date, weekday, n)
    log_file.write(formatted_result + "\n")
