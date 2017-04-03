"""
Support for astronomical date/time calculations.

A date or date time is represented as a tuple of the form (year, month, day[, hours, minutes, seconds[, mode]])
where the time is optional or the mode is optional.

Example 1:
(1980, 4, 22, 19, 36, 51.67, 'lct') represents the Local Civil Time of 19:36:51.67 on date April 22, 1980.

Example 2:
(1980, 4, 22) represents the date April 22, 1980.
Due to the lack of a time in this date time it cannot be used in a time conversion.

Example 3:
(1980, 4, 22, 19, 36, 51.67) represents the time of 19:36:51.67 on date April 22, 1980.
Due to the ambiguous nature of this date time it cannot be used in a time conversion.
"""

import time
import deltat
from mathutils import *

DAYS_OF_WEEK = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
LENGTH_OF_MONTH = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
TIME_MODE_LCT = u"lct"
TIME_MODE_UT = u"ut"
TIME_MODE_TD = u"td"
TIME_MODE_LST = u"lst"
TIME_MODE_GST = u"gst"
TIME_MODES = [TIME_MODE_LCT, TIME_MODE_UT, TIME_MODE_TD, TIME_MODE_GST, TIME_MODE_LST]
DAYLIGHT_SAVINGS = True
ZONE_CORRECTION = 0     # - for west, + for east
LONGITUDE = 0           # - for west, + for east
LATITUDE = 0            # + for north, - for south
DATETIME_PRINT_FORMAT = '%b %d, %Y %H:%M:%S'
TIME_SECONDS_PRECISION = 2

def _convert_date_time(res):
    """
    Convert the response array (usually from keyboard input) into a date time tuple.

    :param res: the response to convert
    :return:    an unvalidated date time tuple
    """
    dat = []
    i = 0
    while (i < len(res)) and (i < 7):
        if i < 5:
            dat.append(int(res[i]))
        elif i == 5:
            dat.append(fix(res[i], TIME_SECONDS_PRECISION))
        else:
            dat.append(res[i])
        i += 1
    return dat

def add_days(dat, dd):
    """
    Add the day delta to the date.

    :param dat: date tuple to adjust (year, month, day[, hours, mins, secs[, mode]])
    :param dd:  day delta
    :return:    adjusted date tuple (year, month, day[, hours, mins, secs[, mode]])
    """
    if validate_date(dat, require_time=False):
        ldat = len(dat)
        j = to_julian_from_date_tuple(dat)
        dat = to_date_tuple_from_julian(j + dd)
        return dat[0:ldat]
    raise ValueError, "Invalid date!"

def add_months(dat, dm):
    """
    Add the month delta to the date.

    :param dat: date tuple to adjust (year, month, day[, hours, mins, secs[, mode]])
    :param dm:  month delta
    :return:    adjusted date tuple (year, month, day[, hours, mins, secs[, mode]])
    """
    if validate_date(dat, require_time=False):
        m = dat[1] + dm
        dy = 0
        while m < 1:
            dy -= 1
            m += 12
        while m > 12:
            dy += 1
            m -= 12
        dat[1] = m
        return add_years(dat, dy)
    raise ValueError, "Invalid date!"

def add_years(dat, dy):
    """
    Add the year delta to the date.

    :param dat: date tuple to adjust (year, month, day[, hours, mins, secs[, mode]])
    :param dy:  year delta
    :return:    adjusted date tuple (year, month, day[, hours, mins, secs[, mode]])
    """
    if validate_date(dat, require_time=False):
        dat[0] += dy
    raise ValueError, "Invalid date!"

def get_date_of_easter(year):
    """
    Calculate the date of Easter.

    :param year: year for which to calculate the date of Easter
    :return:    date tuple for Easter (None if not a valid year)(year, month, day)
    """
    if (year is not None) and (year >= 1583):
        a = int(year % 19)
        b = int(year / 100)
        c = int(year % 100)
        d = int(b / 4)
        e = int(b % 4)
        f = int((b + 8) / 25)
        g = int((b - f + 1) / 3)
        h = int(((19 * a) + b - d - g + 15) % 30)
        i = int(c / 4)
        k = int(c % 4)
        l = int((32 + (2 * e) + (2 * i) - h - k ) % 7)
        m = int((a + (11 * h) + (22 * l) ) / 451)
        t = int((h + l - (7 * m) + 114))
        n = int(t / 31)
        p = int((t % 31) + 1)
        return year, n, p
    return None

