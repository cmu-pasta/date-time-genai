
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def get_thai_buddhist_date(gregorian_date: pendulum.DateTime) -> pendulum.DateTime:
    # Step 1: Extract the Gregorian year from the input date.
    gregorian_year = gregorian_date.year
    
    # Step 2: Calculate the Thai Buddhist year by adding 543 to the Gregorian year.
    thai_buddhist_year = gregorian_year + 543
    
    # Step 3: Construct a new pendulum.DateTime object with the Thai Buddhist year,
    # keeping the month, day, time components, and timezone from the original Gregorian date.
    thai_buddhist_date = pendulum.datetime(
        thai_buddhist_year,
        gregorian_date.month,
        gregorian_date.day,
        gregorian_date.hour,
        gregorian_date.minute,
        gregorian_date.second,
        gregorian_date.microsecond,
        tz=gregorian_date.tz
    )
    
    # Step 4: Return the newly created Thai Buddhist calendar date.
    return thai_buddhist_date

# Entry point: get_thai_buddhist_date(gregorian_date: pendulum.DateTime) -> pendulum.DateTime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_97_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_thai_buddhist_date(gregorian_date):
    result = get_thai_buddhist_date(gregorian_date)
    formatted_result = format_value_pd(result, gregorian_date)
    log_file.write(formatted_result + "\n")
