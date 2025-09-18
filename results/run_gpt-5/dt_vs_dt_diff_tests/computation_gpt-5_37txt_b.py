
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def zodiac_sign_code(birth_date: date) -> int:
    """
    Determine the zodiac sign for a given birth date and return it as an integer code.

    Zodiac code mapping (1-12):
      1 = Capricorn   (Dec 22 - Jan 19)
      2 = Aquarius    (Jan 20 - Feb 18)
      3 = Pisces      (Feb 19 - Mar 20)
      4 = Aries       (Mar 21 - Apr 19)
      5 = Taurus      (Apr 20 - May 20)
      6 = Gemini      (May 21 - Jun 20)
      7 = Cancer      (Jun 21 - Jul 22)
      8 = Leo         (Jul 23 - Aug 22)
      9 = Virgo       (Aug 23 - Sep 22)
     10 = Libra       (Sep 23 - Oct 22)
     11 = Scorpio     (Oct 23 - Nov 21)
     12 = Sagittarius (Nov 22 - Dec 21)
    """
    m = birth_date.month
    d = birth_date.day

    # Capricorn: Dec 22 - Jan 19
    if (m == 12 and d >= 22) or (m == 1 and d <= 19):
        return 1
    # Aquarius: Jan 20 - Feb 18
    if (m == 1 and d >= 20) or (m == 2 and d <= 18):
        return 2
    # Pisces: Feb 19 - Mar 20
    if (m == 2 and d >= 19) or (m == 3 and d <= 20):
        return 3
    # Aries: Mar 21 - Apr 19
    if (m == 3 and d >= 21) or (m == 4 and d <= 19):
        return 4
    # Taurus: Apr 20 - May 20
    if (m == 4 and d >= 20) or (m == 5 and d <= 20):
        return 5
    # Gemini: May 21 - Jun 20
    if (m == 5 and d >= 21) or (m == 6 and d <= 20):
        return 6
    # Cancer: Jun 21 - Jul 22
    if (m == 6 and d >= 21) or (m == 7 and d <= 22):
        return 7
    # Leo: Jul 23 - Aug 22
    if (m == 7 and d >= 23) or (m == 8 and d <= 22):
        return 8
    # Virgo: Aug 23 - Sep 22
    if (m == 8 and d >= 23) or (m == 9 and d <= 22):
        return 9
    # Libra: Sep 23 - Oct 22
    if (m == 9 and d >= 23) or (m == 10 and d <= 22):
        return 10
    # Scorpio: Oct 23 - Nov 21
    if (m == 10 and d >= 23) or (m == 11 and d <= 21):
        return 11
    # Sagittarius: Nov 22 - Dec 21
    # Remaining dates fall here by exclusion, but we keep the explicit check for clarity.
    if (m == 11 and d >= 22) or (m == 12 and d <= 21):
        return 12

    # Fallback (should never be reached with valid Gregorian dates)
    # Assign Capricorn by default to maintain integer return type.
    return 1

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_37txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_zodiac_sign_code(birth_date):
    result = zodiac_sign_code(birth_date)
    formatted_result = format_value_dt(result, birth_date)
    log_file.write(formatted_result + "\n")
