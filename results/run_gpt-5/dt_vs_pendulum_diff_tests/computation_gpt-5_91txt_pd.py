
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def gregorian_to_indian_national_date(g_date: pendulum.Date) -> pendulum.Date:
    """
    Convert a Gregorian date (pendulum.Date) to the Indian National Calendar (Saka) date.
    Returns a pendulum.Date whose year, month, and day fields correspond to the Saka calendar.
    """
    # Normalize to a DateTime at midnight for safe arithmetic
    dt = pendulum.datetime(g_date.year, g_date.month, g_date.day)

    gy = dt.year
    # Chaitra 1 falls on March 22 in common years and March 21 in Gregorian leap years
    is_gy_leap = pendulum.datetime(gy, 1, 1).is_leap_year()
    chaitra_start_this_year = pendulum.datetime(gy, 3, 21 if is_gy_leap else 22)

    if dt >= chaitra_start_this_year:
        # Saka year starts this Gregorian year
        saka_year = gy - 78
        start_dt = chaitra_start_this_year
        chaitra_len = 31 if is_gy_leap else 30
    else:
        # Saka year started in the previous Gregorian year
        prev = gy - 1
        is_prev_leap = pendulum.datetime(prev, 1, 1).is_leap_year()
        start_dt = pendulum.datetime(prev, 3, 21 if is_prev_leap else 22)
        saka_year = gy - 79
        chaitra_len = 31 if is_prev_leap else 30

    # Month lengths in Saka calendar from Chaitra to Phalguna
    # Chaitra length depends on the leap condition determined above
    month_lengths = (
        chaitra_len,  # 1. Chaitra
        31,           # 2. Vaisakha
        31,           # 3. Jyaistha
        31,           # 4. Asadha
        31,           # 5. Sravana
        31,           # 6. Bhadra
        30,           # 7. Asvina
        30,           # 8. Kartika
        30,           # 9. Agrahayana
        30,           # 10. Pausa
        30,           # 11. Magha
        30,           # 12. Phalguna
    )

    # Days elapsed since Chaitra 1 (0-based)
    days_since_start = start_dt.diff(dt).in_days()

    # Determine Saka month and day
    remaining = days_since_start
    saka_month = 1
    for ml in month_lengths:
        if remaining < ml:
            saka_day = remaining + 1
            break
        remaining -= ml
        saka_month += 1

    # Construct a pendulum.Date to carry Saka Y-M-D components
    saka_date = pendulum.date(saka_year, saka_month, saka_day)
    return saka_date

# Entry point: gregorian_to_indian_national_date(g_date: pendulum.Date) -> pendulum.Date

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_91txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_indian_national_date(g_date):
    result = gregorian_to_indian_national_date(g_date)
    formatted_result = format_value_pd(result, g_date)
    log_file.write(formatted_result + "\n")
