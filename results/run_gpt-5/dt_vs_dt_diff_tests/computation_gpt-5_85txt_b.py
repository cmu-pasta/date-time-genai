
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime
def determine_japanese_era_year(gregorian_date: date) -> int:
    """
    Determine the Japanese calendar era and year for a given Gregorian date.

    Encoding of the return value:
      result = era_code * 10000 + era_year
        - era_code:
            1 = Meiji  (1868-10-23 to 1912-07-29)
            2 = Taisho (1912-07-30 to 1926-12-24)
            3 = Showa  (1926-12-25 to 1989-01-07)
            4 = Heisei (1989-01-08 to 2019-04-30)
            5 = Reiwa  (2019-05-01 to open-ended)
        - era_year: positive integer starting at 1
      Returns 0 if the date does not fall within the supported eras.
    """

    # Normalize input in case a datetime object is passed (still allowed type).
    if isinstance(gregorian_date, datetime):
        d = gregorian_date.date()
    elif isinstance(gregorian_date, date):
        d = gregorian_date
    else:
        # Unsupported type; adhere to contract by returning 0
        return 0

    # Define era boundaries (inclusive)
    meiji_start = date(1868, 10, 23)
    meiji_end   = date(1912, 7, 29)

    taisho_start = date(1912, 7, 30)
    taisho_end   = date(1926, 12, 24)

    showa_start = date(1926, 12, 25)
    showa_end   = date(1989, 1, 7)

    heisei_start = date(1989, 1, 8)
    heisei_end   = date(2019, 4, 30)

    reiwa_start = date(2019, 5, 1)
    # Reiwa is ongoing; no end date yet.

    # Determine era and compute year-in-era
    if meiji_start <= d <= meiji_end:
        era_code = 1
        era_year = d.year - meiji_start.year + 1
    elif taisho_start <= d <= taisho_end:
        era_code = 2
        era_year = d.year - taisho_start.year + 1
    elif showa_start <= d <= showa_end:
        era_code = 3
        era_year = d.year - showa_start.year + 1
    elif heisei_start <= d <= heisei_end:
        era_code = 4
        era_year = d.year - heisei_start.year + 1
    elif d >= reiwa_start:
        era_code = 5
        era_year = d.year - reiwa_start.year + 1
    else:
        # Before Meiji or otherwise unsupported
        return 0

    # Encode result as a single integer: era_code * 10000 + era_year
    # This supports up to 9999 years per era (well beyond realistic needs).
    return era_code * 10000 + era_year

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_85txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_determine_japanese_era_year(gregorian_date):
    result = determine_japanese_era_year(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")
