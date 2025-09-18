
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def autumnal_equinox_date(year: int) -> date:
    """
    Estimate the date of the September (autumnal) equinox for a given Gregorian year.
    Valid for years 1900 through 2099 (civil-date approximation).
    
    Parameters:
        year (int): Gregorian calendar year.
    
    Returns:
        date: Estimated date of the September equinox in the given year.
    """
    if year < 1900 or year > 2099:
        raise ValueError("Year out of supported range: 1900–2099")

    y = year - 1980
    # Empirical civil-date formula used for Japanese holiday calculations
    day = int((23.2488 + 0.242194 * y) - int(y / 4))
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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_53txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_autumnal_equinox_date(year):
    result = autumnal_equinox_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
