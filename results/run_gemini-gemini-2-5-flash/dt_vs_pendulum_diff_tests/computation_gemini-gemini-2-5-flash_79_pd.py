
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def get_buddhist_year(gregorian_date: pendulum.DateTime) -> int:
    # Step 1: Extract the Gregorian year from the input date.
    gregorian_year = gregorian_date.year
    
    # Step 2: Add 543 to the Gregorian year to get the Buddhist calendar year.
    # The Buddhist Era (B.E.) is 543 years ahead of the Common Era (C.E.).
    buddhist_year = gregorian_year + 543
    
    # Step 3: Return the Buddhist year as an integer.
    return buddhist_year

# Entry point: get_buddhist_year(gregorian_date: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_79_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_buddhist_year(gregorian_date):
    result = get_buddhist_year(gregorian_date)
    formatted_result = format_value_pd(result, gregorian_date)
    log_file.write(formatted_result + "\n")
