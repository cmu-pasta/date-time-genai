
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def chinese_new_year_date(year: int) -> date:
    """
    Return the Gregorian date of Chinese New Year for the given Gregorian year.
    
    Supported years: 1990 through 2030 (inclusive).
    Input: year (integer)
    Output: datetime.date
    """
    # Mapping of Gregorian year -> (month, day) for Chinese New Year
    # Source range compiled from widely published CNY date tables.
    cny_map = {
        1990: (1, 27),
        1991: (2, 15),
        1992: (2, 4),
        1993: (1, 23),
        1994: (2, 10),
        1995: (1, 31),
        1996: (2, 19),
        1997: (2, 7),
        1998: (1, 28),
        1999: (2, 16),
        2000: (2, 5),
        2001: (1, 24),
        2002: (2, 12),
        2003: (2, 1),
        2004: (1, 22),
        2005: (2, 9),
        2006: (1, 29),
        2007: (2, 18),
        2008: (2, 7),
        2009: (1, 26),
        2010: (2, 14),
        2011: (2, 3),
        2012: (1, 23),
        2013: (2, 10),
        2014: (1, 31),
        2015: (2, 19),
        2016: (2, 8),
        2017: (1, 28),
        2018: (2, 16),
        2019: (2, 5),
        2020: (1, 25),
        2021: (2, 12),
        2022: (2, 1),
        2023: (1, 22),
        2024: (2, 10),
        2025: (1, 29),
        2026: (2, 17),
        2027: (2, 6),
        2028: (1, 26),
        2029: (2, 13),
        2030: (2, 3),
    }
    if year not in cny_map:
        raise ValueError("Supported years are 1990 through 2030 inclusive.")
    m, d = cny_map[year]
    return date(year, m, d)

# Entry point: chinese_new_year_date(year: int) -> date

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_59txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_chinese_new_year_date(year):
    result = chinese_new_year_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
