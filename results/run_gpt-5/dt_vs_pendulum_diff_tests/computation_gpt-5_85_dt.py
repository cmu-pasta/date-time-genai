
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime
def determine_japanese_era_year(d: date) -> int:
    """
    Determine the Japanese calendar era and year for a given Gregorian date.

    Returns an integer encoded as:
      era_code * 100 + era_year
    where era_code is:
      1 = Meiji (from 1868-01-25)
      2 = Taisho (from 1912-07-30)
      3 = Showa (from 1926-12-25)
      4 = Heisei (from 1989-01-08)
      5 = Reiwa (from 2019-05-01)

    For example:
      Reiwa 5 -> 505
      Heisei 1 -> 401

    Raises:
      ValueError if the date predates the Meiji era start (1868-01-25).
    """
    # Normalize to a date if a datetime is provided
    if isinstance(d, datetime):
        d = d.date()

    # Validate type (basic safeguard)
    if not isinstance(d, date):
        raise TypeError("Input must be a datetime.date or datetime.datetime instance.")

    # Determine era and compute era year using only conditionals (no lists/dicts)
    if d >= date(2019, 5, 1):
        era_code = 5  # Reiwa
        base_year = 2018
    elif d >= date(1989, 1, 8):
        era_code = 4  # Heisei
        base_year = 1988
    elif d >= date(1926, 12, 25):
        era_code = 3  # Showa
        base_year = 1925
    elif d >= date(1912, 7, 30):
        era_code = 2  # Taisho
        base_year = 1911
    elif d >= date(1868, 1, 25):
        era_code = 1  # Meiji
        base_year = 1867
    else:
        raise ValueError("Date predates the Meiji era (1868-01-25) and is unsupported.")

    era_year = d.year - base_year
    return era_code * 100 + era_year

# Entry point: determine_japanese_era_year(d: date) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_85_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_determine_japanese_era_year(d):
    result = determine_japanese_era_year(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")
