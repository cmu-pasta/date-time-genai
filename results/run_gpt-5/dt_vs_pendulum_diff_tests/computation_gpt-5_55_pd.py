
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def gregorian_to_islamic_date(gregorian_dt: pendulum.DateTime) -> pendulum.Date:
    # Helper: Gregorian date to Julian Day Number (integer JDN)
    def gregorian_to_jdn(y: int, m: int, d: int) -> int:
        a = (14 - m) // 12
        y2 = y + 4800 - a
        m2 = m + 12 * a - 3
        return d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4 - y2 // 100 + y2 // 400 - 32045

    # Helper: is Islamic year leap (tabular/civil calendar)
    def is_islamic_leap(iy: int) -> bool:
        return ((11 * iy + 14) % 30) < 11

    # Helper: Islamic (civil) date to JDN (integer, matching the above JDN convention)
    def islamic_to_jdn(iy: int, im: int, iday: int) -> int:
        # ceil(29.5 * (im - 1)) using integer arithmetic: ceil(29.5*x) = (59*x + 1) // 2
        months_days = (59 * (im - 1) + 1) // 2
        return iday + months_days + (iy - 1) * 354 + ((3 + 11 * iy) // 30) + 1948439

    # Extract Gregorian Y-M-D from the pendulum.DateTime
    gy = gregorian_dt.year
    gm = gregorian_dt.month
    gd = gregorian_dt.day

    # Convert Gregorian date to JDN
    jdn = gregorian_to_jdn(gy, gm, gd)

    # Days since Islamic epoch and Islamic year
    days_since_epoch = jdn - 1948439
    iy = (30 * days_since_epoch + 10646) // 10631

    # JDN of the first day of the computed Islamic year
    jdn_iy1 = islamic_to_jdn(iy, 1, 1)

    # Day index within the Islamic year starting from 0
    day_index = jdn - jdn_iy1

    # Find Islamic month and day by iterating month lengths
    im = 1
    remaining = day_index
    leap = is_islamic_leap(iy)

    while True:
        # Month length: odd months 30, even months 29, except month 12 is 30 in leap years
        if im == 12:
            month_len = 30 if leap else 29
        else:
            month_len = 30 if (im % 2 == 1) else 29

        if remaining < month_len:
            iday = remaining + 1
            break
        remaining -= month_len
        im += 1

    # Return the Islamic date encoded as a pendulum.Date (year=iy, month=im, day=iday)
    return pendulum.date(iy, im, iday)

# Entry point: gregorian_to_islamic_date(gregorian_dt: pendulum.DateTime) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_55_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_gregorian_to_islamic_date(gregorian_dt):
    result = gregorian_to_islamic_date(gregorian_dt)
    formatted_result = format_value_pd(result, gregorian_dt)
    log_file.write(formatted_result + "\n")
