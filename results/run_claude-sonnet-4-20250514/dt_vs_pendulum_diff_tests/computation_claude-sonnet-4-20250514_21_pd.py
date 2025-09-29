
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def days_until_next_birthday(birth_date: pendulum.Date) -> int:
    today = pendulum.today()
    
    # Calculate this year's birthday
    current_year = today.year
    try:
        this_year_birthday = pendulum.date(current_year, birth_date.month, birth_date.day)
    except ValueError:
        # Handle leap year case (Feb 29 on non-leap year)
        this_year_birthday = pendulum.date(current_year, birth_date.month, 28)
    
    if this_year_birthday > today:
        # Birthday hasn't passed this year
        next_birthday = this_year_birthday
    else:
        # Birthday has passed or is today, next one is next year
        next_year = current_year + 1
        try:
            next_birthday = pendulum.date(next_year, birth_date.month, birth_date.day)
        except ValueError:
            # Handle leap year case
            next_birthday = pendulum.date(next_year, birth_date.month, 28)
    
    # Calculate difference in days
    difference = next_birthday.diff(today).in_days()
    
    return difference

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_21_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_days_until_next_birthday(birth_date):
    result = days_until_next_birthday(birth_date)
    formatted_result = format_value_pd(result, birth_date)
    log_file.write(formatted_result + "\n")
