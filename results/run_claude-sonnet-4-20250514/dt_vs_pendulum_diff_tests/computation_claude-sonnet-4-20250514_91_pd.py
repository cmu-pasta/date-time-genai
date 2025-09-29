
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def gregorian_to_indian_national_calendar(gregorian_date: pendulum.Date) -> int:
    # The Indian National Calendar (Saka calendar) starts from 78 CE
    saka_era_offset = 78
    
    # Determine the Saka new year date for the current Gregorian year
    # Saka new year typically falls on March 22 (March 21 in leap years)
    current_year = gregorian_date.year
    is_leap_year = current_year % 4 == 0 and (current_year % 100 != 0 or current_year % 400 == 0)
    
    if is_leap_year:
        saka_new_year = pendulum.date(current_year, 3, 21)
    else:
        saka_new_year = pendulum.date(current_year, 3, 22)
    
    # Calculate the Saka year
    if gregorian_date >= saka_new_year:
        # If the date is after or on the Saka new year, use current Gregorian year
        saka_year = current_year - saka_era_offset
    else:
        # If the date is before the Saka new year, use previous Gregorian year
        saka_year = current_year - saka_era_offset - 1
    
    return saka_year

# Entry point: gregorian_to_indian_national_calendar(gregorian_date: pendulum.Date) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_91_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_indian_national_calendar(gregorian_date):
    result = gregorian_to_indian_national_calendar(gregorian_date)
    formatted_result = format_value_pd(result, gregorian_date)
    log_file.write(formatted_result + "\n")
