
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_age_ymd(start: pendulum.Date, end: pendulum.Date) -> pendulum.Duration:
    """
    Calculate the age as a compound of years, months, and days between two dates.

    Inputs:
      - start: pendulum.Date or pendulum.DateTime
      - end: pendulum.Date or pendulum.DateTime

    Returns:
      - pendulum.Duration with years, months, and days components representing the age.
    """
    # Normalize to pendulum.Date (ignore time components if DateTime is provided)
    if isinstance(start, pendulum.DateTime):
        start_date = start.date()
    elif isinstance(start, pendulum.Date):
        start_date = start
    else:
        raise TypeError("start must be a pendulum.Date or pendulum.DateTime")

    if isinstance(end, pendulum.DateTime):
        end_date = end.date()
    elif isinstance(end, pendulum.Date):
        end_date = end
    else:
        raise TypeError("end must be a pendulum.Date or pendulum.DateTime")

    # Ensure chronological order
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    # Build a period to extract calendar-aware components
    period = pendulum.period(start_date, end_date)

    years = period.years
    months = period.months
    days = period.days

    # Return as a pendulum.Duration preserving Y/M/D components
    return pendulum.duration(years=years, months=months, days=days)

# Entry point: calculate_age_ymd(start: pendulum.Date, end: pendulum.Date) -> pendulum.Duration

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_6txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_age_ymd(start, end):
    result = calculate_age_ymd(start, end)
    formatted_result = format_value_pd(result, start, end)
    log_file.write(formatted_result + "\n")
