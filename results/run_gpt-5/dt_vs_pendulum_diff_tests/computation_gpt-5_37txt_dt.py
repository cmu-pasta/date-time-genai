
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def zodiac_sign_code(birth_date: date) -> int:
    """
    Determine the Western zodiac sign for a given birth date.

    Returns an integer code 1–12:
        1 = Aries (Mar 21 – Apr 19)
        2 = Taurus (Apr 20 – May 20)
        3 = Gemini (May 21 – Jun 20)
        4 = Cancer (Jun 21 – Jul 22)
        5 = Leo (Jul 23 – Aug 22)
        6 = Virgo (Aug 23 – Sep 22)
        7 = Libra (Sep 23 – Oct 22)
        8 = Scorpio (Oct 23 – Nov 21)
        9 = Sagittarius (Nov 22 – Dec 21)
        10 = Capricorn (Dec 22 – Jan 19)
        11 = Aquarius (Jan 20 – Feb 18)
        12 = Pisces (Feb 19 – Mar 20)
    """
    m, d = birth_date.month, birth_date.day

    if (m, d) >= (3, 21) and (m, d) <= (4, 19):
        return 1  # Aries
    if (m, d) >= (4, 20) and (m, d) <= (5, 20):
        return 2  # Taurus
    if (m, d) >= (5, 21) and (m, d) <= (6, 20):
        return 3  # Gemini
    if (m, d) >= (6, 21) and (m, d) <= (7, 22):
        return 4  # Cancer
    if (m, d) >= (7, 23) and (m, d) <= (8, 22):
        return 5  # Leo
    if (m, d) >= (8, 23) and (m, d) <= (9, 22):
        return 6  # Virgo
    if (m, d) >= (9, 23) and (m, d) <= (10, 22):
        return 7  # Libra
    if (m, d) >= (10, 23) and (m, d) <= (11, 21):
        return 8  # Scorpio
    if (m, d) >= (11, 22) and (m, d) <= (12, 21):
        return 9  # Sagittarius
    if (m, d) >= (12, 22) or (m, d) <= (1, 19):
        return 10  # Capricorn
    if (m, d) >= (1, 20) and (m, d) <= (2, 18):
        return 11  # Aquarius
    # Remaining case: Pisces (Feb 19 – Mar 20)
    return 12  # Pisces

# Entry point: zodiac_sign_code(birth_date: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_37txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_zodiac_sign_code(birth_date):
    result = zodiac_sign_code(birth_date)
    formatted_result = format_value_dt(result, birth_date)
    log_file.write(formatted_result + "\n")
