
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
# Helper: Integer ceiling division for non-negative integers
def _ceil_div(a: int, b: int) -> int:
    # Assuming a >= 0 and b > 0 in our use cases
    return (a + b - 1) // b

# Convert a Gregorian date to Julian Day Number (JDN) using the Fliegel–Van Flandern algorithm
def _gregorian_to_jdn(year: int, month: int, day: int) -> int:
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    return day + ((153 * m + 2) // 5) + 365 * y + y // 4 - y // 100 + y // 400 - 32045

# Compute the JDN for an Islamic (Hijri) civil date
def _islamic_to_jdn(year: int, month: int, day: int) -> int:
    # Islamic civil epoch in JDN (corresponds to 622-07-16 Julian)
    ISLAMIC_EPOCH_JDN = 1948439
    # ceil(29.5 * (month - 1)) == ceil_div(59 * (month - 1), 2)
    month_days = _ceil_div(59 * (month - 1), 2)
    leap_days = (3 + 11 * year) // 30
    return day + month_days + (year - 1) * 354 + leap_days + ISLAMIC_EPOCH_JDN - 1

# Convert a JDN to an Islamic (Hijri) civil date
def _jdn_to_islamic(jdn: int):
    ISLAMIC_EPOCH_JDN = 1948439
    # Year calculation
    year = (30 * (jdn - ISLAMIC_EPOCH_JDN) + 10646) // 10631
    # Month calculation
    diff = jdn - (29 + _islamic_to_jdn(year, 1, 1))
    # ceil(diff / 29.5) == ceil_div(2 * diff, 59)
    month = min(12, _ceil_div(2 * diff, 59) + 1)
    # Day calculation
    day = jdn - _islamic_to_jdn(year, month, 1) + 1
    return year, month, day

def determine_islamic_date(gregorian_dt: pendulum.DateTime) -> int:
    # Step 1: Extract Gregorian Y-M-D
    g_year = gregorian_dt.year
    g_month = gregorian_dt.month
    g_day = gregorian_dt.day

    # Step 2: Convert Gregorian date to JDN
    jdn = _gregorian_to_jdn(g_year, g_month, g_day)

    # Step 3: Convert JDN to Islamic (Hijri) civil date
    h_year, h_month, h_day = _jdn_to_islamic(jdn)

    # Step 4: Return as integer formatted YYYYMMDD (Hijri)
    return h_year * 10000 + h_month * 100 + h_day

# Entry point: determine_islamic_date(gregorian_dt: pendulum.DateTime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_55txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_determine_islamic_date(gregorian_dt):
    result = determine_islamic_date(gregorian_dt)
    formatted_result = format_value_pd(result, gregorian_dt)
    log_file.write(formatted_result + "\n")
