
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_thanksgiving_date(year: int) -> pendulum.Date:
    # Step 1: Create November 1st for the given year
    november_first = pendulum.date(year, 11, 1)
    
    # Step 2: Find what day of the week November 1st is (1=Monday, 7=Sunday)
    day_of_week = november_first.day_of_week
    
    # Step 3: Calculate days to add to get to the first Thursday (Thursday = 4)
    # If November 1st is Thursday (4), we need 0 days
    # If November 1st is Friday (5), we need 6 days to get to next Thursday
    # Formula: (4 - day_of_week) % 7
    days_to_first_thursday = (4 - day_of_week) % 7
    
    # Step 4: Get the first Thursday of November
    first_thursday = november_first.add(days=days_to_first_thursday)
    
    # Step 5: Add 21 days (3 weeks) to get the fourth Thursday (Thanksgiving)
    thanksgiving = first_thursday.add(days=21)
    
    return thanksgiving

# Entry point: find_thanksgiving_date(year: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_29_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_thanksgiving_date(year):
    result = find_thanksgiving_date(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
