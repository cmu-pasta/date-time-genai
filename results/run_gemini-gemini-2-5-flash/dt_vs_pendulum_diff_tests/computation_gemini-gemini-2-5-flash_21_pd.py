
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_days_until_next_birthday(birth_date: pendulum.Date) -> int:
    # Step 1: Get the current date
    today = pendulum.today()

    # Step 2 & 3: Determine the next birthday's year and handle Feb 29th
    current_year = today.year
    birth_month = birth_date.month
    birth_day = birth_date.day

    next_birthday_year = current_year

    # Try to construct the birthday in the current year
    # Handle Feb 29th specifically
    if birth_month == 2 and birth_day == 29:
        # Keep advancing the year until we find a leap year
        while not pendulum.date(next_birthday_year, 1, 1).is_leap():
            next_birthday_year += 1
        potential_next_birthday = pendulum.date(next_birthday_year, birth_month, birth_day)
    else:
        # For non-Feb 29th birthdays, simply use the current year
        potential_next_birthday = pendulum.date(next_birthday_year, birth_month, birth_day)

    # If the potential birthday for the current (or next valid leap) year has already passed
    if potential_next_birthday < today:
        next_birthday_year += 1
        # If the original birth date was Feb 29, ensure the new year is also a leap year
        if birth_month == 2 and birth_day == 29:
            while not pendulum.date(next_birthday_year, 1, 1).is_leap():
                next_birthday_year += 1
        next_birthday_date = pendulum.date(next_birthday_year, birth_month, birth_day)
    else:
        next_birthday_date = potential_next_birthday

    # Step 5: Calculate the difference between the next birthday and today
    difference_duration = next_birthday_date - today

    # Step 6: Extract the number of days
    return difference_duration.in_days()

# Entry point: calculate_days_until_next_birthday(birth_date: pendulum.Date) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_21_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_calculate_days_until_next_birthday(birth_date):
    result = calculate_days_until_next_birthday(birth_date)
    formatted_result = format_value_pd(result, birth_date)
    log_file.write(formatted_result + "\n")
