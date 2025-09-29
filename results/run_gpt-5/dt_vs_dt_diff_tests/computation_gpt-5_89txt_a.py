
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, timezone, timedelta
from zoneinfo import ZoneInfo
import math
def _march_equinox_jde_tt(year: int) -> float:
    """
    March equinox, Julian Ephemeris Day (TT), using Meeus (Astronomical Algorithms, ch. 27).
    Valid and accurate primarily for years 1000..3000.
    """
    # Polynomial approximation for March equinox (Table 27.2 / 27.3 form)
    T = (year - 2000) / 1000.0
    # JDE0 for March equinox
    JDE0 = (
        2451623.80984
        + 365242.37404 * T
        + 0.05169 * T * T
        - 0.00411 * T * T * T
        - 0.00057 * T * T * T * T
    )

    # Periodic terms S = sum A * cos(B + C*T) where angles are degrees
    # Table 27.B (March equinox) coefficients:
    terms = (
        (485, 324.96, 1934.136),
        (203, 337.23, 32964.467),
        (199, 342.08, 20.186),
        (182, 27.85, 445267.112),
        (156, 73.14, 45036.886),
        (136, 171.52, 22518.443),
        (77, 222.54, 65928.934),
        (74, 296.72, 3034.906),
        (70, 243.58, 9037.513),
        (58, 119.81, 33718.147),
        (52, 297.17, 150.678),
        (50, 21.02, 2281.226),
        (45, 247.54, 29929.562),
        (44, 325.15, 31555.956),
        (29, 60.93, 4443.417),
        (18, 155.12, 67555.328),
        (17, 288.79, 4562.452),
        (16, 198.04, 62894.029),
        (14, 199.76, 31436.921),
        (12, 95.39, 14577.848),
        (12, 287.11, 31931.756),
        (12, 320.81, 34777.259),
        (9, 227.73, 1222.114),
        (8, 15.45, 16859.074),
    )

    S = 0.0
    deg2rad = math.pi / 180.0
    for A, B, C in terms:
        S += A * math.cos((B + C * T) * deg2rad)

    # Correction in days
    JDE = JDE0 + 0.00001 * S
    return JDE

def _delta_t_seconds(year: int, month: int = 3) -> float:
    """
    Approximate ΔT = TT - UT in seconds.
    Uses polynomial approximations from NASA/Espenak, with reasonable coverage for years 1000..3000.
    The month parameter allows slight refinement around the equinox.
    """
    y = year + (month - 0.5) / 12.0  # fractional year near March
    if y < -500:
        u = (y - 1820) / 100.0
        return -20.0 + 32.0 * u * u
    elif -500 <= y < 500:
        u = y / 100.0
        return 10583.6 - 1014.41*u + 33.78311*u*u - 5.952053*u**3 - 0.1798452*u**4 + 0.022174192*u**5 + 0.0090316521*u**6
    elif 500 <= y < 1600:
        u = (y - 1000) / 100.0
        return 1574.2 - 556.01*u + 71.23472*u*u + 0.319781*u**3 - 0.8503463*u**4 - 0.005050998*u**5 + 0.0083572073*u**6
    elif 1600 <= y < 1700:
        t = y - 1600.0
        return 120.0 - 0.9808*t - 0.01532*t*t + t**3 / 7129.0
    elif 1700 <= y < 1800:
        t = y - 1700.0
        return 8.83 + 0.1603*t - 0.0059285*t*t + 0.00013336*t**3 - t**4 / 1174000.0
    elif 1800 <= y < 1860:
        t = y - 1800.0
        return 13.72 - 0.332447*t + 0.0068612*t*t + 0.0041116*t**3 - 0.00037436*t**4 + 0.0000121272*t**5 - 0.0000001699*t**6 + 0.000000000875*t**7
    elif 1860 <= y < 1900:
        t = y - 1860.0
        return 7.62 + 0.5737*t - 0.251754*t*t + 0.01680668*t**3 - 0.0004473624*t**4 + t**5 / 233174.0
    elif 1900 <= y < 1920:
        t = y - 1900.0
        return -2.79 + 1.494119*t - 0.0598939*t*t + 0.0061966*t**3 - 0.000197*t**4
    elif 1920 <= y < 1941:
        t = y - 1920.0
        return 21.20 + 0.84493*t - 0.076100*t*t + 0.0020936*t**3
    elif 1941 <= y < 1961:
        t = y - 1950.0
        return 29.07 + 0.407*t - t*t/233.0 + t**3/2547.0
    elif 1961 <= y < 1986:
        t = y - 1975.0
        return 45.45 + 1.067*t - t*t/260.0 - t**3/718.0
    elif 1986 <= y < 2005:
        t = y - 2000.0
        return 63.86 + 0.3345*t - 0.060374*t*t + 0.0017275*t**3 + 0.000651814*t**4 + 0.00002373599*t**5
    elif 2005 <= y < 2050:
        t = y - 2000.0
        return 62.92 + 0.32217*t + 0.005589*t*t
    elif 2050 <= y < 2150:
        return -20.0 + 32.0 * ((y - 1820.0) / 100.0) ** 2 - 0.5628 * (2150.0 - y)
    else:  # y >= 2150
        u = (y - 1820.0) / 100.0
        return -20.0 + 32.0 * u * u