def get_days_in_month(dat):
    """
    Determine the number of days in the specified month.

    :param dat: date tuple (year, month, day[, hours, mins, secs[, mode]])
    :return:    number of days in the month (0=error)
    """
    d = 0
    if validate_date(dat, require_time=False):
        d = LENGTH_OF_MONTH[dat[1]]
        if (dat[1] == 2) and is_leap_year(dat[0]):
            d += 1
        return d
    raise ValueError, "Invalid date!"

def is_leap_year(year):
    """
    Determine if the specified year is a leap year.

    :param year:    the year to test
    :return:    True or False
    """
    if year is not None:
        year = int(year)
        if (year % 100) == 0:
            return (year % 400) == 0
        return (year % 4) == 0
    raise ValueError, "Invalid year!"

def now():
    """
    Get a date tuple of the current date and time.

    :return:    date tuple with the current date and time (year, month, day, hours, minutes, seconds, mode)
    """
    current = time.time()
    dat = time.gmtime(current)
#   dat = (year, month, day, hour, min, sec, weekday, julian day, daylight savings flag)
    return dat[0], dat[1], dat[2], dat[3], dat[4], fix(dat[5], TIME_SECONDS_PRECISION), 'ut'

def set_daylight_savings(daylight_savings):
    """
    Set the daylight savings to be used in date calculations.

    :param daylight_savings: True=daylight savings
    """
    global DAYLIGHT_SAVINGS
    if daylight_savings is not None:
        DAYLIGHT_SAVINGS = daylight_savings

def set_latitude(latitude):
    """
    Set the latitude to be used in date calculations.

    :param latitude:    the latitude to set (- for west, + for east)
    """
    global LATITUDE
    if latitude is not None:
        latitude = to_float(latitude)
        latitude = normalize_degrees(latitude, 90.0)
        LATITUDE = latitude

def set_longitude(longitude):
    """
    Set the longitude to be used in date calculations.

    :param longitude:   the longitude to set (- for west, + for east)
    """
    global LONGITUDE
    if longitude is not None:
        longitude = to_float(longitude)
        longitude = normalize_degrees(longitude)
        LONGITUDE = longitude

def set_zone_correction(zc):
    """
    Set the time zone correction to be used in date calculations.

    :param zc:  the time zone correction to set (- for west, + for east)
    """
    global ZONE_CORRECTION
    if zc is not None:
        zc = to_int(zc)
        if zc < -24:
            zc = -24
        elif zc > 24:
            zc = 24
        ZONE_CORRECTION = zc

def to_pretty_date(dat, format=DATETIME_PRINT_FORMAT):
    """
    Convert the date tuple to a formatted date.

    :param dat: the date tuple to use
    :return:    the formatted date string (or None if error)
    """
    s = ""
    if validate_date(dat):
        t = (int(dat[0]), int(dat[1]), int(dat[2]), int(dat[3]), int(dat[4]), int(dat[5]), 0, 0, 0)
        s = time.strftime(format, t)
        if len(dat) > 6:
            s += ' ' + dat[6].upper()
    return s

def to_date_tuple_from_julian(jul, mode=TIME_MODE_UT):
    """
    Converts a julian day to a date tuple.

    :param jul:     julian
    :param mode:    time mode (default: 'ut')
    :return:        date tuple (year, month, day, hours, minutes, seconds, mode)
    """
    if jul is not None:
        jd = 0.5 + jul
        I = int(jd)
        F = jd - I
        if I > 2229160:
            A = int((I - 1867216.25) / 36524.25)
            B = I + 1 + A - int(A / 4.0)
        else:
            B = I
        C = B + 1524
        D = int((C - 122.1) / 365.25)
        E = int(365.25 * D)
        G = int((C - E) / 30.6001)
        d = C - E + F - int(30.6001 * G)
        if G < 13.5:
            month = G - 1
        else:
            month = G - 13
        if month > 2.5:
            year = D - 4716
        else:
            year = D - 4715
        day = int(d)
        h = (d - day) * 24
        hour, minute, sec = to_time_tuple_from_hours(h)
        return year, month, day, hour, minute, sec, mode
    raise ValueError, "Invalid julian date!"

def to_day_of_week_from_julian(jul):
    """
    Converts a julian to day of the week.

    :param jul: julian
    :return:    day of week
    """
    global DAYS_OF_WEEK
    if jul is not None:
        a = (jul + 1.5) / 7.0
        day = int(round((a - int(a)) * 7.0))
        return day - 1
    raise ValueError, "Invalid julian date!"

