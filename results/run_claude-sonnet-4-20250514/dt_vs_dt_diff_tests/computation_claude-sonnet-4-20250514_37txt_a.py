
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def determine_zodiac_sign(birth_date: date) -> int:
    month = birth_date.month
    day = birth_date.day
    
    # Zodiac sign mapping (1-12):
    # 1: Capricorn, 2: Aquarius, 3: Pisces, 4: Aries, 5: Taurus, 6: Gemini
    # 7: Cancer, 8: Leo, 9: Virgo, 10: Libra, 11: Scorpio, 12: Sagittarius
    
    if (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return 1  # Capricorn
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return 2  # Aquarius
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return 3  # Pisces
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return 4  # Aries
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return 5  # Taurus
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return 6  # Gemini
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return 7  # Cancer
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return 8  # Leo
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return 9  # Virgo
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return 10  # Libra
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return 11  # Scorpio
    else:  # (month == 11 and day >= 22) or (month == 12 and day <= 21)
        return 12  # Sagittarius

# Entry point: determine_zodiac_sign(birth_date: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_37txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_determine_zodiac_sign(birth_date):
    result = determine_zodiac_sign(birth_date)
    formatted_result = format_value_dt(result, birth_date)
    log_file.write(formatted_result + "\n")
