
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime, timedelta
def _jde_december_solstice(year: int) -> float:
    # Meeus approximation for December solstice (JDE) for years roughly 1000..3000
    # Y is in thousands of years from J2000.0
    Y = (year - 2000) / 1000.0
    # Polynomial for December solstice (Meeus, Astronomical Algorithms, ch. 27)
    JDE0 = (
        2451900.05952
        + 365242.74049 * Y
        - 0.000061 * (Y ** 2)
        - 0.000000716 * (Y ** 3)
        + 0.00000000059 * (Y ** 4)
    )
    return JDE0  # In Terrestrial Time; for our purpose, date will be unaffected

def _jd_to_datetime_utc(jd: float) -> datetime:
    # Convert Julian Day Number to Gregorian calendar datetime (UTC-like, no leap seconds)
    # Algorithm adapted from Meeus (with day fraction to time)
    jd += 0.5
    Z = int(jd)
    F = jd - Z

    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha / 4)

    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)

    # Day with fraction
    day = B - D - int(30.6001 * E) + F
    month = E - 1 if E < 14 else E - 13
    year = C - 4716 if month > 2 else C - 4715

    day_int = int(day)
    frac = day - day_int

    # Convert fractional day to seconds
    seconds = int(round(frac * 86400.0))
    # Normalize in case of rounding to 24:00:00
    base_dt = datetime(year, month, day_int)
    dt = base_dt + timedelta(seconds=seconds)
    return dt

def winter_solstice_date(year: int) -> date:
    # Compute approximate JDE for December solstice for the given year
    jde = _jde_december_solstice(year)
    # Convert JDE to a datetime and return the calendar date
    solstice_dt = _jd_to_datetime_utc(jde)
    return solstice_dt.date()

# Entry point: winter_solstice_date(year: int) -> date

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_41_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_winter_solstice_date(year):
    result = winter_solstice_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