def _jd_to_datetime_utc(jd: float) -> datetime:
    """
    Convert Julian Day (UTC) to a timezone-aware UTC datetime.
    Algorithm based on the method in 'Astronomical Algorithms'.
    """
    # Shift to start at midnight by adding 0.5 and splitting integer and fractional parts
    J = jd + 0.5
    Z = int(math.floor(J))
    F = J - Z

    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha / 4)

    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)

    # Day with fractional part
    day_float = B - D - int(30.6001 * E) + F
    day = int(math.floor(day_float))
    frac = day_float - day

    # Month and year
    if E < 14:
        month = E - 1
    else:
        month = E - 13
    if month > 2:
        year = C - 4716
    else:
        year = C - 4715

    # Convert fractional day to time
    seconds_in_day = 86400.0
    total_seconds = frac * seconds_in_day
    # Round to nearest microsecond
    microseconds = int(round((total_seconds - int(total_seconds)) * 1_000_000))
    # Handle carry into seconds if rounding pushed us to 1_000_000
    sec = int(total_seconds)
    if microseconds >= 1_000_000:
        microseconds -= 1_000_000
        sec += 1
    # Handle possible day rollover
    if sec >= 86400:
        sec -= 86400
        # Increment date by one day
        dt = datetime(year, month, day, tzinfo=timezone.utc) + timedelta(days=1)
        year, month, day = dt.year, dt.month, dt.day

    hour = sec // 3600
    minute = (sec % 3600) // 60
    second = sec % 60

    return datetime(year, month, day, hour, minute, second, microseconds, tzinfo=timezone.utc)

def nowruz_date_for_gregorian_year(year: int) -> date:
    """
    Compute the Gregorian date of Persian New Year (Nowruz) for a given Gregorian year.
    The result is the civil date in Tehran that contains the exact instant of the March equinox.
    """
    # 1) March equinox in terrestrial time as JDE
    jde_tt = _march_equinox_jde_tt(year)
    # 2) Estimate ΔT for this epoch (seconds), convert to days
    delta_t = _delta_t_seconds(year, 3) / 86400.0
    # 3) Convert JDE(TT) to JD(UTC)
    jd_utc = jde_tt - delta_t
    # 4) Convert to UTC datetime
    eqx_utc = _jd_to_datetime_utc(jd_utc)
    # 5) Convert to Tehran local time
    tehran = ZoneInfo("Asia/Tehran")
    eqx_tehran = eqx_utc.astimezone(tehran)
    # 6) Return the date component: Nowruz date in Gregorian calendar
    return eqx_tehran.date()

# Entry point: nowruz_date_for_gregorian_year(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_89txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_nowruz_date_for_gregorian_year(year):
    result = nowruz_date_for_gregorian_year(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
