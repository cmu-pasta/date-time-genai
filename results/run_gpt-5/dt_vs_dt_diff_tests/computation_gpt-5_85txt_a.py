
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def determine_japanese_era_year(gregorian_date: date) -> int:
    """
    Determine the Japanese calendar era and year for a given Gregorian date.

    Encoding of the return value (single integer to satisfy output constraints):
      result = era_code * 1000 + era_year

      Era code mapping:
        1 = Meiji   (1868-10-23 to 1912-07-29)
        2 = Taisho  (1912-07-30 to 1926-12-24)
        3 = Showa   (1926-12-25 to 1989-01-07)
        4 = Heisei  (1989-01-08 to 2019-04-30)
        5 = Reiwa   (2019-05-01 to open-ended)

    Returns 0 if the date is before the Meiji era.
    """
    # Define era ranges (inclusive) with their numeric codes
    eras = [
        (1, date(1868, 10, 23), date(1912, 7, 29)),  # Meiji
        (2, date(1912, 7, 30), date(1926, 12, 24)),  # Taisho
        (3, date(1926, 12, 25), date(1989, 1, 7)),   # Showa
        (4, date(1989, 1, 8), date(2019, 4, 30)),    # Heisei
        (5, date(2019, 5, 1), date.max),             # Reiwa
    ]

    # Find the era that contains the given date
    for era_code, start, end in eras:
        if start <= gregorian_date <= end:
            # Era year is 1-based from the start date year
            era_year = gregorian_date.year - start.year + 1
            return era_code * 1000 + era_year

    # Date is before Meiji
    return 0

# Entry point: determine_japanese_era_year(gregorian_date: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_85txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_determine_japanese_era_year(gregorian_date):
    result = determine_japanese_era_year(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")
