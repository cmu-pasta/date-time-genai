
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def determine_japanese_year(gregorian_date: datetime) -> int:
    """
    Determines the Japanese calendar year for a given Gregorian date.
    Note: Due to output type constraints (no strings, no complex types),
    this function returns only the Japanese year as an integer.
    The Japanese era name cannot be returned as per the problem's strict output constraints.
    """

    # Define the start dates for major modern Japanese eras (Gregorian calendar)
    # Stored as datetime objects for direct comparison
    reiwa_start = datetime(2019, 5, 1)
    heisei_start = datetime(1989, 1, 8)
    showa_start = datetime(1926, 12, 25)
    taisho_start = datetime(1912, 7, 30)
    meiji_start = datetime(1868, 9, 8)

    # Determine the current era and calculate the Japanese year
    if gregorian_date >= reiwa_start:
        # It's the Reiwa era
        japanese_year = gregorian_date.year - reiwa_start.year + 1
        if gregorian_date.month < reiwa_start.month or \
           (gregorian_date.month == reiwa_start.month and gregorian_date.day < reiwa_start.day):
            # If the date is in the same Gregorian year but before the era started, it's the previous era's year
            # This logic branch is technically for dates *after* the start,
            # so this condition should not apply if gregorian_date >= reiwa_start
            # However, for consistency and robustness in year calculation:
            pass # The year difference already handles this correctly. Reiwa 1 starts May 1, 2019.
                 # If gregorian_date is e.g., 2019-06-01, then 2019 - 2019 + 1 = 1.
                 # If gregorian_date is e.g., 2020-01-01, then 2020 - 2019 + 1 = 2.
    elif gregorian_date >= heisei_start:
        # It's the Heisei era
        japanese_year = gregorian_date.year - heisei_start.year + 1
        if gregorian_date.month < heisei_start.month or \
           (gregorian_date.month == heisei_start.month and gregorian_date.day < heisei_start.day):
            japanese_year -= 1 # Adjust if the date is earlier in the same Gregorian year than era start
    elif gregorian_date >= showa_start:
        # It's the Showa era
        japanese_year = gregorian_date.year - showa_start.year + 1
        if gregorian_date.month < showa_start.month or \
           (gregorian_date.month == showa_start.month and gregorian_date.day < showa_start.day):
            japanese_year -= 1
    elif gregorian_date >= taisho_start:
        # It's the Taisho era
        japanese_year = gregorian_date.year - taisho_start.year + 1
        if gregorian_date.month < taisho_start.month or \
           (gregorian_date.month == taisho_start.month and gregorian_date.day < taisho_start.day):
            japanese_year -= 1
    elif gregorian_date >= meiji_start:
        # It's the Meiji era
        japanese_year = gregorian_date.year - meiji_start.year + 1
        if gregorian_date.month < meiji_start.month or \
           (gregorian_date.month == meiji_start.month and gregorian_date.day < meiji_start.day):
            japanese_year -= 1
    else:
        # Date is before Meiji era or unsupported
        # Return a value indicating an error or 'not applicable', e.g., -1
        # or raise an error. For this problem, returning -1 as an integer is compliant.
        japanese_year = -1 
        
    return japanese_year

# Entry point: determine_japanese_year(gregorian_date: datetime) -> int

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_85_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_determine_japanese_year(gregorian_date):
    result = determine_japanese_year(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")
