
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_next_valentines_day(given_date: pendulum.DateTime) -> pendulum.DateTime:
    # Get the current year from the given date
    current_year = given_date.year
    
    # Create Valentine's Day for the current year (February 14)
    valentines_this_year = pendulum.datetime(current_year, 2, 14, tz=given_date.timezone)
    
    # If the given date is before this year's Valentine's Day, return this year's Valentine's Day
    if given_date < valentines_this_year:
        return valentines_this_year
    else:
        # Otherwise, return next year's Valentine's Day
        valentines_next_year = pendulum.datetime(current_year + 1, 2, 14, tz=given_date.timezone)
        return valentines_next_year

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_56_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_valentines_day(given_date):
    result = find_next_valentines_day(given_date)
    formatted_result = format_value_pd(result, given_date)
    log_file.write(formatted_result + "\n")