def to_gst(dat):
    """
    Converts to greenwich sidereal time.

    :param dat: the date time tuple to use
    :return:    the converted date time tuple (None if error)
    """
    global LONGITUDE
    if validate_date(dat):
        if (dat[6] == TIME_MODE_TD) or (dat[6] == TIME_MODE_LCT):
            dat = to_ut(dat)
        if dat[6] == TIME_MODE_UT:
            j = to_julian_from_date_tuple(dat[0:3])
            S = j - 2451545.0
            T = S / 36525.0
            T0 = 6.69737455833 + (T * (2400.0513369 + (T * 0.00002586222 + (T * 0.00000000172))))
            while T0 >= 24.0:
                T0 -= 24.0
            while T0 < 0.0:
                T0 += 24.0
            t = to_hours_from_time_tuple(dat[3:6])
            t *= 1.002737909
            t += T0
            if t >= 24.0:
                t -= 24.0
            tim = to_time_tuple_from_hours(t)
            dat = dat[0], dat[1], dat[2], tim[0], tim[1], tim[2], TIME_MODE_GST
        if dat[6] == TIME_MODE_LST:
            t = to_hours_from_time_tuple(dat[3:6])
            t -= LONGITUDE / 15.0
            if t >= 24.0:
                t -= 24.0
            elif t < 0.0:
                t += 24.0
            tim = to_time_tuple_from_hours(t)
            dat = dat[0], dat[1], dat[2], tim[0], tim[1], tim[2], TIME_MODE_GST
        return dat
    raise ValueError, "Invalid date!"

def to_hours_from_time_tuple(tim):
    """
    Converts a time tuple to decimal hours.

    :param tim: time tuple (hours, mins, secs)
    :return:    dhours
    """
    if validate_time(tim):
        hour, min, sec = tim
        if hour < 0:
            mult = -1
        else:
            mult = 1
        return mult * (abs(hour) + ((fix(sec, TIME_SECONDS_PRECISION) / 60.0) + min) / 60.0)
    raise ValueError, "Invalid time!"

def to_julian_from_date_tuple(dat):
    """
    Converts a date tuple to julian day.

    :param dat: date tuple (year, month, day[, hours, mins, secs[, mode]])
    :return:    julian
    """
    if validate_date(dat, require_time=False):
        if len(dat) == 7:
            year, month, day, hour, min, sec, mode = dat
        elif len(dat) == 6:
            year, month, day, hour, min, sec = dat
        elif len(dat) == 3:
            year, month, day = dat
            hour, min, sec = 0, 0, 0
    else:
        raise ValueError, "Invalid date!"
    if month <= 2:
        year -= 1
        month += 12
    if year >= 1582:
        A = year / 100
        B = 2 - A + (A / 4)
    else:
        B = 0
    if year < 0:
        C = int((365.25 * year) - 0.75)
    else:
        C = int(365.25 * year)
    D = int(30.6001 * (month + 1))
    return 1720994.5 + B + C + D + day + ((((fix(sec, TIME_SECONDS_PRECISION) / 60.0) + float(min)) / 60.0) + float(hour)) / 24.0

def to_lct(dat):
    """
    Converts to local civil time.

    :param dat: the date time tuple to use
    :return:    the converted date time tuple
    """
    global DAYLIGHT_SAVINGS, ZONE_CORRECTION
    if validate_date(dat):
        if (dat[6] == TIME_MODE_TD) or (dat[6] == TIME_MODE_LST) or (dat[6] == TIME_MODE_GST):
            dat = to_ut(dat)
        if dat[6] == TIME_MODE_UT:
            t = to_hours_from_time_tuple(dat[3:6])
            t += ZONE_CORRECTION
            if DAYLIGHT_SAVINGS:
                t += 1
            if t >= 24.0:
                t -= 24.0
                dat = add_days(dat, 1)
            elif t < 0.0:
                t += 24.0
                dat = add_days(dat, -1)
            tim = to_time_tuple_from_hours(t)
            dat = dat[0], dat[1], dat[2], tim[0], tim[1], tim[2], TIME_MODE_LCT
        return dat
    raise ValueError, "Invalid date!"

def to_lst(dat):
    """
    Converts to local sidereal time.

    :param dat: the date time tuple to use
    :return:    the converted date time tuple
    """
    global LONGITUDE
    if validate_date(dat):
        if dat[6] == TIME_MODE_TD:
            dat = to_ut(dat)
        if (dat[6] == TIME_MODE_LCT) or (dat[6] == TIME_MODE_UT):
            dat = to_gst(dat)
        if dat[6] == TIME_MODE_GST:
            t = to_hours_from_time_tuple(dat[3:6])
            t += LONGITUDE / 15.0
            if t >= 24.0:
                t -= 24.0
            elif t < 0.0:
                t += 24.0
            tim = to_time_tuple_from_hours(t)
            dat = dat[0], dat[1], dat[2], tim[0], tim[1], tim[2], TIME_MODE_LST
        return dat
    raise ValueError, "Invalid date!"

