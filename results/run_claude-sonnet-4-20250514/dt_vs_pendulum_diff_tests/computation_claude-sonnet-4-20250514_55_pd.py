
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def gregorian_to_islamic(gregorian_date: pendulum.Date) -> pendulum.Date:
    # Step 1: Convert Gregorian date to Julian Day Number
    # Using Pendulum's built-in Julian day calculation
    julian_day = gregorian_date.to_date_string()
    
    # Manual conversion using the standard algorithm
    year = gregorian_date.year
    month = gregorian_date.month
    day = gregorian_date.day
    
    # Calculate Julian Day Number
    if month <= 2:
        year -= 1
        month += 12
    
    a = year // 100
    b = 2 - a + (a // 4)
    
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524
    
    # Step 2: Convert Julian Day to Islamic date
    # Islamic epoch is July 16, 622 CE (Julian Day 1948441)
    islamic_epoch = 1948441
    days_since_epoch = jd - islamic_epoch
    
    # Islamic year calculation (approximately 354.367 days per Islamic year)
    islamic_year = int(days_since_epoch / 354.367) + 1
    
    # Calculate remaining days for month and day
    days_in_islamic_year = days_since_epoch - int((islamic_year - 1) * 354.367)
    
    # Approximate Islamic month (29.53 days per month on average)
    islamic_month = min(12, max(1, int(days_in_islamic_year / 29.53) + 1))
    
    # Calculate Islamic day
    days_in_months = int((islamic_month - 1) * 29.53)
    islamic_day = max(1, min(30, int(days_in_islamic_year - days_in_months) + 1))
    
    # Step 3: Return as pendulum.Date (values represent Islamic date)
    # Note: This creates a Gregorian date object with Islamic date values
    return pendulum.Date(islamic_year, islamic_month, islamic_day)

# Entry point: gregorian_to_islamic(gregorian_date: pendulum.Date) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_55_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_islamic(gregorian_date):
    result = gregorian_to_islamic(gregorian_date)
    formatted_result = format_value_pd(result, gregorian_date)
    log_file.write(formatted_result + "\n")
