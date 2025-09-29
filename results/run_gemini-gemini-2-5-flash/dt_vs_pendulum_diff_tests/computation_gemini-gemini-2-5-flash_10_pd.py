
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def convert_date_to_julian_day_number(dt: pendulum.DateTime) -> int:
    # Step 1: Extract year, month, and day from the pendulum.DateTime object
    year = dt.year
    month = dt.month
    day = dt.day

    # Step 2: Apply the Julian Day Number calculation formula (for Gregorian calendar)
    # The formula below is a common algorithm for calculating the Julian Day Number.
    # It accounts for the changes between the Julian and Gregorian calendars.

    if month <= 2:
        year -= 1
        month += 12

    a = year // 100
    b = 2 - a + (a // 4)
    
    # Julian Day Number calculation
    # The term -1524.5 is usually for Julian Date, which includes fractional time.
    # For Julian Day Number (integer part), the formula is often adjusted slightly
    # to ensure the day starts at 00:00 UTC for the given date.
    # We will use a robust integer formula that directly yields JDN.
    
    # This formula calculates JDN at noon UTC for the given date.
    # To get the JDN for the start of the day (00:00 UTC), some sources use floor(JD + 0.5).
    # The problem asks for "Julian day number", which usually refers to the integer value
    # representing the day, starting at noon. Let's use the common integer calculation.
    
    julian_day_number = (
        365 * year
        + (year // 4)
        - (year // 100)
        + (year // 400)
        + ((153 * month + 2) // 5)
        + day
        + 1721119 # This constant aligns with JDN 0 = Jan 1, 4713 BC (Julian) at noon.
        + b # This term corrects for the Gregorian calendar reform.
    )

    # Note: Some definitions of JDN might vary by a small offset (e.g., 0.5 or 1)
    # depending on whether the day starts at midnight or noon, and the exact calendar origin.
    # This implementation provides the standard JDN where 0 is Jan 1, 4713 BC, noon UTC.

    # Step 3: Return the result as an integer
    return julian_day_number

# Entry point: convert_date_to_julian_day_number(dt: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_10_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_date_to_julian_day_number(dt):
    result = convert_date_to_julian_day_number(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
