
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def get_zodiac_sign(birth_date: date) -> int:
    """
    Given a birth date, return the zodiac sign as an integer.
    Aries=1, Taurus=2, Gemini=3, Cancer=4, Leo=5, Virgo=6, 
    Libra=7, Scorpio=8, Sagittarius=9, Capricorn=10, 
    Aquarius=11, Pisces=12
    """
    month = birth_date.month
    day = birth_date.day
    
    if   (month == 3 and day >= 21) or (month == 4 and day <= 19):
        # Aries
        return 1
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        # Taurus
        return 2
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        # Gemini
        return 3
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        # Cancer
        return 4
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        # Leo
        return 5
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        # Virgo
        return 6
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        # Libra
        return 7
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        # Scorpio
        return 8
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        # Sagittarius
        return 9
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        # Capricorn
        return 10
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        # Aquarius
        return 11
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        # Pisces
        return 12
    else:
        # Fallback, in case input is invalid
        return 0

# Entry point: get_zodiac_sign(birth_date: date) -> int

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_90txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_get_zodiac_sign(birth_date):
    result = get_zodiac_sign(birth_date)
    formatted_result = format_value_dt(result, birth_date)
    log_file.write(formatted_result + "\n")
