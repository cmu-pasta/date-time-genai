
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def _march_equinox_jde_tt(year: int) -> float:
    # Meeus: March equinox JDE approximation (valid for years near 2000)
    T = (year - 2000) / 1000.0
    return (
        2451623.80984
        + 365242.37404 * T
        + 0.05169 * T**2
        - 0.00411 * T**3
        - 0.00057 * T**4
    )

def _delta_t_seconds(year: int) -> float:
    y = float(year)
    # Espenak-Meeus delta T approximations (seconds)
    if year < -500:
        u = (y - 1820.0) / 100.0
        dt = -20.0 + 32.0 * (u * u)
    elif -500 <= year < 500:
        u = (y - 2000.0) / 100.0
        dt = (
            10583.6
            - 1014.41 * u
            + 33.78311 * u**2
            - 5.952053 * u**3
            - 0.1798452 * u**4
            + 0.022174192 * u**5
            + 0.0090316521 * u**6
        )
    elif 500 <= year < 1600:
        u = (y - 1000.0) / 100.0
        dt = (
            1574.2
            - 556.01 * u
            + 71.23472 * u**2
            + 0.319781 * u**3
            - 0.8503463 * u**4
            - 0.005050998 * u**5
            + 0.0083572073 * u**6
        )
    elif 1600 <= year < 1700:
        t = y - 1600.0
        dt = 120.0 - 0.9808 * t - 0.01532 * t**2 + (t**3) / 7129.0
    elif 1700 <= year < 1800:
        t = y - 1700.0
        dt = 8.83 + 0.1603 * t - 0.0059285 * t**2 + 0.00013336 * t**3 - 1.5e-6 * t**4
    elif 1800 <= year < 1900:
        u = (y - 1800.0) / 100.0
        dt = (
            13.72
            - 33.2447 * u
            + 68.612 * u**2
            + 4111.6 * u**3
            - 37436.0 * u**4
            + 121272.0 * u**5
            - 169900.0 * u**6
            + 87500.0 * u**7
        )
    elif 1900 <= year < 1986:
        u = (y - 1900.0) / 100.0
        dt = (
            -2.79
            + 1.494119 * u
            - 0.0598939 * u**2
            + 0.0061966 * u**3
            - 0.000197 * u**4
        )
    elif 1986 <= year < 2005:
        t = y - 2000.0
        dt = (
            63.86
            + 0.3345 * t
            - 0.060374 * t**2
            + 0.0017275 * t**3
            + 0.000651814 * t**4
            + 0.00002373599 * t**5
        )
    elif 2005 <= year < 2050:
        t = y - 2000.0
        dt = 62.92 + 0.32217 * t + 0.005589 * t**2
    elif 2050 <= year <= 2150:
        # Linear bridge to general quadratic; modest accuracy
        dt = -20.0 + 32.0 * ((y - 1820.0) / 100.0) ** 2 - 0.5628 * (2150.0 - y)
    else:  # year > 2150
        t = (y - 2000.0) / 100.0
        dt = 102.0 + 102.0 * t + 25.3 * t**2
    return float(dt)

def _jd_utc_to_pendulum_datetime_utc(jd_utc: float) -> pendulum.DateTime:
    # Convert Julian Day (UTC) to Gregorian calendar date/time in UTC.
    JD = jd_utc
    ZF = JD + 0.5
    Z = int(ZF)
    F = ZF - Z

    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha / 4)

    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)

    day_float = B - D - int(30.6001 * E) + F
    day = int(day_float)
    frac = day_float - day

    if E < 14:
        month = E - 1
    else:
        month = E - 13

    if month > 2:
        year = C - 4716
    else:
        year = C - 4715

    # Convert fractional day to h:m:s
    total_seconds = round(frac * 86400.0)
    # Handle overflow if rounding pushes to next day
    if total_seconds >= 86400:
        total_seconds -= 86400
        # Increment date by one day using pendulum for correctness
        base = pendulum.datetime(year, int(month), int(day), tz="UTC").add(days=1)
        year, month, day = base.year, base.month, base.day

    hour = int(total_seconds // 3600)
    minute = int((total_seconds % 3600) // 60)
    second = int(total_seconds % 60)

    return pendulum.datetime(int(year), int(month), int(day), hour, minute, second, tz="UTC")

def nowruz_date_for_gregorian_year(year: int) -> pendulum.Date:
    # Step 1: Approximate March equinox in Terrestrial Time (JDE)
    jde_tt = _march_equinox_jde_tt(year)
    # Step 2: Convert TT to UTC using ΔT (seconds)
    delta_t = _delta_t_seconds(year)
    jd_utc = jde_tt - (delta_t / 86400.0)
    # Step 3: Convert JD (UTC) to pendulum DateTime in UTC
    dt_utc = _jd_utc_to_pendulum_datetime_utc(jd_utc)
    # Step 4: Convert to Tehran time, then take the local calendar date as Nowruz date
    tehran = pendulum.timezone("Asia/Tehran")
    dt_tehran = dt_utc.in_timezone(tehran)
    return dt_tehran.date()

# Entry point: nowruz_date_for_gregorian_year(year: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_89_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_nowruz_date_for_gregorian_year(year):
    result = nowruz_date_for_gregorian_year(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
