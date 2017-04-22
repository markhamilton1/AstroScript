
import astrodate
import mathutils
import sio
import time

DATE_DELIMITER = ','
DATE_PROMPT = "Enter a date"
DATE_FORMAT = "yr, mo, dy"
DATE_HELP = "Enter the date in the indicated order (ignoring the square brackets).\r\nEntering an '*' will use the current system date."
DATE_INVALID = "The entered date is invalid!"
DATETIME_PROMPT = "Enter a date-time"
DATETIME_FORMAT = "yr, mo, dy, hr, mn, sc, md"
DATETIME_HELP = "Enter the date and time in the indicated order (ignoring the square brackets).\r\nEntering an '*' will use the current system date and time."
DATETIME_INVALID = "The entered date-time is invalid!"
LONGITUDE_PROMPT = "Enter a longitude (-W|+E)"
LONGITUDE_FORMAT = "###.##"
LONGITUDE_HELP = "No help available."
LONGITUDE_INVALID = "The entered longitude is invalid!"
LATITUDE_PROMPT = "Enter a latitude (+N|-S)"
LATITUDE_FORMAT = "##.##"
LATITUDE_HELP = "No help available."
LATITUDE_INVALID = "The entered latitude is invalid!"
ZONE_CORRECTION_PROMPT = "Enter a zone correction (-W|+E)"
ZONE_CORRECTION_FORMAT = "##"
ZONE_CORRECTION_HELP = "No help available."
ZONE_CORRECTION_INVALID = "The entered zone correction is invalid!"


def __convert_date_time(res):
    """
    Convert the response array (usually from keyboard input) into a date time tuple.

    :param res: the response to convert
    :return:    an unvalidated date time tuple
    """
    dat = []
    i = 0
    while (i < len(res)) and (i < 7):
        if i < 5:
            dat.append(mathutils.to_int(res[i]))
        elif i == 5:
            dat.append(mathutils.fix(res[i], astrodate.TIME_SECONDS_PRECISION))
        else:
            dat.append(res[i])
        i += 1
    return dat


def print_pretty_date(label, dat, newline=True):
    """
    Print the date date tuple as a properly formatted date string

    :param label:   the label to prepend
    :param dat:     the date tuple to use
    :param newline: a boolean indicating if a newline should be added
    """
    s = dat.to_pretty_date(dat)
    if s:
        sio.print_labeled_text(label, s, newline=newline)


def read_date(default_date=None, prompt=DATE_PROMPT, format=DATE_FORMAT):
    """
    Read a date tuple.

    :param default_date:    the default date tuple to use
    :param prompt:          the prompt to use (optional)
    :param format:          the format to use (optional)
    :return:    the date tuple (year, month, day[, hours, minutes, seconds, mode])
    """
    while True:
        res = sio.read_delimited_line(DATE_DELIMITER, prompt, None, format, default_date)
        if (type(res) is str) and (len(res) == 0):
            return None
        if (type(res) is str) and (len(res) == 1) and (res[0] == '?'):
            sio.print_newline()
            sio.print_text(DATE_HELP)
            sio.print_newline()
        elif (type(res) is str) and (len(res) == 1) and (res[0] == '*'):
            current = time.time()
            dat = time.gmtime(current)
            #   dat = (year, month, day, hour, min, sec, weekday, julian day, daylight savings flag)
            year = dat[0]
            month = dat[1]
            day = dat[2]
            hours = dat[3]
            minutes = dat[4]
            seconds = mathutils.fix(dat[5], astrodate.TIME_SECONDS_PRECISION)
            mode = astrodate.TIME_MODE_UT
            return year, month, day, hours, minutes, seconds, mode
        else:
            dat = __convert_date_time(res)
            if not astrodate.validate_date(dat, False):
                sio.print_newline()
                sio.print_text(DATE_INVALID)
                sio.print_newline()
            else:
                return tuple(dat)


