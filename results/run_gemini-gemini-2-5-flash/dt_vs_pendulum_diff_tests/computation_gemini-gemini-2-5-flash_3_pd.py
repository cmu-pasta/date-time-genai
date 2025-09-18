
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_next_leap_year(dt: pendulum.DateTime) -> int:
    # Step 1: Get the year from the input date
    year = dt.year

    # Step 2: Determine the starting year for the search
    # If the current year is a leap year and the date is on or before Feb 29th of that year,
    # then the current year is the next leap year.
    # Otherwise, we need to search from the next year.
    if pendulum.is_leap(year):
        # Create a pendulum.DateTime for February 29th of the current year
        # Note: If the year is not a leap year, pendulum.datetime(year, 2, 29) would raise an error.
        # But we only enter this block if pendulum.is_leap(year) is True, so Feb 29th exists.
        feb_29_current_year = pendulum.datetime(year, 2, 29, tz=dt.timezone)
        
        if dt <= feb_29_current_year:
            # The current year is a leap year and the date has not passed Feb 29th,
            # so the current year is the next leap year.
            return year
        else:
            # The current year is a leap year, but the date has passed Feb 29th,
            # so we need to find the next one starting from year + 1.
            start_year = year + 1
    else:
        # The current year is not a leap year, so we start searching from the next year.
        start_year = year + 1
    
    # Step 3: Iterate from start_year to find the next leap year
    current_search_year = start_year
    while True:
        if pendulum.is_leap(current_search_year):
            return current_search_year
        current_search_year += 1

# Entry point: find_next_leap_year(dt: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_3_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_leap_year(dt):
    result = find_next_leap_year(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
