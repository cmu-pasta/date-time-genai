
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def determine_zodiac_sign(birth_date: date) -> int:
    """
    Determine the Western tropical zodiac sign for the given birth date.

    Returns an integer code:
    1: Aries       (Mar 21 – Apr 19)
    2: Taurus      (Apr 20 – May 20)
    3: Gemini      (May 21 – Jun 20)
    4: Cancer      (Jun 21 – Jul 22)
    5: Leo         (Jul 23 – Aug 22)
    6: Virgo       (Aug 23 – Sep 22)
    7: Libra       (Sep 23 – Oct 22)
    8: Scorpio     (Oct 23 – Nov 21)
    9: Sagittarius (Nov 22 – Dec 21)
    10: Capricorn  (Dec 22 – Jan 19)
    11: Aquarius   (Jan 20 – Feb 18)
    12: Pisces     (Feb 19 – Mar 20)
    """
    m = birth_date.month
    d = birth_date.day

    if (m == 3 and d >= 21) or (m == 4 and d <= 19):
        return 1  # Aries
    elif (m == 4 and d >= 20) or (m == 5 and d <= 20):
        return 2  # Taurus
    elif (m == 5 and d >= 21) or (m == 6 and d <= 20):
        return 3  # Gemini
    elif (m == 6 and d >= 21) or (m == 7 and d <= 22):
        return 4  # Cancer
    elif (m == 7 and d >= 23) or (m == 8 and d <= 22):
        return 5  # Leo
    elif (m == 8 and d >= 23) or (m == 9 and d <= 22):
        return 6  # Virgo
    elif (m == 9 and d >= 23) or (m == 10 and d <= 22):
        return 7  # Libra
    elif (m == 10 and d >= 23) or (m == 11 and d <= 21):
        return 8  # Scorpio
    elif (m == 11 and d >= 22) or (m == 12 and d <= 21):
        return 9  # Sagittarius
    elif (m == 12 and d >= 22) or (m == 1 and d <= 19):
        return 10  # Capricorn
    elif (m == 1 and d >= 20) or (m == 2 and d <= 18):
        return 11  # Aquarius
    else:
        return 12  # Pisces (Feb 19 – Mar 20)

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_37_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_determine_zodiac_sign(birth_date):
    result = determine_zodiac_sign(birth_date)
    formatted_result = format_value_dt(result, birth_date)
    log_file.write(formatted_result + "\n")
