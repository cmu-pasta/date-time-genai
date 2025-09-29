
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_biweekly_periods_in_year(year: int) -> int:
    # Step 1: Get the first day of the year
    start_of_year = pendulum.date(year, 1, 1)

    # Step 2: Get the last day of the year
    # Using 'year + 1' and 'subtract(days=1)' ensures we handle leap years correctly
    end_of_year = pendulum.date(year + 1, 1, 1).subtract(days=1)

    # Step 3: Calculate the total number of days in the year.
    # We add 1 because diff calculates the difference *between* dates.
    # For example, Jan 1 to Jan 1 is 0 days, but it's 1 day inclusive.
    # Alternatively, we can use the `day_of_year` for the last day, which correctly gives 365 or 366.
    total_days_in_year = end_of_year.day_of_year

    # Step 4: A bi-weekly period is 14 days.
    # Calculate the number of full bi-weekly periods using floor division.
    number_of_periods = total_days_in_year // 14
    
    return number_of_periods

# Entry point: calculate_biweekly_periods_in_year(year: int) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_72_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_calculate_biweekly_periods_in_year(year):
    result = calculate_biweekly_periods_in_year(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
