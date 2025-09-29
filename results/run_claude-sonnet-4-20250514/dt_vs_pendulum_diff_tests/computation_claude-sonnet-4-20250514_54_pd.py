
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_year_percentage(date: pendulum.DateTime) -> float:
    # Get the start of the year (January 1st at 00:00:00)
    year_start = date.start_of('year')
    
    # Get the start of the next year to calculate total year duration
    next_year_start = year_start.add(years=1)
    
    # Calculate total seconds passed from start of year to given date
    seconds_passed = date.diff(year_start).total_seconds()
    
    # Calculate total seconds in the year
    total_seconds_in_year = next_year_start.diff(year_start).total_seconds()
    
    # Calculate percentage
    percentage = (seconds_passed / total_seconds_in_year) * 100
    
    return percentage

# Entry point: calculate_year_percentage(date: pendulum.DateTime) -> float

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_54_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_year_percentage(date):
    result = calculate_year_percentage(date)
    formatted_result = format_value_pd(result, date)
    log_file.write(formatted_result + "\n")
