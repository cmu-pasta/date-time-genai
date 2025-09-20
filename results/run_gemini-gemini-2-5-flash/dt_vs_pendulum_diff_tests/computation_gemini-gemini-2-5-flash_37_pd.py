
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def get_zodiac_sign_id(birth_date: pendulum.Date) -> int:
    """
    Determines the zodiac sign for a given birth date and returns its
    corresponding integer ID.

    Zodiac Sign IDs:
    1: Aries (Mar 21 - Apr 19)
    2: Taurus (Apr 20 - May 20)
    3: Gemini (May 21 - Jun 20)
    4: Cancer (Jun 21 - Jul 22)
    5: Leo (Jul 23 - Aug 22)
    6: Virgo (Aug 23 - Sep 22)
    7: Libra (Sep 23 - Oct 22)
    8: Scorpio (Oct 23 - Nov 21)
    9: Sagittarius (Nov 22 - Dec 21)
    10: Capricorn (Dec 22 - Jan 19)
    11: Aquarius (Jan 20 - Feb 18)
    12: Pisces (Feb 19 - Mar 20)

    Args:
        birth_date: A pendulum.Date object representing the birth date.

    Returns:
        An integer representing the zodiac sign ID.
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
        return 10 # Capricorn
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return 11 # Aquarius
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return 12 # Pisces
    else:
        # This case should ideally not be reached with valid dates,
        # but provides a fallback.
        # For a practical solution, one might raise an error or return a specific error code.
        # For this problem, we'll assume valid dates covering all signs.
        return 0 # Indicate an unknown or invalid sign for robustness, if ever reached.

# Entry point: get_zodiac_sign_id(birth_date: pendulum.Date) -> int

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_37_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_get_zodiac_sign_id(birth_date):
    result = get_zodiac_sign_id(birth_date)
    formatted_result = format_value_pd(result, birth_date)
    log_file.write(formatted_result + "\n")
