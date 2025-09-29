
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def japanese_era_year(given_date: pendulum.Date) -> pendulum.Duration:
    """
    Determine the Japanese calendar era and year for a given Gregorian date.

    Return encoding (due to output type restrictions):
      - pendulum.Duration.years  = Japanese era year (>= 1)
      - pendulum.Duration.months = Era index:
            1 = Meiji
            2 = Taisho
            3 = Showa
            4 = Heisei
            5 = Reiwa

    Raises:
      ValueError: if the date is before the Meiji era start.
    """

    # Define era start and end dates (inclusive)
    # Sources: Official era boundaries
    MEIJI_START  = pendulum.date(1868, 1, 25)
    TAISHO_START = pendulum.date(1912, 7, 30)
    SHOWA_START  = pendulum.date(1926, 12, 25)
    HEISEI_START = pendulum.date(1989, 1, 8)
    REIWA_START  = pendulum.date(2019, 5, 1)

    MEIJI_END  = TAISHO_START.subtract(days=1)
    TAISHO_END = SHOWA_START.subtract(days=1)
    SHOWA_END  = HEISEI_START.subtract(days=1)
    HEISEI_END = REIWA_START.subtract(days=1)
    REIWA_END  = pendulum.date(9999, 12, 31)  # open-ended

    eras = [
        ("Meiji",  1, MEIJI_START,  MEIJI_END),
        ("Taisho", 2, TAISHO_START, TAISHO_END),
        ("Showa",  3, SHOWA_START,  SHOWA_END),
        ("Heisei", 4, HEISEI_START, HEISEI_END),
        ("Reiwa",  5, REIWA_START,  REIWA_END),
    ]

    # Validate input range
    if given_date < MEIJI_START:
        raise ValueError("Date is before the start of the Meiji era (1868-01-25).")

    # Find the era and compute era year
    for _, era_index, start_date, end_date in eras:
        if start_date <= given_date <= end_date:
            era_year = given_date.year - start_date.year + 1
            # If the given date is before the start date within the same year (shouldn't happen due to range),
            # the adjustment would be handled by the range check above.
            return pendulum.duration(years=era_year, months=era_index)

    # This should be unreachable due to open-ended Reiwa
    raise ValueError("Unable to determine era for the given date.")

# Entry point: japanese_era_year(given_date: pendulum.Date) -> pendulum.Duration

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_85_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_japanese_era_year(given_date):
    result = japanese_era_year(given_date)
    formatted_result = format_value_pd(result, given_date)
    log_file.write(formatted_result + "\n")
