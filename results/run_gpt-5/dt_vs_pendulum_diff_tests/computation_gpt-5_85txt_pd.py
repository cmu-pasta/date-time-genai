
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def japanese_era_code_year(dt: pendulum.DateTime) -> int:
    """
    Determine the Japanese calendar era and year for a given Gregorian date.

    Encoding rule:
      - Return era_code * 10000 + era_year
      - era_code mapping:
          1 = Meiji (from 1868-01-25 to 1912-07-29)
          2 = Taisho (from 1912-07-30 to 1926-12-24)
          3 = Showa (from 1926-12-25 to 1989-01-07)
          4 = Heisei (from 1989-01-08 to 2019-04-30)
          5 = Reiwa (from 2019-05-01 onward)
      - Return 0 if the date precedes Meiji.

    Input: pendulum.DateTime
    Output: integer (encoded era and era year)
    """
    d = dt.date()

    # Era boundaries (inclusive)
    meiji_start = pendulum.date(1868, 1, 25)
    meiji_end   = pendulum.date(1912, 7, 29)

    taisho_start = pendulum.date(1912, 7, 30)
    taisho_end   = pendulum.date(1926, 12, 24)

    showa_start = pendulum.date(1926, 12, 25)
    showa_end   = pendulum.date(1989, 1, 7)

    heisei_start = pendulum.date(1989, 1, 8)
    heisei_end   = pendulum.date(2019, 4, 30)

    reiwa_start = pendulum.date(2019, 5, 1)
    # Reiwa has no defined end yet.

    # Determine era and compute encoded result
    if d >= reiwa_start:
        era_code = 5
        era_year = d.year - reiwa_start.year + 1
        return era_code * 10000 + era_year

    if heisei_start <= d <= heisei_end:
        era_code = 4
        era_year = d.year - heisei_start.year + 1
        return era_code * 10000 + era_year

    if showa_start <= d <= showa_end:
        era_code = 3
        era_year = d.year - showa_start.year + 1
        return era_code * 10000 + era_year

    if taisho_start <= d <= taisho_end:
        era_code = 2
        era_year = d.year - taisho_start.year + 1
        return era_code * 10000 + era_year

    if meiji_start <= d <= meiji_end:
        era_code = 1
        era_year = d.year - meiji_start.year + 1
        return era_code * 10000 + era_year

    # Date is earlier than Meiji start (unsupported)
    return 0

# Entry point: japanese_era_code_year(dt: pendulum.DateTime) -> int

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_85txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_japanese_era_code_year(dt):
    result = japanese_era_code_year(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
