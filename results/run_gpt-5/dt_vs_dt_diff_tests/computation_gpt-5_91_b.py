
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def _is_gregorian_leap(year: int) -> bool:
    # Use datetime.date construction to test for Feb 29 existence
    try:
        date(year, 2, 29)
        return True
    except ValueError:
        return False

def gregorian_to_saka(gregorian_date: date) -> date:
    # Determine Saka New Year start for the relevant Gregorian year
    gy = gregorian_date.year
    gy_is_leap = _is_gregorian_leap(gy)
    saka_start_current = date(gy, 3, 21 if gy_is_leap else 22)

    if gregorian_date >= saka_start_current:
        saka_year = gy - 78
        saka_year_start = saka_start_current
        chaitra_len = 31 if gy_is_leap else 30
    else:
        prev_gy = gy - 1
        prev_is_leap = _is_gregorian_leap(prev_gy)
        saka_year = gy - 79
        saka_year_start = date(prev_gy, 3, 21 if prev_is_leap else 22)
        chaitra_len = 31 if prev_is_leap else 30

    # Compute days since start of Saka year
    days_since_start = (gregorian_date - saka_year_start).days  # 0-based

    # Month lengths in Saka year starting from Chaitra
    month_lengths = (
        chaitra_len, 31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30
    )

    # Map day offset to month and day
    month = 1
    remaining = days_since_start
    for ml in month_lengths:
        if remaining < ml:
            day = remaining + 1
            break
        remaining -= ml
        month += 1

    # Return as a datetime.date representing the Saka calendar components
    return date(saka_year, month, day)

# Entry point: gregorian_to_saka(gregorian_date: date) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_91_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_saka(gregorian_date):
    result = gregorian_to_saka(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")
