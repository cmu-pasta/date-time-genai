
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def columbus_day(year: int) -> pendulum.Date:
    """
    Compute Columbus Day (second Monday of October) for the given year.
    
    Args:
        year (int): The target year.
        
    Returns:
        pendulum.Date: The date of Columbus Day for the given year.
    """
    # Step 1: October 1st of the given year
    oct_first = pendulum.date(year, 10, 1)
    
    # Step 2: Weekday of Oct 1st (0=Monday ... 6=Sunday)
    dow = oct_first.day_of_week
    
    # Step 3: Day of month for the first Monday in October
    # If Oct 1 is Monday (dow=0), offset is 0; otherwise days until next Monday
    days_until_monday = (7 - dow) % 7
    first_monday = oct_first.add(days=days_until_monday)
    
    # Step 4: Second Monday = first Monday + 7 days
    second_monday = first_monday.add(days=7)
    
    # Step 5: Return the pendulum.Date for Columbus Day
    return second_monday

# Entry point: columbus_day(year: int) -> pendulum.Date

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_77txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_columbus_day(year):
    result = columbus_day(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
