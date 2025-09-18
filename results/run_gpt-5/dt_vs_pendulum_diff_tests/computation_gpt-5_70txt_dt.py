
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def julian_to_gregorian(julian_date: date) -> date:
    """
    Convert a Julian calendar date to the corresponding proleptic Gregorian date.
    
    Parameters:
    - julian_date: date object whose Y-M-D fields are interpreted in the Julian calendar.
    
    Returns:
    - date: The equivalent date in the proleptic Gregorian calendar.
    """
    y = julian_date.year
    m = julian_date.month
    d = julian_date.day

    # Step 1: Julian calendar date to Julian Day Number (JDN)
    # Algorithm for Julian calendar:
    # JDN = d + ((153*m' + 2)//5) + 365*y' + y'//4 - 32083
    # where:
    # a = (14 - m)//12
    # y' = y + 4800 - a
    # m' = m + 12*a - 3
    a = (14 - m) // 12
    y_prime = y + 4800 - a
    m_prime = m + 12 * a - 3
    jdn = d + ((153 * m_prime + 2) // 5) + 365 * y_prime + y_prime // 4 - 32083

    # Step 2: JDN to proleptic Gregorian date
    # Inverse algorithm to derive Gregorian Y-M-D from JDN
    A = jdn + 32044
    B = (4 * A + 3) // 146097
    C = A - (146097 * B) // 4
    D = (4 * C + 3) // 1461
    E = C - (1461 * D) // 4
    M = (5 * E + 2) // 153

    day = E - (153 * M + 2) // 5 + 1
    month = M + 3 - 12 * (M // 10)
    year = 100 * B + D - 4800 + (M // 10)

    return date(year, month, day)

# Entry point: julian_to_gregorian(julian_date: date) -> date

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_70txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_julian_to_gregorian(julian_date):
    result = julian_to_gregorian(julian_date)
    formatted_result = format_value_dt(result, julian_date)
    log_file.write(formatted_result + "\n")
