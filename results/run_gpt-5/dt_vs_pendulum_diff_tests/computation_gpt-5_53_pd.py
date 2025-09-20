
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def _jde_september_equinox(year: int) -> float:
    # Meeus approximation (Astronomical Algorithms) for the September equinox (JDE)
    # Valid with good accuracy near years around 2000; acceptable for date determination.
    T = (year - 2000) / 1000.0
    T2 = T * T
    T3 = T2 * T
    T4 = T3 * T
    # Polynomial for September equinox
    jde = (
        2451810.21715
        + 365242.01767 * T
        + 0.11575 * T2
        - 0.00337 * T3
        - 0.00078 * T4
    )
    return jde

def _calendar_from_jd(jd: float) -> pendulum.DateTime:
    # Convert Julian Day to Gregorian date-time (UTC), returning a pendulum.DateTime
    # Algorithm based on standard JD -> Gregorian conversion
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

    day_float = B - D - int(30.6001 * E) + F
    day = int(day_float)
    frac_day = day_float - day

    if E < 14:
        month = E - 1
    else:
        month = E - 13

    if month > 2:
        year = C - 4716
    else:
        year = C - 4715

    # Convert fractional day to time components
    hours_float = frac_day * 24.0
    hour = int(hours_float)
    minutes_float = (hours_float - hour) * 60.0
    minute = int(minutes_float)
    seconds_float = (minutes_float - minute) * 60.0
    second = int(seconds_float + 0.5)  # round to nearest second

    # Normalize possible 60 seconds rounding
    if second >= 60:
        second -= 60
        minute += 1
    if minute >= 60:
        minute -= 60
        hour += 1
    if hour >= 24:
        hour -= 24
        # advance date by one day
        base = pendulum.date(year, month, day).add(days=1)
        year, month, day = base.year, base.month, base.day

    tz = pendulum.timezone("UTC")
    return pendulum.datetime(year, month, day, hour, minute, second, tz=tz)

def autumnal_equinox_date(year: int) -> pendulum.Date:
    # Compute JDE of the September equinox
    jde = _jde_september_equinox(year)
    # Convert JDE to UTC calendar date-time
    dt_utc = _calendar_from_jd(jde)
    # Return only the calendar date
    return dt_utc.date()

# Entry point: autumnal_equinox_date(year: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_53_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_autumnal_equinox_date(year):
    result = autumnal_equinox_date(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
