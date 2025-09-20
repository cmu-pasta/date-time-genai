
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def gregorian_is_leap(year: int) -> bool:
    # Gregorian leap year rules
    if year % 4 != 0:
        return False
    if year % 100 != 0:
        return True
    return year % 400 == 0

def gregorian_to_indian_national(greg_date: date) -> date:
    # Step 1: Determine Chaitra 1 for the relevant Gregorian year
    gy = greg_date.year
    is_leap_current = gregorian_is_leap(gy)
    chaitra1_current = date(gy, 3, 21 if is_leap_current else 22)

    if greg_date >= chaitra1_current:
        # Date falls in Saka year that starts this Gregorian year
        saka_year = gy - 78
        start_year_for_saka = gy
        start_date = chaitra1_current
        chaitra_len = 31 if is_leap_current else 30
    else:
        # Date falls in Saka year that started in previous Gregorian year
        prev_year = gy - 1
        is_leap_prev = gregorian_is_leap(prev_year)
        start_year_for_saka = prev_year
        start_date = date(prev_year, 3, 21 if is_leap_prev else 22)
        saka_year = gy - 79
        chaitra_len = 31 if is_leap_prev else 30

    # Step 2: Compute days since Chaitra 1
    days_since = (greg_date - start_date).days  # 0-based offset

    # Step 3: Define Saka month lengths for this Saka year
    # Months: Chaitra, Vaisakha, Jyaistha, Asadha, Sravana, Bhadra, Asvina, Kartika, Agrahayana, Pausha, Magha, Phalguna
    month_lengths = (
        chaitra_len, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 30
    )

    # Step 4: Find Saka month and day
    month = 1
    remaining = days_since
    for ml in month_lengths:
        if remaining < ml:
            day = remaining + 1
            break
        remaining -= ml
        month += 1

    # Step 5: Return a date object representing the Saka calendar date (year, month, day)
    # Note: This date object encodes the Saka year-month-day, not a Gregorian date.
    return date(saka_year, month, day)

# Entry point: gregorian_to_indian_national(greg_date: date) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_91_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_indian_national(greg_date):
    result = gregorian_to_indian_national(greg_date)
    formatted_result = format_value_dt(result, greg_date)
    log_file.write(formatted_result + "\n")
