
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def days_until_next_birthday(birth_date: pendulum.Date) -> int:
    # Step 1: Get today's date (as pendulum.Date)
    today = pendulum.today()

    # Step 2: Attempt to create this year's birthday; handle Feb 29 on non-leap years by using Feb 28
    year = today.year
    try:
        this_year_birthday = pendulum.date(year, birth_date.month, birth_date.day)
    except ValueError:
        # Fallback for invalid dates like Feb 29 on non-leap years: use Feb 28
        this_year_birthday = pendulum.date(year, 2, 28)

    # Step 3: Decide whether the next birthday is this year or next year
    if this_year_birthday < today:
        year += 1
        try:
            next_birthday = pendulum.date(year, birth_date.month, birth_date.day)
        except ValueError:
            next_birthday = pendulum.date(year, 2, 28)
    else:
        next_birthday = this_year_birthday

    # Step 4: Compute the difference in days (as a positive integer)
    days_until = today.diff(next_birthday).in_days()

    # Step 5: Return the integer number of days
    return days_until

# Entry point: days_until_next_birthday(birth_date: pendulum.Date) -> int

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_21_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_days_until_next_birthday(birth_date):
    result = days_until_next_birthday(birth_date)
    formatted_result = format_value_pd(result, birth_date)
    log_file.write(formatted_result + "\n")
