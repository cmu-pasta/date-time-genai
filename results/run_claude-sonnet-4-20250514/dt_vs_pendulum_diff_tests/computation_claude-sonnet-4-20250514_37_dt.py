
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def determine_zodiac_sign(birth_date: datetime) -> int:
    # Extract month and day from the datetime object
    month = birth_date.month
    day = birth_date.day
    
    # Determine zodiac sign based on month and day
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return 1  # Aries
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return 2  # Taurus
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return 3  # Gemini
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return 4  # Cancer
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return 5  # Leo
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return 6  # Virgo
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return 7  # Libra
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return 8  # Scorpio
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return 9  # Sagittarius
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return 10  # Capricorn
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return 11  # Aquarius
    else:  # (month == 2 and day >= 19) or (month == 3 and day <= 20)
        return 12  # Pisces

# Entry point: determine_zodiac_sign(birth_date: datetime) -> int

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_37_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_determine_zodiac_sign(birth_date):
    result = determine_zodiac_sign(birth_date)
    formatted_result = format_value_dt(result, birth_date)
    log_file.write(formatted_result + "\n")
