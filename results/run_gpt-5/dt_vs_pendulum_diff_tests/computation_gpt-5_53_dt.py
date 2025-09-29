
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def autumnal_equinox_date(year: int) -> date:
    """
    Calculate the date of the autumnal equinox for a given year using
    widely used approximation formulas (sufficient for civil use, e.g., Japan's
    Autumnal Equinox Day calculation).

    Supported year ranges:
      - 1900 to 1979
      - 1980 to 2099
      - 2100 to 2150
    """
    if 1900 <= year <= 1979:
        day = int(23.2588 + 0.242194 * (year - 1900) - ((year - 1900) // 4))
    elif 1980 <= year <= 2099:
        day = int(23.2488 + 0.242194 * (year - 1980) - ((year - 1980) // 4))
    elif 2100 <= year <= 2150:
        day = int(24.2488 + 0.242194 * (year - 2100) - ((year - 2100) // 4))
    else:
        raise ValueError("Year out of supported range (1900-2150).")

    return date(year, 9, day)

# Entry point: autumnal_equinox_date(year: int) -> date

def format_value_dt(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, datetime):
            formatted_values.append(value.isoformat())
        elif isinstance(value, date):
            # Use strftime to format the date similar to to_date_string()
            formatted_values.append(value.strftime("%Y-%m-%d"))
        elif isinstance(value, time):
            formatted_values.append(value.isoformat())
        elif isinstance(value, timedelta):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_53_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_autumnal_equinox_date(year):
    result = autumnal_equinox_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
