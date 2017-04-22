import deltat
import math
import mathutils
import time


J1900 = 2415020.0			# corresponding to 1900 January 1 12:00:00 TDT
J1950 = 2433283.0           # corresponding to 1950 January 1 12:00:00 TDT
J2000 = 2451545.0			# corresponding to 2000 January 1 12:00:00 TDT

DAYS_OF_WEEK = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
LENGTH_OF_MONTH = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
TIME_MODE_LCT = u"lct"
TIME_MODE_UT = u"ut"
TIME_MODE_TD = u"td"
TIME_MODE_LST = u"lst"
TIME_MODE_GST = u"gst"
TIME_MODES = [TIME_MODE_LCT, TIME_MODE_UT, TIME_MODE_TD, TIME_MODE_GST, TIME_MODE_LST]
DATETIME_PRINT_FORMAT = '%b %d, %Y %H:%M:%S'
TIME_SECONDS_PRECISION = 2
SECONDS_MAX = None


def calculate_julian(yr, mth, day, hrs=None, mns=None, scs=None):
    """
    Calculate the julian date value.
    :param yr:  the year
    :param mth: the month
    :param day: the day
    :param hrs: the hours
    :param mns: the minutes
    :param scs: the seconds
    :return: the julian date
    """
    yr = mathutils.to_int(yr)
    mth = mathutils.to_int(mth)
    day = mathutils.to_int(day)
    hrs = mathutils.to_int(hrs)
    mns = mathutils.to_int(mns)
    scs = mathutils.to_float(scs)
    if mth <= 2:
        yr -= 1
        mth += 12
    if yr >= 1582:
        A = yr / 100
        B = 2 - A + (A / 4)
    else:
        B = 0
    if yr < 0:
        C = int((365.25 * yr) - 0.75)
    else:
        C = int(365.25 * yr)
    D = int(30.6001 * (mth + 1))
    return 1720994.5 + B + C + D + day + ((((mathutils.fix(scs, TIME_SECONDS_PRECISION) / 60.0) + float(
        mns)) / 60.0) + float(
        hrs)) / 24.0


def dh_from_hms(h, m, s):
    """
    Converts a time to decimal hours.
    :param h: hours
    :param m: minutes
    :param s: seconds
    :return:  dh
    """
    h = mathutils.to_int(h, None)
    m = mathutils.to_int(m, None)
    s = mathutils.to_float(s, None)
    if (h is not None) and (m is not None) and (s is not None):
        if h < 0:
            sgn = -1
        else:
            sgn = 1
        return sgn * ((((s / 60.0) + m) / 60.0) + abs(h))
    return None


def get_date_of_easter(y):
    """
    Calculate the date of Easter.
    :param y: year for which to calculate the date of Easter
    :return:  date tuple for Easter (None if not a valid year)(year, month, day)
    """
    y = mathutils.to_int(y)
    if y is not None:
        if y >= 1583:
            a = int(y % 19)
            b = int(y / 100)
            c = int(y % 100)
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
            return y, n, p
    return None


def get_days_in_month(m, y=None):
    """
    Determine the number of days in the month.
    :param:     m to analyze (1..12)
    :param:     y to use with month (None for basic analysis)
    :return:    number of days in the month
    """
    d = 0
    m = mathutils.to_int(m, None)
    if m is not None:
        d = LENGTH_OF_MONTH[m]
        if (y is not None) and (m == 2):
            y = mathutils.to_int(y, None)
            if is_leap_year(y):
                d += 1
    return d


def get_max_seconds():
    global SECONDS_MAX
    if SECONDS_MAX is not None:
        return SECONDS_MAX
    mult = math.pow(10, TIME_SECONDS_PRECISION)
    mx = int(60.0 * mult) - 1
    SECONDS_MAX = float(mx) / mult
    return SECONDS_MAX


