
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def vernal_equinox_date(year: int) -> date:
    """
    Compute the approximate date of the vernal equinox (March equinox) for a given year.
    This implementation uses a widely known approximation valid for Gregorian years 1900–2099,
    yielding a date in March (typically the 20th or 21st).

    Parameters:
        year (int): Gregorian calendar year, must be in the range 1900–2099.

    Returns:
        date: The approximated date of the vernal equinox for the given year.
    """
    if not (1900 <= year <= 2099):
        raise ValueError("Year out of supported range: valid for 1900–2099")

    # Approximation used in practice (e.g., for Japan's 'Shunbun no Hi')
    # day = floor(20.8431 + 0.242194*(year - 1980) - floor((year - 1980)/4))
    offset = year - 1980
    day = int(20.8431 + 0.242194 * offset - (offset // 4))

    return date(year, 3, day)

# Entry point: vernal_equinox_date(year: int) -> date

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_71txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_vernal_equinox_date(year):
    result = vernal_equinox_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
