
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
# Approximate Delta T (TT - UT) in seconds based on Espenak/Meeus piecewise polynomials.
# Sufficiently accurate for determining the calendar date around the equinox for modern years.
def _approx_delta_t_seconds(year: int) -> float:
    y = float(year)
    if 2005 <= y <= 2050:
        t = y - 2000.0
        return 62.92 + 0.32217 * t + 0.005589 * t * t
    elif 1986 <= y < 2005:
        t = y - 2000.0
        return 63.86 + 0.3345 * t - 0.060374 * t * t + 0.0017275 * t ** 3 + 0.000651814 * t ** 4 + 0.00002373599 * t ** 5
    elif 1900 <= y < 1986:
        t = y - 1900.0
        return -2.79 + 1.494119 * t - 0.0598939 * t * t + 0.0061966 * t ** 3 - 0.000197 * t ** 4
    elif 1800 <= y < 1900:
        t = y - 1860.0
        return 13.72 - 0.332447 * t + 0.0068612 * t ** 2 + 0.0041116 * t ** 3 - 0.00037436 * t ** 4 + 0.0000121272 * t ** 5 - 0.0000001699 * t ** 6 + 0.000000000875 * t ** 7
    elif 1700 <= y < 1800:
        t = y - 1700.0
        return 8.83 + 0.1603 * t - 0.0059285 * t ** 2 + 0.00013336 * t ** 3 - 0.0000015 * t ** 4
    elif 1600 <= y < 1700:
        t = y - 1600.0
        return 120.0 - 0.9808 * t - 0.01532 * t ** 2 + t ** 3 / 7129.0
    elif 500 <= y < 1600:
        t = y - 1000.0
        return 1574.2 - 556.01 * t / 100.0 + 71.23472 * (t / 100.0) ** 2 + 0.319781 * (t / 100.0) ** 3 - 0.8503463 * (t / 100.0) ** 4 - 0.005050998 * (t / 100.0) ** 5 + 0.0083572073 * (t / 100.0) ** 6
    else:
        # Very rough fallback outside the above ranges
        # (good enough to not shift the date in most practical modern use cases).
        return 69.0

# March equinox JDE (Terrestrial Time) using Meeus polynomial.
# For years 1000..3000:
#   JDE = 2451623.80984 + 365242.37404*T + 0.05169*T^2 - 0.00411*T^3 - 0.00057*T^4
# Where T = (year - 2000)/1000
# For our goal (calendar date in Tehran), this approximation is sufficient.
def _march_equinox_jde_tt(year: int) -> float:
    T = (float(year) - 2000.0) / 1000.0
    return (
        2451623.80984
        + 365242.37404 * T
        + 0.05169 * T * T
        - 0.00411 * T ** 3
        - 0.00057 * T ** 4
    )

# Convert Julian Day (UTC) to pendulum.DateTime in UTC using Unix epoch relation.
def _jd_utc_to_pendulum_datetime_utc(jd_utc: float) -> pendulum.DateTime:
    # JD at Unix epoch (1970-01-01T00:00:00Z) is 2440587.5
    seconds_since_unix_epoch = (jd_utc - 2440587.5) * 86400.0
    return pendulum.from_timestamp(seconds_since_unix_epoch, tz="UTC")

# Core computation: find Nowruz date (in Tehran) for a given Gregorian year.
def find_nowruz_date(gregorian_year: int) -> pendulum.Date:
    # 1) March equinox in TT (JDE)
    jde_tt = _march_equinox_jde_tt(gregorian_year)

    # 2) Estimate Delta T and convert TT to UT (UTC approximation)
    delta_t_sec = _approx_delta_t_seconds(gregorian_year)
    jd_utc = jde_tt - (delta_t_sec / 86400.0)

    # 3) Convert to UTC DateTime
    equinox_utc = _jd_utc_to_pendulum_datetime_utc(jd_utc)

    # 4) Convert to Tehran time and take the calendar date
    tehran_tz: pendulum.Timezone = pendulum.timezone("Asia/Tehran")
    equinox_tehran: pendulum.DateTime = equinox_utc.in_timezone(tehran_tz)
    return equinox_tehran.date()

# Entry point: find_nowruz_date(gregorian_year: int) -> pendulum.Date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_89txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_nowruz_date(gregorian_year):
    result = find_nowruz_date(gregorian_year)
    formatted_result = format_value_pd(result, gregorian_year)
    log_file.write(formatted_result + "\n")
