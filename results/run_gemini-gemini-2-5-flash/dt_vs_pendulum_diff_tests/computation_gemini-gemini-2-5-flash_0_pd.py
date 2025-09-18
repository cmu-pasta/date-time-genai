
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_business_days_between(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int:
    # Step 1 & 2: Determine the start and end dates to ensure correct iteration
    if dt1 <= dt2:
        start_date = dt1
        end_date = dt2
    else:
        start_date = dt2
        end_date = dt1
    
    business_days_count = 0
    
    # Step 3: Iterate through each day in the period from start_date to end_date (exclusive of end_date)
    # pendulum.period(start, end) iterates from 'start' up to, but not including, 'end'.
    # For example, between Monday and Wednesday, it iterates Monday and Tuesday.
    # If the user means to include the 'end_date' if it's a business day, then the iteration needs adjustment.
    # As per typical "between" calculations, we iterate the days *strictly between* the two endpoints.
    # If the problem implies an inclusive range for days, then we might need to adjust end_date by +1 day,
    # or iterate 'start_date' to 'end_date' inclusive.
    # Given the previous example calculated difference, it typically refers to the number of full days *between*
    # or the count of specific days in the interval [start_date, end_date).
    # Let's interpret "between two dates" as the days in the interval [start_date, end_date).
    
    for day in pendulum.period(start_date.start_of('day'), end_date.start_of('day')):
        # Step 4: Check if the current day is a weekday (Monday to Friday)
        if day.is_weekday():
            business_days_count += 1
            
    return business_days_count

# Entry point: calculate_business_days_between(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_0_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_business_days_between(dt1, dt2):
    result = calculate_business_days_between(dt1, dt2)
    formatted_result = format_value_pd(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
