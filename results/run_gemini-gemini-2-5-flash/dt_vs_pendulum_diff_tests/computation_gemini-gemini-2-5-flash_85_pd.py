
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def get_japanese_era_and_year(gregorian_date: pendulum.DateTime) -> int:
    """
    Determines the Japanese calendar era and year for a given Gregorian date
    and returns them as a single composite integer.

    The composite integer is structured as (era_code * 1000) + era_year.
    Era codes: Meiji=1, Taisho=2, Showa=3, Heisei=4, Reiwa=5.
    Example: Reiwa 5 would be 5005.

    Args:
        gregorian_date: A pendulum.DateTime object representing the Gregorian date.

    Returns:
        An integer representing the composite era code and year.
    """
    # Convert input DateTime to Date for comparison, ignoring time component
    date_to_check = gregorian_date.date()

    # Define era start dates using pendulum.date()
    reiwa_start = pendulum.date(2019, 5, 1)
    heisei_start = pendulum.date(1989, 1, 8)
    showa_start = pendulum.date(1926, 12, 25)
    taisho_start = pendulum.date(1912, 7, 30)
    meiji_start = pendulum.date(1868, 10, 23) # Modern Meiji era starts earlier, but 1868-10-23 is official start of Meiji era under current system.

    era_code = 0
    era_year = 0

    if date_to_check >= reiwa_start:
        era_code = 5 # Reiwa
        era_year = date_to_check.year - reiwa_start.year + 1
    elif date_to_check >= heisei_start:
        era_code = 4 # Heisei
        era_year = date_to_check.year - heisei_start.year + 1
    elif date_to_check >= showa_start:
        era_code = 3 # Showa
        era_year = date_to_check.year - showa_start.year + 1
    elif date_to_check >= taisho_start:
        era_code = 2 # Taisho
        era_year = date_to_check.year - taisho_start.year + 1
    elif date_to_check >= meiji_start:
        era_code = 1 # Meiji
        era_year = date_to_check.year - meiji_start.year + 1
    else:
        # For dates before Meiji era, we'll return 0 for both era and year
        # This could be extended to handle older eras if needed.
        pass
    
    # Return a composite integer: (era_code * 1000) + era_year
    # Assumes era_year will not exceed 999, which is reasonable for practical purposes.
    return era_code * 1000 + era_year

# Entry point: get_japanese_era_and_year(gregorian_date: pendulum.DateTime) -> int

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_85_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_japanese_era_and_year(gregorian_date):
    result = get_japanese_era_and_year(gregorian_date)
    formatted_result = format_value_pd(result, gregorian_date)
    log_file.write(formatted_result + "\n")
