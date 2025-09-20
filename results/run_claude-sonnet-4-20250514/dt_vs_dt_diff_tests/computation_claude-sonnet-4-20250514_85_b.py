
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def get_japanese_year(gregorian_date: datetime) -> int:
    # Define the start dates of Japanese eras
    meiji_start = datetime(1868, 9, 8)
    taisho_start = datetime(1912, 7, 30)
    showa_start = datetime(1926, 12, 25)
    heisei_start = datetime(1989, 1, 8)
    reiwa_start = datetime(2019, 5, 1)
    
    # Determine which era the date falls into and calculate the Japanese year
    if gregorian_date >= reiwa_start:
        # Reiwa era
        japanese_year = (gregorian_date.year - reiwa_start.year) + 1
        if gregorian_date.month < reiwa_start.month or (gregorian_date.month == reiwa_start.month and gregorian_date.day < reiwa_start.day):
            japanese_year -= 1
    elif gregorian_date >= heisei_start:
        # Heisei era
        japanese_year = (gregorian_date.year - heisei_start.year) + 1
        if gregorian_date.month < heisei_start.month or (gregorian_date.month == heisei_start.month and gregorian_date.day < heisei_start.day):
            japanese_year -= 1
    elif gregorian_date >= showa_start:
        # Showa era
        japanese_year = (gregorian_date.year - showa_start.year) + 1
        if gregorian_date.month < showa_start.month or (gregorian_date.month == showa_start.month and gregorian_date.day < showa_start.day):
            japanese_year -= 1
    elif gregorian_date >= taisho_start:
        # Taisho era
        japanese_year = (gregorian_date.year - taisho_start.year) + 1
        if gregorian_date.month < taisho_start.month or (gregorian_date.month == taisho_start.month and gregorian_date.day < taisho_start.day):
            japanese_year -= 1
    elif gregorian_date >= meiji_start:
        # Meiji era
        japanese_year = (gregorian_date.year - meiji_start.year) + 1
        if gregorian_date.month < meiji_start.month or (gregorian_date.month == meiji_start.month and gregorian_date.day < meiji_start.day):
            japanese_year -= 1
    else:
        # Before Meiji era - return 0 to indicate unsupported date
        japanese_year = 0
    
    return japanese_year

# Entry point: get_japanese_year(gregorian_date: datetime) -> int

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_85_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_japanese_year(gregorian_date):
    result = get_japanese_year(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")