def read_datetime(default_datetime=None, prompt=DATETIME_PROMPT, format=DATETIME_FORMAT):
    """
    Read a date time tuple.

    :param default_datetime:    the default date time tuple to use
    :param prompt:              the prompt to use (optional)
    :param format:              the format to use (optional)
    :return:    the date time tuple (year, month, day[, hours, minutes, seconds, mode])
    """
    while True:
        res = sio.read_delimited_line(DATE_DELIMITER, prompt, None, format, default_datetime)
        if (type(res) is str) and (len(res) == 0):
            return None
        if (type(res) is str) and (len(res) == 1) and (res[0] == '?'):
            sio.print_newline()
            sio.print_text(DATETIME_HELP)
            sio.print_newline()
        elif (type(res) is str) and (len(res) == 1) and (res[0] == '*'):
            current = time.time()
            dat = time.gmtime(current)
            #   dat = (year, month, day, hour, min, sec, weekday, julian day, daylight savings flag)
            year = dat[0]
            month = dat[1]
            day = dat[2]
            hours = dat[3]
            minutes = dat[4]
            seconds = mathutils.fix(dat[5], astrodate.TIME_SECONDS_PRECISION)
            mode = astrodate.TIME_MODE_UT
            return year, month, day, hours, minutes, seconds, mode
        else:
            dat = __convert_date_time(res)
            if not astrodate.validate_date(dat, True):
                sio.print_newline()
                sio.print_text(DATETIME_INVALID)
                sio.print_newline()
            else:
                return tuple(dat)


def read_latitude(default_latitude=None, prompt=LATITUDE_PROMPT, format=LATITUDE_FORMAT):
    """
    Read a latitude.

    :param default_latitude:    the default latitude to use
    :param prompt:              the prompt to use (optional)
    :param format:              the format to use (optional)
    :return:    the latitude
    """
    while True:
        res = sio.read_line(prompt, None, format, default_latitude)
        if not len(res):
            return None
        if len(res) == 1:
            if res[0] == '?':
                sio.print_newline()
                sio.print_text(LATITUDE_HELP)
                sio.print_newline()
        else:
            try:
                lat = float(res)
                if abs(lat) <= 90.0:
                    return lat
            except Exception:
                pass
            sio.print_newline()
            sio.print_text(LATITUDE_INVALID)
            sio.print_newline()


def read_longitude(default_longitude=None, prompt=LONGITUDE_PROMPT, format=LONGITUDE_FORMAT):
    """
    Read a longitude.

    :param default_longitude:   the default longitude to use
    :param prompt:              the prompt to use (optional)
    :param format:              the format to use (optional)
    :return:    the longitude
    """
    while True:
        res = sio.read_line(prompt, None, format, default_longitude)
        if not len(res):
            return None
        if len(res) == 1:
            if res[0] == '?':
                sio.print_newline()
                sio.print_text(LONGITUDE_HELP)
                sio.print_newline()
        else:
            try:
                lng = float(res)
                if abs(lng) <= 180.0:
                    return lng
            except Exception:
                pass
            sio.print_newline()
            sio.print_text(LONGITUDE_INVALID)
            sio.print_newline()


def read_zone_correction(default_zone_correction=None, prompt=ZONE_CORRECTION_PROMPT, format=ZONE_CORRECTION_FORMAT):
    """
    Read a time zone correction.

    :param default_zone_correction: the default time zone correction to use
    :param prompt:                  the prompt to use (optional)
    :param format:                  the format to use (optional)
    :return:    the zone correction
    """
    while True:
        res = sio.read_line(prompt, None, format, default_zone_correction)
        if not len(res):
            return None
        if len(res) == 1:
            if res[0] == '?':
                sio.print_newline()
                sio.print_text(ZONE_CORRECTION_HELP)
                sio.print_newline()
        else:
            try:
                zc = int(res)
                if abs(zc) <= 12:
                    return zc
            except Exception:
                pass
            sio.print_newline()
            sio.print_text(ZONE_CORRECTION_INVALID)
            sio.print_newline()
