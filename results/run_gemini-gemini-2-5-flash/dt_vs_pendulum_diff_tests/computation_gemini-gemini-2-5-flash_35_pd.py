
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_last_business_day_of_month(date_in_month: pendulum.DateTime) -> pendulum.Date:
    # Step 1: Get the last day of the month
    current_day = date_in_month.end_of_month().date()

    # Step 2: Iterate backwards until a business day is found
    # A business day is Monday (0) to Friday (4). Weekend days are Saturday (5) and Sunday (6).
    while current_day.weekday() >= 5:  # Check if it's Saturday or Sunday
        current_day = current_day.subtract(days=1)
    
    # Step 3: Return the last business day
    return current_day

# Entry point: find_last_business_day_of_month(date_in_month: pendulum.DateTime) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_35_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_last_business_day_of_month(date_in_month):
    result = find_last_business_day_of_month(date_in_month)
    formatted_result = format_value_pd(result, date_in_month)
    log_file.write(formatted_result + "\n")