def hms_from_dh(dh):
    """
    Converts decimal hours to a time tuple.
    :param dh:  decimal hours to convert
    :return:    time tuple (hours, mins, secs)
    """
    dh = mathutils.to_float(dh, None)
    if dh is not None:
        h = int(dh)
        dm = abs(dh - h) * 60.0
        m = int(dm + 0.0005)    # add a tiny amount to make sure the minutes round properly
        s = (dm - m) * 60.0
        return h, m, s
    return None


def is_leap_year(y):
    """
    Determine if the year is a leap year.
    :param y:   year     
    :return:    True or False
    """
    y = mathutils.to_int(y, None)
    if y is not None:
        if (y % 100) == 0:
            return (y % 400) == 0
        return (y % 4) == 0
    return None


def to_day_of_week_from_julian(jul):
    """
    Converts a julian to day of the week.
    :param jul: julian
    :return:    day of week
    """
    jul = mathutils.to_float(jul, None)
    if jul is not None:
        a = (jul + 1.5) / 7.0
        day = mathutils.to_int(round((a - mathutils.to_int(a)) * 7.0))
        return day - 1
    return None


def validate_date(year, month, day, hours=None, minutes=None, seconds=None, mode=None, require_time=True):
    """
    Validate a date or date time.
    :return:    (year, month, day[, hours, minutes, seconds[, mode]]) or None
    """
    yr = mathutils.to_int(year, None)
    mth = mathutils.to_int(month, None)
    dy = mathutils.to_int(day, None)
    if yr is not None:
        if (mth is not None) and (mth >= 1) and (mth <= 12):
            if is_leap_year(yr) and (mth == 2):
                if dy > 29:
                    return None
            elif dy > LENGTH_OF_MONTH[mth]:
                return None
            elif dy < 1:
                return None
            if hours is not None:
                tm = validate_time(hours, minutes, seconds, mode)
                if tm is None:
                    return None
                if len(tm) == 4:
                    return yr, mth, dy, tm[0], tm[1], tm[2], tm[3]
                return yr, mth, dy, tm[0], tm[1], tm[2]
            elif require_time:
                return None
            return yr, mth, dy
    return None


def validate_time(hours, minutes, seconds, mode=None):
    """
    Validate the time.
    :return:    (hours, minutes, seconds[, mode]) or None
    """
    hrs = mathutils.to_int(hours, None)
    mns = mathutils.to_int(minutes, None)
    scs = mathutils.to_float(seconds, None)
    if (hrs is not None) and (mns is not None) and (scs is not None):
        if (hrs >= 0) and (hrs < 24):
            if (mns >= 0) and (mns < 60):
                if (scs >= 0) and (scs < 60):
                    if mode is not None:
                        if mode in TIME_MODES:
                            return hrs, mns, scs, mode
                    else:
                        return hrs, mns, scs
    return None


