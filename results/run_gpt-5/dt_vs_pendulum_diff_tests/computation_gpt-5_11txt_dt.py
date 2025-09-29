
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def find_easter_sunday(year: int) -> date:
    """
    Compute the date of Easter Sunday for a given year using the
    Meeus/Jones/Butcher algorithm for the Gregorian calendar.
    
    Input:
      - year: integer in the range 1..9999
    
    Output:
      - date: a datetime.date representing Easter Sunday of the given year
    """
    if not (1 <= year <= 9999):
        raise ValueError("year must be in the range 1..9999")
    
    # Meeus/Jones/Butcher algorithm
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31  # 3 = March, 4 = April
    day = ((h + l - 7 * m + 114) % 31) + 1

    return date(year, month, day)

# Entry point: find_easter_sunday(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_11txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_easter_sunday(year):
    result = find_easter_sunday(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
