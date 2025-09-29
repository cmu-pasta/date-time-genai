
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def date_to_julian_day_number(d: date) -> int:
    # Extract Gregorian date components
    y = d.year
    m = d.month
    day = d.day

    # Gregorian calendar to Julian Day Number (proleptic Gregorian)
    a = (14 - m) // 12
    y_adj = y + 4800 - a
    m_adj = m + 12 * a - 3

    jdn = day + ((153 * m_adj + 2) // 5) + 365 * y_adj + (y_adj // 4) - (y_adj // 100) + (y_adj // 400) - 32045
    return jdn

# Entry point: date_to_julian_day_number(d: date) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_10_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_date_to_julian_day_number(d):
    result = date_to_julian_day_number(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")
