
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_work_weeks(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int:
    # Ensure dt_start is the earlier date and dt_end is the later date
    dt_start = min(dt1, dt2).start_of("day")
    dt_end = max(dt1, dt2).start_of("day")

    business_days_count = 0
    current_date = dt_start

    # Iterate through each day from start to end (inclusive)
    while current_date <= dt_end:
        # Check if the current day is a weekday (Monday=0 to Friday=4)
        if current_date.weekday() < pendulum.SATURDAY:
            business_days_count += 1
        current_date = current_date.add(days=1)
    
    # Calculate the number of full work weeks (5 business days per week)
    number_of_work_weeks = business_days_count // 5
    
    return number_of_work_weeks

# Entry point: calculate_work_weeks(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_57_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_work_weeks(dt1, dt2):
    result = calculate_work_weeks(dt1, dt2)
    formatted_result = format_value_pd(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
