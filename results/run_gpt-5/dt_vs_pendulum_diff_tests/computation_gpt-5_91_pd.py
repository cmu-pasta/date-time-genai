
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def _is_gregorian_leap(year: int) -> bool:
    # Gregorian leap year rule
    return (year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0))

def gregorian_to_indian_national(g_date: pendulum.Date) -> pendulum.Date:
    # Extract components from the Gregorian date
    gy = g_date.year
    # Determine Saka New Year start for the relevant Gregorian year
    start_day_current = 21 if _is_gregorian_leap(gy) else 22
    saka_start_current = pendulum.date(gy, 3, start_day_current)

    if g_date >= saka_start_current:
        saka_year = gy - 78
        chaitra_len = 31 if _is_gregorian_leap(gy) else 30
        saka_year_start = saka_start_current
    else:
        prev_year = gy - 1
        start_day_prev = 21 if _is_gregorian_leap(prev_year) else 22
        saka_year_start = pendulum.date(prev_year, 3, start_day_prev)
        saka_year = gy - 79
        chaitra_len = 31 if _is_gregorian_leap(prev_year) else 30

    # Days since the start of the Saka year
    day_index = (g_date - saka_year_start).in_days()  # 0-based offset

    # Month lengths in the Saka year
    # Chaitra, Vaisakha, Jyaistha, Asadha, Sravana, Bhadra, Asvina, Kartika, Agrahayana, Pausa, Magha, Phalguna
    mlengths_chaitra_first = chaitra_len
    # Next five months of 31 days, then six months of 30 days
    months_lengths = [mlengths_chaitra_first, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 30]

    # Determine Saka month and day
    month = 1
    remaining = day_index
    for ml in months_lengths:
        if remaining < ml:
            day = remaining + 1
            break
        remaining -= ml
        month += 1

    # Construct and return the Saka date as a pendulum.Date
    return pendulum.date(saka_year, month, day)

# Entry point: gregorian_to_indian_national(g_date: pendulum.Date) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_91_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_indian_national(g_date):
    result = gregorian_to_indian_national(g_date)
    formatted_result = format_value_pd(result, g_date)
    log_file.write(formatted_result + "\n")
