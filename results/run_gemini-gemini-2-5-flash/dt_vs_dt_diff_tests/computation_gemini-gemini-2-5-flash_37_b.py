
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def get_zodiac_sign_as_integer(birth_date: datetime) -> int:
    """
    Determines the zodiac sign for a given birth date and returns it as an integer.

    Args:
        birth_date (datetime): A datetime object representing the birth date.

    Returns:
        int: An integer representing the zodiac sign.
             1: Aries (March 21 - April 19)
             2: Taurus (April 20 - May 20)
             3: Gemini (May 21 - June 20)
             4: Cancer (June 21 - July 22)
             5: Leo (July 23 - August 22)
             6: Virgo (August 23 - September 22)
             7: Libra (September 23 - October 22)
             8: Scorpio (October 23 - November 21)
             9: Sagittarius (November 22 - December 21)
             10: Capricorn (December 22 - January 19)
             11: Aquarius (January 20 - February 18)
             12: Pisces (February 19 - March 20)
             Returns 0 if the date is out of a defined range (should not happen with valid dates).
    """
    month = birth_date.month
    day = birth_date.day

    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return 1  # Aries
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return 2  # Taurus
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return 3  # Gemini
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return 4  # Cancer
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return 5  # Leo
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return 6  # Virgo
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return 7  # Libra
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return 8  # Scorpio
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return 9  # Sagittarius
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return 10  # Capricorn
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return 11  # Aquarius
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return 12  # Pisces
    else:
        return 0 # Should not be reached with valid Gregorian calendar dates, but as a fallback.

# Entry point: get_zodiac_sign_as_integer(birth_date: datetime) -> int

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_37_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_zodiac_sign_as_integer(birth_date):
    result = get_zodiac_sign_as_integer(birth_date)
    formatted_result = format_value_dt(result, birth_date)
    log_file.write(formatted_result + "\n")
