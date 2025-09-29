
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_next_valentines_day(given_date: pendulum.DateTime) -> pendulum.DateTime:
    # Step 1: Get the year from the given date
    year = given_date.year
    
    # Step 2: Construct Valentine's Day for the current year (Feb 14th)
    # We set time to midnight (00:00:00) to ensure consistent comparison if given_date has time components.
    valentines_this_year = pendulum.datetime(year, 2, 14, tz=given_date.timezone)
    
    # Step 3: Check if Valentine's Day this year has already passed or is today
    if valentines_this_year <= given_date:
        # If it has passed or is today, the next Valentine's Day is next year
        next_valentines_day = pendulum.datetime(year + 1, 2, 14, tz=given_date.timezone)
    else:
        # Otherwise, Valentine's Day this year is the next one
        next_valentines_day = valentines_this_year
        
    # Step 4: Return the result
    return next_valentines_day

# Entry point: find_next_valentines_day(given_date: pendulum.DateTime) -> pendulum.DateTime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_56_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_valentines_day(given_date):
    result = find_next_valentines_day(given_date)
    formatted_result = format_value_pd(result, given_date)
    log_file.write(formatted_result + "\n")
