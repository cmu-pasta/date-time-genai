
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime, timedelta
def _delta_t_seconds(year: int) -> float:
    """
    Approximate Delta T (ΔT = TT - UT) in seconds for a given year.
    Uses Espenak/NASA piecewise polynomial approximations valid over wide historical ranges.
    """
    y = float(year)
    if y < -500:
        t = (y - 1820.0) / 100.0
        return 32.0 * (t * t) - 20.0
    elif -500 <= y < 500:
        t = y / 100.0
        return (
            10583.6
            - 1014.41 * t
            + 33.78311 * t**2
            - 5.952053 * t**3
            - 0.1798452 * t**4
            + 0.022174192 * t**5
            + 0.0090316521 * t**6
        )
    elif 500 <= y < 1600:
        t = (y - 1000.0) / 100.0
        return (
            1574.2
            - 556.01 * t
            + 71.23472 * t**2
            + 0.319781 * t**3
            - 0.8503463 * t**4
            - 0.005050998 * t**5
            + 0.0083572073 * t**6
        )
    elif 1600 <= y < 1700:
        u = y - 1600.0
        return 120.0 - 0.9808 * u - 0.01532 * u**2 + (u**3) / 7129.0
    elif 1700 <= y < 1800:
        u = y - 1700.0
        return 8.83 + 0.1603 * u - 0.0059285 * u**2 + 0.00013336 * u**3 - (u**4) / 1174000.0
    elif 1800 <= y < 1860:
        u = y - 1800.0
        return (
            13.72
            - 0.332447 * u
            + 0.0068612 * u**2
            + 0.0041116 * u**3
            - 0.00037436 * u**4
            + 0.0000121272 * u**5
            - 0.0000001699 * u**6
            + 0.000000000875 * u**7
        )
    elif 1860 <= y < 1900:
        u = y - 1860.0
        return 7.62 + 0.5737 * u - 0.251754 * u**2 + 0.01680668 * u**3 - 0.0004473624 * u**4 + (1.0 / 233174.0) * u**5
    elif 1900 <= y < 1920:
        u = y - 1900.0
        return -2.79 + 1.494119 * u - 0.0598939 * u**2 + 0.0061966 * u**3 - 0.000197 * u**4
    elif 1920 <= y < 1941:
        u = y - 1920.0
        return 21.20 + 0.84493 * u - 0.0761 * u**2 + 0.0020936 * u**3
    elif 1941 <= y < 1961:
        u = y - 1950.0
        return 29.07 + 0.407 * u - (u**2) / 233.0 + (u**3) / 2547.0
    elif 1961 <= y < 1986:
        u = y - 1975.0
        return 45.45 + 1.067 * u - (u**2) / 260.0 - (u**3) / 718.0
    elif 1986 <= y < 2005:
        u = y - 2000.0
        return 63.86 + 0.3345 * u - 0.060374 * u**2 + 0.0017275 * u**3 + 0.000651814 * u**4 + 0.00002373599 * u**5
    elif 2005 <= y < 2050:
        u = y - 2000.0
        return 62.92 + 0.32217 * u + 0.005589 * u**2
    elif 2050 <= y < 2150:
        # Transition correction suggested by Espenak
        return (-20.0 + 32.0 * ((y - 1820.0) / 100.0) ** 2) - 0.5628 * (2150.0 - y)
    else:  # y >= 2150
        t = (y - 1820.0) / 100.0
        return -20.0 + 32.0 * (t * t)

def _june_solstice_jde(year: int) -> float:
    """
    Approximate Julian Ephemeris Day (TT) for the June solstice of the given year.
    Uses Meeus' polynomial valid for years roughly 1000..3000 (Table 27.B).
    """
    T = (float(year) - 2000.0) / 1000.0
    # June Solstice coefficients (Meeus):
    # JDE0 = 2451716.56767 + 365241.62603*T + 0.00325*T^2 + 0.00888*T^3 - 0.00030*T^4
    return 2451716.56767 + 365241.62603 * T + 0.00325 * T**2 + 0.00888 * T**3 - 0.00030 * T**4

def _jd_ut_to_datetime(jd_ut: float) -> datetime:
    """
    Convert Julian Day (UT) to a UTC datetime (naive, representing UTC).
    """
    # Algorithm from "Astronomical Algorithms" by Jean Meeus
    J = jd_ut + 0.5
    Z = int(J)
    F = J - Z
    if Z >= 2299161:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha / 4)
    else:
        A = Z
    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)

    # Day with fraction
    day_float = B - D - int(30.6001 * E) + F
    day_int = int(day_float)
    frac = day_float - day_int

    # Time of day from fraction
    seconds_in_day = 86400.0
    total_seconds = frac * seconds_in_day
    hour = int(total_seconds // 3600)
    total_seconds -= hour * 3600
    minute = int(total_seconds // 60)
    total_seconds -= minute * 60
    second = int(total_seconds)
    microsecond = int(round((total_seconds - second) * 1_000_000))
    # Handle rounding overflow
    if microsecond >= 1_000_000:
        microsecond -= 1_000_000
        second += 1
    if second >= 60:
        second -= 60
        minute += 1
    if minute >= 60:
        minute -= 60
        hour += 1
    if hour >= 24:
        hour -= 24
        day_int += 1

    if E < 14:
        month = E - 1
    else:
        month = E - 13
    if month > 2:
        year = C - 4716
    else:
        year = C - 4715

    return datetime(year, month, day_int, hour, minute, second, microsecond)

def get_summer_solstice_date(year: int) -> date:
    """
    Compute the calendar date (UTC) of the Northern Hemisphere summer solstice (June solstice)
    for the given Gregorian year. The result is an approximation based on Meeus' polynomials
    with an estimated ΔT and is generally accurate to within a day.
    """
    # 1) June solstice in TT as JDE
    jde_tt = _june_solstice_jde(year)
    # 2) Estimate ΔT and convert to UT JD
    delta_t = _delta_t_seconds(year)  # seconds
    jd_ut = jde_tt - (delta_t / 86400.0)
    # 3) Convert to UTC datetime and return the calendar date
    dt_utc = _jd_ut_to_datetime(jd_ut)
    return dt_utc.date()

# Entry point: get_summer_solstice_date(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_65txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_get_summer_solstice_date(year):
    result = get_summer_solstice_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
