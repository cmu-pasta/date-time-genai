
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def thanksgiving_date(year: int) -> pendulum.Date:
    """
    Compute the date of Thanksgiving (fourth Thursday of November) for a given year.
    Returns a pendulum.Date.
    """
    # Step 1: November 1st of the given year
    nov_first: pendulum.Date = pendulum.date(year, 11, 1)
    
    # Step 2: Compute offset to the first Thursday (Thursday = 4 with Monday=0)
    thursday_dow = 4
    offset = (thursday_dow - nov_first.day_of_week) % 7
    
    # Step 3: First Thursday in November
    first_thursday: pendulum.Date = nov_first.add(days=offset)
    
    # Step 4: Fourth Thursday = first Thursday + 3 weeks (21 days)
    fourth_thursday: pendulum.Date = first_thursday.add(days=21)
    
    return fourth_thursday

# Entry point: thanksgiving_date(year: int) -> pendulum.Date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_29txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_thanksgiving_date(year):
    result = thanksgiving_date(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
