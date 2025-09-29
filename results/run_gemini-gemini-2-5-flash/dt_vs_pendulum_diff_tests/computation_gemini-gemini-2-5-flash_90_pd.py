
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_lunar_age(date: pendulum.DateTime) -> int:
    # Step 1: Define a reference new moon date (e.g., Jan 6, 2000, 18:14 UTC was a New Moon)
    # Using a slightly simplified base date for integer day calculation.
    # The actual precise average synodic month length is 29.530588 days.
    # We will use 29.530588 for the modulo operation.
    base_new_moon = pendulum.datetime(2000, 1, 6, tz='UTC')

    # Step 2: Ensure the input date is in UTC for consistent calculation
    # and convert to start of day for simpler day count if it's not already at midnight.
    # However, for accurate lunar age, we should consider time.
    # Let's keep the time component of the input date.
    date_utc = date.in_timezone('UTC')

    # Step 3: Calculate the total number of days between the base new moon and the target date
    # pendulum.Duration.in_days() gives total full days.
    # For more precision when dealing with moon phases, we calculate total hours and divide by 24.
    duration = date_utc - base_new_moon
    total_days_float = duration.total_seconds() / (24 * 3600)

    # Step 4: Define the average length of a synodic month (new moon to new moon)
    synodic_month_length = 29.530588

    # Step 5: Calculate the lunar age using the modulo operator
    # The result will be in the range [0, synodic_month_length)
    lunar_age_float = total_days_float % synodic_month_length

    # Ensure the result is positive, as Python's % can yield negative for negative dividends
    if lunar_age_float < 0:
        lunar_age_float += synodic_month_length

    # Step 6: Return the result as an integer (days since new moon)
    return int(round(lunar_age_float))

# Entry point: calculate_lunar_age(date: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_90_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_lunar_age(date):
    result = calculate_lunar_age(date)
    formatted_result = format_value_pd(result, date)
    log_file.write(formatted_result + "\n")