class AstroDate:
    """
    Encapsulate the functionality to create and manipulate astronomical dates and times.
    This class supports dates with one of the following times: Local Civil Time (LCT), Universal Time (UT),
    mean Greenwich Sidereal Time (GST), Local Sidereal Time (LST), and Dynamical Time (TD).
    
    LCT refers to statutory time scales designated by civilian authorities, or to local time indicated by clocks.
    
    UT is a time standard based on Earth's rotation. It is a modern continuation of Greenwich Mean Time.
    
    GST is a minor adjustment from Greenwich apparent sidereal time (GAST), the hour angle of the vernal equinox
    at the prime meridian at Greenwich London, using the equation of the equinoxes.
    
    LST is a time standard adjussted by an amount that is proportional to the longitude of the locality.
    """

    def __init__(self):
        self.year = None
        self.month = None
        self.day = None
        self.hours = None
        self.minutes = None
        self.seconds = None
        self.mode = None
        self.daylight_saving = True
        self.zone_correction = 0
        self.longitude = 0

    @staticmethod
    def alloc(year, month=1, day=1, hours=0, minutes=0, seconds=0.0, mode=TIME_MODE_UT):
        """
        Allocate an AstroDate and set.
        :param year:    the year
        :param month:   the month
        :param day:     the day
        :param hours:   the hours
        :param minutes: the minutes
        :param seconds: the seconds
        :param mode:    the time mode
        :return: the AstroDate object
        """
        d = AstroDate()
        d.set(year, month, day, hours, minutes, seconds, mode)
        return d

    @staticmethod
    def alloc_with_date(date):
        d = AstroDate()
        dat = date.get_tuple()
        zc = date.get_zone_correction()
        ds = date.get_daylight_savings()
        lng = date.get_longitude()
        d.set_from_tuple(dat)
        d.set_zone_correction(zc)
        d.set_daylight_savings(ds)
        d.set_longitude(lng)
        return d

    @staticmethod
    def alloc_with_epochTD(epochTD):
        d = AstroDate()
        d.set_from_epochTD(epochTD)
        return d

    @staticmethod
    def alloc_with_julian(jd, mode=TIME_MODE_UT):
        """
        Allocate an AstroDate and set.
        :param jd:      the julian date
        :param mode:    the time mode
        :return: the AstroDate object
        """
        d = AstroDate()
        d.set_from_julian(jd, mode)
        return d

    @staticmethod
    def alloc_with_now():
        """
        Allocate an AstroDate and set to now.
        :return: the AstroDate object
        """
        d = AstroDate()
        d.now()
        return d

    @staticmethod
    def alloc_with_tuple(dat):
        """
        Allocate an AstroDate and set.
        :param dat: the date tuple to set with
        :return: the AstroDate object
        """
        d = AstroDate()
        d.set_from_tuple(dat)
        return d

    def add_days(self, dd):
        """
        Add a day delta to the date.
        :param dd:  day delta
        """
        if self.day is not None:
            self.day += mathutils.to_int(dd, 0)
            dm = 0
            while self.day < 1:
                self.day += get_days_in_month(self.month, self.year)
                dm -= 1
            while self.day > get_days_in_month(self.month, self.year):
                self.day -= get_days_in_month(self.month, self.year)
                dm += 1
            self.add_months(dm)

    def add_hours(self, dh):
        """
        Add an hour delta to the date.
        :param dh:  hour delta
        """
        if self.hours is not None:
            self.hours += mathutils.to_int(dh, 0)
            dd = 0
            while self.hours < 1:
                self.hours += 24
                dd -= 1
            while self.hours >= 24:
                self.hours -= 24
                dd += 1
            self.add_days(dd)

    def add_minutes(self, dm):
        """
        Add a minute delta to the date.
        :param dm:  minute delta
        """
        if self.minutes is not None:
            self.minutes += mathutils.to_int(dm, 0)
            dh = 0
            while self.minutes < 1:
                self.minutes += 24
                dh -= 1
            while self.minutes >= 24:
                self.minutes -= 24
                dh += 1
            self.add_hours(dh)

    def add_seconds(self, ds):
        """
        Add a seconds delta to the date.
        :param ds:  seconds delta
        """
        if self.seconds is not None:
            self.seconds += mathutils.to_float(ds, 0.0)
            dm = 0
            while self.seconds < 1:
                self.seconds += 60.0
                dm -= 1
            while self.seconds >= 60.0:
                self.seconds -= 60.0
                dm += 1
            self.add_minutes(dm)

    def add_months(self, dm):
        """
        Add a month delta to the date.
        :param dm:  month delta
        """
        if self.month is not None:
            self.month += mathutils.to_int(dm, 0)
            dy = 0
            while self.month < 1:
                self.month += 12
                dy -= 1
            while self.month > 12:
                self.month -= 12
                dy += 1
            self.add_years(dy)

    def add_years(self, dy):
        """
        Add a year delta to the date.
        :param dy:  year delta
        """
        if self.year is not None:
            self.year += mathutils.to_int(dy, 0)

    def get_date_of_easter(self):
        """
        Get the date of easter for the current year.
        :return:    the date of easter as a tuple (year, month, day)
        """
        return get_date_of_easter(self.year)

    def get_day(self):
        return self.day

    def get_daylight_savings(self):
        return self.daylight_saving

    def get_days_in_month(self):
        """
        Get the number of days in the current month.
        :return:    the number of days
        """
        return get_days_in_month(self.month, self.year)

    def get_decimal_hours(self):
        """
        Get the current time as a decimal value. 
        :return:    the current time
        """
        return dh_from_hms(self.hours, self.minutes, self.seconds)

    def get_julian(self, useZeroHours = False):
        """
        Calculate the julian day.
        :return:    julian
        """
        if useZeroHours:
            return calculate_julian(self.year, self.month, self.day)
        return calculate_julian(self.year, self.month, self.day, self.hours, self.minutes, self.seconds)

    def get_longitude(self):
        return self.longitude

    def get_month(self):
        return self.month

    def get_pretty_string(self, format=DATETIME_PRINT_FORMAT):
        """
        Convert the date to a formatted date string.
        :return:    the formatted date string
        """
        t = (self.year, self.month, self.day, self.hours, self.minutes, int(self.seconds), 0, 0, 0)
        s = time.strftime(format, t)
        if self.mode is not None:
            s += ' ' + self.mode.upper()
        return s

    def get_tuple(self):
        """
        Get the current date/time as a tuple.
        :return:    the date/time (year, month, day[, hours, minutes, seconds[, mode]])
        """
        if self.year is not None:
            if self.hours is not None:
                secs = mathutils.fix(self.seconds, TIME_SECONDS_PRECISION)
                if self.mode is not None:
                    return self.year, self.month, self.day, self.hours, self.minutes, secs, self.mode
                return self.year, self.month, self.day, self.hours, self.minutes, secs
            return self.year, self.month, self.day
        return None

    def get_year(self):
        return self.year

    def get_zone_correction(self):
        return self.zone_correction

    def is_date_set(self):
        """
        Test if the date has been set.
        :return: true=is set
        """
        return (self.year is not None) and (self.month is not None) and (self.day is not None)

    def is_gst(self):
        """
        Test if the time mode is GST.
        :return: true=is GST
        """
        return self.mode == TIME_MODE_GST

    def is_lct(self):
        """
        Test if the time mode is LCT.
        :return: true=is LCT
        """
        return self.mode == TIME_MODE_LCT

    def is_leap_year(self):
        """
        Test if the year is a leap year.
        :return: true=is leap year
        """
        return is_leap_year(self.year)

    def is_lst(self):
        """
        Test if the time mode is LST.
        :return: true=is LST
        """
        return self.mode == TIME_MODE_LST

    def is_mode_set(self):
        """
        Test if the time mode is set.
        :return: true=is set
        """
        return self.mode is not None

    def is_td(self):
        """
        Test if the time mode is TD.
        :return: true=is TD
        """
        return self.mode == TIME_MODE_TD

    def is_time_set(self):
        """
        Test if the time has been set.
        :return: true=is set
        """
        return (self.hours is not None) and (self.minutes is not None) and (self.seconds is not None)

    def is_ut(self):
        """
        Test if the time mode is UT.
        :return: true=is UT
        """
        return self.mode == TIME_MODE_UT

    def now(self, mode=TIME_MODE_LCT):
        """
        Get the current date and time.
        """
        current = time.time()
        dat = time.gmtime(current)
    #   dat = (year, month, day, hour, min, sec, weekday, julian day, daylight savings flag)
        self.set_year(dat[0])
        self.set_month(dat[1])
        self.set_day(dat[2])
        self.set_hours(dat[3])
        self.set_minutes(dat[4])
        self.set_seconds(dat[5])
        self.set_mode(mode)

    def set(self, year, month=1, day=1, hours=0, minutes=0, seconds=0.0, mode=TIME_MODE_UT):
        """
        Set the date and time.
        :param year:    the year
        :param month:   the month
        :param day:     the day
        :param hours:   the hours
        :param minutes: the minutes
        :param seconds: the seconds
        :param mode:    the mode
        """
        self.year = None
        self.month = None
        self.day = None
        self.hours = None
        self.minutes = None
        self.seconds = None
        self.mode = None
        if (year is not None) and (month is not None) and (day is not None):
            self.set_year(year)
            self.set_month(month)
            self.set_day(day)
            if (hours is not None) and (minutes is not None) and (seconds is not None):
                self.set_hours(hours)
                self.set_minutes(minutes)
                self.set_seconds(seconds)
                if mode is not None:
                    self.set_mode(mode)

    def set_day(self, day=1):
        """
        Set the day.
        :param day:     the day to set (1..31)
        """
        d = 1
        if day is not None:
            d = mathutils.to_int(day, 1)
            if d < 1:
                d = 1
            if d > self.get_days_in_month():
                d = self.get_days_in_month()
        self.day = d

    def set_daylight_savings(self, daylight_savings):
        """
        Set the daylight savings to be used in date calculations.
        :param daylight_savings: True=daylight savings
        """
        if daylight_savings is not None:
            self.daylight_saving = daylight_savings

    def set_from_epochTD(self, epochTD):
        self.set_year(mathutils.to_int(epochTD))
        self.set_month(1)
        self.set_day(1)
        self.set_hours(0)
        self.set_minutes(0)
        self.set_seconds(0.0)
        self.set_mode(TIME_MODE_TD)

    def set_from_hours(self, dh=0.0, mode=TIME_MODE_UT):
        """
        Set the time from decimal hours. 
        :param dh:      the time as decimal hours
        :param mode:    the time mode
        """
        h, m, s = hms_from_dh(dh)
        self.set_hours(m)
        self.set_minutes(m)
        self.set_seconds(s)
        self.set_mode(mode)

    def set_from_julian(self, jul, mode=TIME_MODE_UT):
        """
        Set date from a julian day.
        :param jul:     julian
        :param mode:    time mode (default: 'ut')
        """
        jul = mathutils.to_float(jul, None)
        if jul is not None:
            jd = 0.5 + jul
            I = mathutils.to_int(jd)
            F = jd - I
            if I > 2229160:
                A = mathutils.to_int((I - 1867216.25) / 36524.25)
                B = I + 1 + A - mathutils.to_int(A / 4.0)
            else:
                B = I
            C = B + 1524
            D = mathutils.to_int((C - 122.1) / 365.25)
            E = mathutils.to_int(365.25 * D)
            G = mathutils.to_int((C - E) / 30.6001)
            d = C - E + F - mathutils.to_int(30.6001 * G)
            if G < 13.5:
                mth = G - 1
            else:
                mth = G - 13
            if mth > 2.5:
                yr = D - 4716
            else:
                yr = D - 4715
            day = mathutils.to_int(d)
            h = (d - day) * 24
            hrs, mns, scs = hms_from_dh(h)
            self.set_year(yr)
            self.set_month(mth)
            self.set_day(day)
            self.set_hours(hrs)
            self.set_minutes(mns)
            self.set_seconds(scs)
            self.set_mode(mode)

    def set_from_tuple(self, dat):
        """
        Set from a tuple of values.
        (year, month, day[, hours, minutes, seconds[, mode]]
        :param dat:     the tuple of values to set with
        """
        self.year = None
        self.month = None
        self.day = None
        self.hours = None
        self.minutes = None
        self.seconds = None
        self.mode = None
        if dat is not None:
            if len(dat) == 7:
                self.set(dat[0], dat[1], dat[2], dat[3], dat[4], dat[5], dat[6])
            elif len(dat) == 6:
                self.set(dat[0], dat[1], dat[2], dat[3], dat[4], dat[5])
            elif len(dat) == 3:
                self.set(dat[0], dat[1], dat[2])

    def set_hours(self, h=0):
        """
        Set the hours.
        :param h:   the hours to set (0..23)
        """
        h = mathutils.to_int(h, 0)
        if h is not None:
            if h < 0:
                h = 0
            if h > 23:
                h = 23
        self.hours = h

    def set_longitude(self, longitude=0.0):
        """
        Set the longitude to be used in date calculations.
        :param longitude:   the longitude to set (- for west, + for east)(-180..180)
        """
        l = mathutils.to_float(longitude, 0.0)
        if l is not None:
            l = mathutils.normalize_degrees(l, -180.0, 180.0)
        self.longitude = l

    def set_minutes(self, minutes=0):
        """
        Set the minutes.
        :param minutes:   the minutes to set (0..59)
        """
        m = mathutils.to_int(minutes, 0)
        if m is not None:
            if m < 0:
                m = 0
            if m > 59:
                m = 59
        self.minutes = m

    def set_mode(self, mode=TIME_MODE_UT):
        """
        Set the time mode.
        :param mode: the time mode ("lct", "ut", "gst", "lst", "td") 
        """
        m = TIME_MODE_UT
        if mode is not None:
            mode = mode.lower()
            if mode in TIME_MODES:
                m = mode
        self.mode = m

    def set_month(self, month=1):
        """
        Set the month.
        :param month:   the month to set (1..12)
        """
        m = mathutils.to_int(month, 1)
        if m is not None:
            if m < 1:
                m = 1
            if m > 12:
                m = 12
        self.month = m
        if self.day is not None:
            if self.day > self.get_days_in_month():
                self.day = self.get_days_in_month()

    def set_seconds(self, seconds=0.0):
        """
        Set the seconds.
        :param seconds:     the seconds to set (0..59.99)
        """
        s = mathutils.to_float(seconds, 0.0)
        if s is not None:
            if s < 0.0:
                s = 0.0
            if s > get_max_seconds():
                s = get_max_seconds()
        self.seconds = s

    def set_year(self, year):
        """
        Set the year.
        :param year:    the year to set
        """
        y = mathutils.to_int(year, None)
        if y is not None:
            self.year = y
        if self.day is not None:
            if self.day > self.get_days_in_month():
                self.day = self.get_days_in_month()

    def set_zone_correction(self, zc):
        """
        Set the time zone correction to be used in date calculations.
        :param zc:  the time zone correction to set (- for west, + for east)(-24..24)
        """
        zc = mathutils.to_int(zc, 0)
        if zc is not None:
            zc = mathutils.normalize_hours(zc, -24.0, 24.0)
        self.zone_correction = zc

    def to_gst(self):
        """
        Converts to greenwich mean sidereal time.
        Note: this method depends on longitude being set to convert from LST.
        Note: this method depends on zone_correction and daylight_savings being set to convert from LCT.
        """
        if (self.mode == TIME_MODE_TD) or (self.mode == TIME_MODE_LCT):
            self.to_ut()
        if self.mode == TIME_MODE_UT:
            jd = self.get_julian(useZeroHours=True)
            S = jd - 2451545.0
            T = S / 36525.0
            T0 = 6.69737455833 + (T * (2400.0513369 + (T * 0.00002586222 + (T * 0.00000000172))))
            while T0 >= 24.0:
                T0 -= 24.0
            while T0 < 0.0:
                T0 += 24.0
            H = dh_from_hms(self.hours, self.minutes, self.seconds)
            t = T0
            t += 1.002737909 * H
            while t >= 24.0:
                t -= 24.0
            self.hours, self.minutes, self.seconds = hms_from_dh(t)
            self.mode = TIME_MODE_GST
        if self.mode == TIME_MODE_LST:
            t = dh_from_hms(self.hours, self.minutes, self.seconds)
            t -= self.longitude / 15.0
            if t >= 24.0:
                t -= 24.0
            elif t < 0.0:
                t += 24.0
            self.hours, self.minutes, self.seconds = hms_from_dh(t)
            self.mode = TIME_MODE_GST

    def to_lct(self):
        """
        Convert to local civil time.
        Note: this method depends on longitude being set to convert from LST.
        Note: this method depends on zone_correction and daylight_savings being set to convert to LCT.
        """
        if (self.mode == TIME_MODE_TD) or (self.mode == TIME_MODE_LST) or (self.mode == TIME_MODE_GST):
            self.to_ut()
        if self.mode == TIME_MODE_UT:
            t = dh_from_hms(self.hours, self.minutes, self.seconds)
            t += self.zone_correction
            if self.daylight_saving:
                t += 1
            if t >= 24.0:
                t -= 24.0
                self.add_days(1)
            elif t < 0.0:
                t += 24.0
                self.add_days(-1)
            self.hours, self.minutes, self.seconds = hms_from_dh(t)
            self.mode = TIME_MODE_LCT

    def to_lst(self):
        """
        Convert to local mean sidereal time.
        Note: this method depends on longitude being set to convert to LST.
        Note: this method depends on zone_correction and daylight_savings being set to convert from LCT.
        """
        if self.mode == TIME_MODE_TD:
            self.to_ut()
        if (self.mode == TIME_MODE_LCT) or (self.mode == TIME_MODE_UT):
            self.to_gst()
        if self.mode == TIME_MODE_GST:
            t = dh_from_hms(self.hours, self.minutes, self.seconds)
            t += self.longitude / 15.0
            if t >= 24.0:
                t -= 24.0
            elif t < 0.0:
                t += 24.0
            self.hours, self.minutes, self.seconds = hms_from_dh(t)
            self.mode = TIME_MODE_LST

    def to_td(self):
        """
        Convert to dynamical time.
        Note: this method depends on longitude being set to convert from LST.
        Note: this method depends on zone_correction and daylight_savings being set to convert from LCT.
        """
        if self.mode != TIME_MODE_TD:
            self.to_ut()
            dt = deltat.calc_dt_interp(self.get_tuple()) / 86400.0
            jde = self.get_julian() + dt
            self.set_from_julian(jde, TIME_MODE_TD)

    def to_ut(self):
        """
        Convert to universal time.
        Note: this method depends on longitude being set to convert from LST.
        Note: this method depends on zone_correction and daylight_savings being set to convert from LCT.
        """
        if self.mode == TIME_MODE_LCT:
            t = dh_from_hms(self.hours, self.minutes, self.seconds)
            if self.daylight_saving:
                t -= 1
            t -= self.zone_correction
            if t >= 24.0:
                t -= 24.0
                self.add_days(1)
            elif t < 0.0:
                t += 24.0
                self.add_days(-1)
            self.hours, self.minutes, self.seconds = hms_from_dh(t)
            self.mode = TIME_MODE_UT
        if self.mode == TIME_MODE_LST:
            self.to_gst()
        if self.mode == TIME_MODE_GST:
            jd = self.get_julian(useZeroHours=True)
            S = jd - 2451545.0
            T = S / 36525.0
            T0 = 6.69737455833 + (T * (2400.0513369 + (T * 0.00002586222 + (T * 0.00000000172))))
            while T0 >= 24.0:
                T0 -= 24.0
            while T0 < 0.0:
                T0 += 24.0
            H = dh_from_hms(self.hours, self.minutes, self.seconds)
            t = H - T0
            while t < 0.0:
                t += 24.0
            t /= 1.002737909
            self.hours, self.minutes, self.seconds = hms_from_dh(t)
            self.mode = TIME_MODE_UT
        if self.mode == TIME_MODE_TD:
            t = deltat.calc_dt_interp(self.get_tuple()) / 86400.0
            j = self.get_julian()
            self.set_from_julian(j - t, TIME_MODE_UT)


if __name__ == "__main__":


    dat_td = (1950, 1, 1, 12, 0, 0, "td")
    dat = AstroDate()
    dat.set_from_tuple(dat_td)
    jd = dat.get_julian()
    print(jde)
