
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
# Precomputed Chinese New Year dates for years 2000 through 2030 (inclusive).
# Source: Standard Chinese lunisolar calendar references.
_CNY_BY_YEAR = {
    2000: date(2000, 2, 5),
    2001: date(2001, 1, 24),
    2002: date(2002, 2, 12),
    2003: date(2003, 2, 1),
    2004: date(2004, 1, 22),
    2005: date(2005, 2, 9),
    2006: date(2006, 1, 29),
    2007: date(2007, 2, 18),
    2008: date(2008, 2, 7),
    2009: date(2009, 1, 26),
    2010: date(2010, 2, 14),
    2011: date(2011, 2, 3),
    2012: date(2012, 1, 23),
    2013: date(2013, 2, 10),
    2014: date(2014, 1, 31),
    2015: date(2015, 2, 19),
    2016: date(2016, 2, 8),
    2017: date(2017, 1, 28),
    2018: date(2018, 2, 16),
    2019: date(2019, 2, 5),
    2020: date(2020, 1, 25),
    2021: date(2021, 2, 12),
    2022: date(2022, 2, 1),
    2023: date(2023, 1, 22),
    2024: date(2024, 2, 10),
    2025: date(2025, 1, 29),
    2026: date(2026, 2, 17),
    2027: date(2027, 2, 6),
    2028: date(2028, 1, 26),
    2029: date(2029, 2, 13),
    2030: date(2030, 2, 3),
}

def get_chinese_new_year(year: int) -> date:
    """
    Return the date of Chinese New Year for the given Gregorian year.

    Parameters:
        year (int): Gregorian year to query.

    Returns:
        date: The date of Chinese New Year for the specified year.

    Raises:
        ValueError: If the year is not supported by the internal table.
    """
    try:
        return _CNY_BY_YEAR[year]
    except KeyError:
        raise ValueError("Year out of supported range (2000-2030).")

# Entry point: get_chinese_new_year(year: int) -> date

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_59_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_get_chinese_new_year(year):
    result = get_chinese_new_year(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
