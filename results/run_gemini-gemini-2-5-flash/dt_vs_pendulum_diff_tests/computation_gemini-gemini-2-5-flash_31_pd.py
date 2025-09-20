
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def get_fiscal_year_april_start(date: pendulum.DateTime) -> int:
    # Fiscal year starts in April (month 4)
    fiscal_year_start_month = 4

    # If the month of the given date is April or later, the fiscal year is the current calendar year.
    # Otherwise (Jan, Feb, Mar), the fiscal year is the previous calendar year.
    if date.month >= fiscal_year_start_month:
        fiscal_year = date.year
    else:
        fiscal_year = date.year - 1
        
    return fiscal_year

# Entry point: get_fiscal_year_april_start(date: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_31_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_fiscal_year_april_start(date):
    result = get_fiscal_year_april_start(date)
    formatted_result = format_value_pd(result, date)
    log_file.write(formatted_result + "\n")
