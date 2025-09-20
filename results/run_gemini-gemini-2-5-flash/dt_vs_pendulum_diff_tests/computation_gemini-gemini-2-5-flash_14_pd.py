
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_date_n_business_days_after(start_date: pendulum.DateTime, n: int) -> pendulum.DateTime:
    """
    Finds the date that is exactly N business days after a given date.

    Args:
        start_date (pendulum.DateTime): The starting date.
        n (int): The number of business days to add. Must be non-negative.

    Returns:
        pendulum.DateTime: The date N business days after the start_date.
    """
    if n < 0:
        raise ValueError("The number of business days (n) must be non-negative.")

    # Initialize current_date to the start_date for iteration
    current_date = start_date
    business_days_counted = 0

    # If n is 0, we still need to make sure the start_date itself is considered
    # if it's a business day, or find the next business day if it's not.
    # The logic below handles this by checking the current_date, then advancing.
    # To correctly implement "N business days *after*", we usually start counting
    # from the day following the start_date.
    # However, if N=0, it usually implies the start date itself if it's a business day,
    # or the next business day if the start date is a weekend.

    # Let's adjust the current_date to the next day if N > 0, or handle N=0.
    if n == 0:
        # If 0 business days, return the start_date if it's a business day,
        # otherwise find the first business day on or after start_date.
        while current_date.is_weekend():
            current_date = current_date.add(days=1)
        return current_date

    # If n > 0, we start checking from the day *after* the start_date
    current_date = current_date.add(days=1)

    while business_days_counted < n:
        if not current_date.is_weekend():
            business_days_counted += 1
        
        if business_days_counted < n: # Only advance if more business days are needed
            current_date = current_date.add(days=1)

    return current_date

# Entry point: find_date_n_business_days_after(start_date: pendulum.DateTime, n: int) -> pendulum.DateTime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_14_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timestamp_strategy())
def test_find_date_n_business_days_after(start_date, n):
    result = find_date_n_business_days_after(start_date, n)
    formatted_result = format_value_pd(result, start_date, n)
    log_file.write(formatted_result + "\n")
