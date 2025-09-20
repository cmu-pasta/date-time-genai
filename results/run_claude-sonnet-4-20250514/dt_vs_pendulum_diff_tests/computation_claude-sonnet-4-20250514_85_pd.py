
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def get_japanese_era_and_year(date: pendulum.Date) -> str:
    # Convert to pendulum.Date if it's a DateTime
    if hasattr(date, 'date'):
        date = date.date()
    
    # Define Japanese era periods with their start dates
    meiji_start = pendulum.date(1868, 10, 23)
    taisho_start = pendulum.date(1912, 7, 30)
    showa_start = pendulum.date(1926, 12, 25)
    heisei_start = pendulum.date(1989, 1, 8)
    reiwa_start = pendulum.date(2019, 5, 1)
    
    # Determine which era the date falls into and calculate the era year
    if date >= reiwa_start:
        # Reiwa era (2019 - present)
        era_year = date.year - reiwa_start.year + 1
        return f"Reiwa {era_year}"
    elif date >= heisei_start:
        # Heisei era (1989 - 2019)
        era_year = date.year - heisei_start.year + 1
        return f"Heisei {era_year}"
    elif date >= showa_start:
        # Showa era (1926 - 1989)
        era_year = date.year - showa_start.year + 1
        return f"Showa {era_year}"
    elif date >= taisho_start:
        # Taisho era (1912 - 1926)
        era_year = date.year - taisho_start.year + 1
        return f"Taisho {era_year}"
    elif date >= meiji_start:
        # Meiji era (1868 - 1912)
        era_year = date.year - meiji_start.year + 1
        return f"Meiji {era_year}"
    else:
        # Before Meiji era
        return f"Pre-Meiji {date.year}"

# Entry point: get_japanese_era_and_year(date: pendulum.Date) -> str

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_85_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_get_japanese_era_and_year(date):
    result = get_japanese_era_and_year(date)
    formatted_result = format_value_pd(result, date)
    log_file.write(formatted_result + "\n")