def to_td(dat):
    """
    Converts to dynamical time.

    :param dat: the date time tuple to use
    :return:    the converted date time tuple
    """
    if validate_date(dat):
        if dat[6] != TIME_MODE_TD:
            dat = to_ut(dat)
            dt = deltat.calc_dt_interp(dat) / 86400.0
            td_j = to_julian_from_date_tuple(dat) + dt
            dat = to_date_tuple_from_julian(td_j, TIME_MODE_TD)
        return dat
    raise ValueError, "Invalid date!"

def to_time_tuple_from_hours(dhours):
    """
    Converts decimal hours to a time tuple.

    :param dhours:  decimal hours to convert
    :return:        time tuple (hours, mins, secs)
    """
    if dhours is not None:
        hour = int(dhours)
        dmins = abs(dhours - hour) * 60
        min = int(dmins + 0.0005)    # add a tiny amount to make sure the minutes round properly
        sec = (dmins - min) * 60
        return hour, min, fix(sec, TIME_SECONDS_PRECISION)
    raise ValueError, "Invalid decimal hours!"

def to_ut(dat):
    """
    Converts to universal time.

    :param dat: the date time tuple to use
    :return:    the converted date time tuple
    """
    global DAYLIGHT_SAVINGS, ZONE_CORRECTION
    if validate_date(dat):
        if dat[6] == TIME_MODE_LCT:
            t = to_hours_from_time_tuple(dat[3:6])
            if DAYLIGHT_SAVINGS:
                t -= 1
            t -= ZONE_CORRECTION
            if t >= 24.0:
                t -= 24.0
                dat = add_days(dat, 1)
            elif t < 0.0:
                t += 24.0
                dat = add_days(dat, -1)
            tim = to_time_tuple_from_hours(t)
            dat = dat[0], dat[1], dat[2], tim[0], tim[1], tim[2], TIME_MODE_UT
        if dat[6] == TIME_MODE_LST:
            dat = to_gst(dat)
        if dat[6] == TIME_MODE_GST:
            j = to_julian_from_date_tuple(dat)
            j -= (j - int(j)) - 0.5
            S = float(j) - 2451545.0
            T = float(S) / 36525.0
            T0 = 6.697374558 + (T * (2400.051336 + (0.000025862 * T)))
            while T0 >= 24.0:
                T0 -= 24.0
            while T0 < 0.0:
                T0 += 24.0
            t = to_hours_from_time_tuple(dat[3:6])
            t -= T0
            while t < 0.0:
                t += 24.0
            t *= 0.9972695663
            tim = to_time_tuple_from_hours(t)
            dat = dat[0], dat[1], dat[2], tim[0], tim[1], tim[2], TIME_MODE_UT
        if dat[6] == TIME_MODE_TD:
            t = deltat.calc_dt_interp(dat) / 86400.0
            j = to_julian_from_date_tuple(dat)
            dat = to_date_tuple_from_julian(j - t, TIME_MODE_UT)
        return dat
    raise ValueError, "Invalid date!"

def validate_date(dat, require_time=True):
    """
    Validate a date or date time tuple.

    :param dat:         the date tuple to validate
    :return:            True=valid, False=invalid
    """
    global LENGTH_OF_MONTH
    if (dat is not None) and (len(dat) >= 3):
        yr = to_int(dat[0])
        mth = to_int(dat[1])
        day = to_int(dat[2])
        if not validate_month(mth):
            return False
        if is_leap_year(yr) and (mth == 2):
            if day > 29:
                return False
        elif day > LENGTH_OF_MONTH[mth]:
            return False
        if len(dat) > 3:
            if not validate_time(dat[3:]):
                return False
        elif require_time:
            return False
        return True
    return False

def validate_month(month):
    """
    Validate a month.

    :param month:   the month to validate
    :return:        True=valid, False=invalid
    """
    if month is not None:
        month = to_int(month)
        if month < 1:
            return False
        if month <= 12:
            return True
    return False

def validate_time(tim):
    """
    Validate a time tuple.

    :param tim: the time tuple to validate
    :return:    True=valid, False=invalid
    """
    global TIME_MODES
    if (tim is not None) and (len(tim) >= 3):
        hrs = to_int(tim[0])
        mns = to_int(tim[1])
        scs = to_float(tim[2])
        if (hrs >= 0) and (hrs < 24):
            if (mns >= 0) and (mns < 60):
                if (scs >= 0) and (scs < 60):
                    if len(tim) == 4:
                        md = tim[3]
                        if md in TIME_MODES:
                            return True
                    else:
                        return True
    return False
