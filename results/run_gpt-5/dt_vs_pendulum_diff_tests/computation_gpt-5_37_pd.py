
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def zodiac_sign_index(birth_dt: pendulum.DateTime) -> int:
    """
    Determine the zodiac sign from a birth date.

    Returns an integer code for the sign as follows:
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
    """
    m = birth_dt.month
    d = birth_dt.day

    # Aquarius: Jan 20 - Feb 18
    if (m == 1 and d >= 20) or (m == 2 and d <= 18):
        return 11
    # Pisces: Feb 19 - Mar 20
    if (m == 2 and d >= 19) or (m == 3 and d <= 20):
        return 12
    # Aries: Mar 21 - Apr 19
    if (m == 3 and d >= 21) or (m == 4 and d <= 19):
        return 1
    # Taurus: Apr 20 - May 20
    if (m == 4 and d >= 20) or (m == 5 and d <= 20):
        return 2
    # Gemini: May 21 - Jun 20
    if (m == 5 and d >= 21) or (m == 6 and d <= 20):
        return 3
    # Cancer: Jun 21 - Jul 22
    if (m == 6 and d >= 21) or (m == 7 and d <= 22):
        return 4
    # Leo: Jul 23 - Aug 22
    if (m == 7 and d >= 23) or (m == 8 and d <= 22):
        return 5
    # Virgo: Aug 23 - Sep 22
    if (m == 8 and d >= 23) or (m == 9 and d <= 22):
        return 6
    # Libra: Sep 23 - Oct 22
    if (m == 9 and d >= 23) or (m == 10 and d <= 22):
        return 7
    # Scorpio: Oct 23 - Nov 21
    if (m == 10 and d >= 23) or (m == 11 and d <= 21):
        return 8
    # Sagittarius: Nov 22 - Dec 21
    if (m == 11 and d >= 22) or (m == 12 and d <= 21):
        return 9
    # Capricorn: Dec 22 - Jan 19
    # Remaining case; covers Dec 22-31 and Jan 1-19
    return 10

# Entry point: zodiac_sign_index(birth_dt: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_37_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_zodiac_sign_index(birth_dt):
    result = zodiac_sign_index(birth_dt)
    formatted_result = format_value_pd(result, birth_dt)
    log_file.write(formatted_result + "\n")
