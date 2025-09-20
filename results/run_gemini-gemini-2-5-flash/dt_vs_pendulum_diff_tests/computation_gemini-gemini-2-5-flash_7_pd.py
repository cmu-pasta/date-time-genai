
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def is_leap_year(year: int) -> bool:
    # Step 1: Create a pendulum.Date object for the given year.
    # We can use any date within that year, for simplicity, we pick January 1st.
    date_in_year = pendulum.date(year, 1, 1)
    
    # Step 2: Access the is_leap_year property of the pendulum.Date object.
    # This property directly returns a boolean indicating if the year is a leap year.
    is_leap = date_in_year.is_leap_year
    
    # Step 3: Return the boolean result.
    return is_leap

# Entry point: is_leap_year(year: int) -> bool

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_7_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_is_leap_year(year):
    result = is_leap_year(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
