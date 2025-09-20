
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def chinese_new_year(year: int) -> pendulum.Date:
    """
    Return the date of Chinese New Year for the given Gregorian year as a pendulum.Date.
    Supported years: 1990 through 2030.
    """
    # Internal mapping of Gregorian year -> (month, day) for Chinese New Year
    # Source: Commonly referenced calendars for Chinese New Year dates (1990–2030)
    cny_md = {
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

    if year not in cny_md:
        raise ValueError("Supported years are from 1990 through 2030.")

    month, day = cny_md[year]
    return pendulum.date(year, month, day)

# Entry point: chinese_new_year(year: int) -> pendulum.Date

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_59_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_chinese_new_year(year):
    result = chinese_new_year(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
