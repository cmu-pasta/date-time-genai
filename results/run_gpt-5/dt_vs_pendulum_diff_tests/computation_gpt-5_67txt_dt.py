
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
# Hebrew calendar computations based on classical algorithms (Dershowitz/Reingold style).
# We use "fixed days" compatible with Python's date.toordinal():
# RD (Rata Die) = days since 0001-01-01 Gregorian, where 0001-01-01 has RD = 1.
#
# HEBREW_EPOCH_RD is the RD of the day before 1 Tishri, AM 1, so that:
# RD_of_RoshHashanah(year) = HEBREW_EPOCH_RD + hebrew_new_year_day_index(year)
# and hebrew_new_year_day_index(1) == 1.

HEBREW_EPOCH_RD = -1373427  # Fixed-day reference for Hebrew epoch (consistent with RD system)

def _is_hebrew_leap(year: int) -> bool:
    # Hebrew leap years are years 3, 6, 8, 11, 14, 17, 19 in the 19-year cycle
    return ((year * 7) + 1) % 19 < 7

def _hebrew_new_year_day_index(year: int) -> int:
    """
    Return the number of days elapsed (as an integer index) from the Hebrew epoch baseline
    to Rosh Hashanah (1 Tishri) of the given Hebrew year.
    This uses the molad Tishri and the postponement rules.
    """
    # Months elapsed up to Tishri of 'year' (relative to reference)
    months = ((235 * year) - 234) // 19

    # Parts per day = 25920 (24h * 1080 parts/hour). The constants below are standard.
    parts = 12084 + 13753 * months
    day = 29 * months + (parts // 25920)
    parts = parts % 25920

    # Postponements
    postpone = False
    if parts >= 19440:
        postpone = True
    elif (day % 7) == 2 and parts >= 9924 and not _is_hebrew_leap(year):
        postpone = True
    elif (day % 7) == 1 and parts >= 16789 and _is_hebrew_leap(year - 1):
        postpone = True

    if postpone:
        day += 1

    # Additional postponement: Rosh Hashanah cannot be on Sunday(0), Wednesday(3), Friday(5)
    if day % 7 in (0, 3, 5):
        day += 1

    return day

def _rosh_hashanah_rd(year: int) -> int:
    # RD of Rosh Hashanah (1 Tishri) for given Hebrew year
    return HEBREW_EPOCH_RD + _hebrew_new_year_day_index(year)

def _hebrew_year_length(year: int) -> int:
    return _rosh_hashanah_rd(year + 1) - _rosh_hashanah_rd(year)

def _hebrew_month_length(year: int, month: int) -> int:
    """
    Month numbering:
    1=Tishri, 2=Heshvan, 3=Kislev, 4=Tevet, 5=Shevat,
    6=Adar I (in leap) or Adar (in common), 7=Adar II (in leap only),
    8=Nisan, 9=Iyar, 10=Sivan, 11=Tammuz, 12=Av, 13=Elul
    """
    leap = _is_hebrew_leap(year)
    year_len = _hebrew_year_length(year)

    # Determine Heshvan/Kislev configuration
    # deficient (353 or 383): Heshvan=29, Kislev=29
    # regular  (354 or 384): Heshvan=29, Kislev=30
    # complete (355 or 385): Heshvan=30, Kislev=30
    mod10 = year_len % 10
    if mod10 == 3:
        heshvan = 29
        kislev = 29
    elif mod10 == 4:
        heshvan = 29
        kislev = 30
    else:
        # mod10 == 5
        heshvan = 30
        kislev = 30

    if month == 1:   # Tishri
        return 30
    if month == 2:   # Heshvan
        return heshvan
    if month == 3:   # Kislev
        return kislev
    if month == 4:   # Tevet
        return 29
    if month == 5:   # Shevat
        return 30
    if leap:
        if month == 6:   # Adar I
            return 30
        if month == 7:   # Adar II
            return 29
        if month == 8:   # Nisan
            return 30
        if month == 9:   # Iyar
            return 29
        if month == 10:  # Sivan
            return 30
        if month == 11:  # Tammuz
            return 29
        if month == 12:  # Av
            return 30
        if month == 13:  # Elul
            return 29
    else:
        if month == 6:   # Adar (only one Adar)
            return 29
        if month == 7:   # Nisan
            return 30
        if month == 8:   # Iyar
            return 29
        if month == 9:   # Sivan
            return 30
        if month == 10:  # Tammuz
            return 29
        if month == 11:  # Av
            return 30
        if month == 12:  # Elul
            return 29

    # Should not reach here
    raise ValueError("Invalid Hebrew month computation")

def _last_hebrew_month_of_year(year: int) -> int:
    return 13 if _is_hebrew_leap(year) else 12

def _rd_to_hebrew(rd: int) -> (int, int, int):
    """
    Convert RD (date.toordinal()) to Hebrew (year, month, day).
    Note: Returns a triple but the public interface will encode it as an integer.
    """
    # Initial rough guess to ensure not overshooting
    # Using 366 prevents guessing too high in any case.
    year = (rd - HEBREW_EPOCH_RD) // 366
    if year < 1:
        year = 1

    # Adjust year to bracket the given RD
    while rd >= _rosh_hashanah_rd(year + 1):
        year += 1
    while rd < _rosh_hashanah_rd(year):
        year -= 1

    day_of_year = rd - _rosh_hashanah_rd(year) + 1  # 1-based day within Hebrew year

    # Find month
    month = 1
    last_month = _last_hebrew_month_of_year(year)
    while True:
        dim = _hebrew_month_length(year, month)
        if day_of_year <= dim:
            day = day_of_year
            break
        day_of_year -= dim
        month += 1
        if month > last_month:
            # Safety, shouldn't happen
            month = last_month
            day = max(1, day_of_year)
            break

    return year, month, day

def gregorian_to_hebrew(gregorian_date: date) -> int:
    """
    Convert a Gregorian date (datetime.date) to a Hebrew calendar date encoded as an integer.
    Return format: YYYYMMDD (Hebrew year, Hebrew month [1..13], Hebrew day [1..30]).
    For leap years, month 6 is Adar I and month 7 is Adar II; in common years, month 6 is Adar.
    """
    rd = gregorian_date.toordinal()
    hy, hm, hd = _rd_to_hebrew(rd)
    # Encode as integer YYYYMMDD
    return hy * 10000 + hm * 100 + hd

# Entry point: gregorian_to_hebrew(gregorian_date: date) -> int

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_67txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_hebrew(gregorian_date):
    result = gregorian_to_hebrew(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")
