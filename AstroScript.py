
import astrocore.astrodate as astrodate
import astrocore.astrodateio as astrodateio
import astrocore.sio as sio
from astrocore.mathutils import *

data = {
    'day_of_week' : -1,                 # Sunday=0, Monday=1, etc...
    'day_of_week_valid' : False,

    'month' : -1,                       # month of year, 1-12
    'day' : -1,                         # day of month, 1-31
    'year' : -1,                        # year, BC negative
    'hours' : -1,                       # hour of day, 1-24
    'minutes' : -1,                     # minute of hour, 0-59
    'seconds' : -1,                     # second of minute, 0-59
    'date_valid' : False,

    'time_mode' : astrodate.TIME_MODE_LCT,  # Type of time
    'time_mode_valid' : True,
    'valid_time_modes' : (astrodate.TIME_MODE_LCT, astrodate.TIME_MODE_UT, astrodate.TIME_MODE_TD, astrodate.TIME_MODE_GST, astrodate.TIME_MODE_LST),

    'julian_date' : -1,
    'julian_date_valid' : False,

    'zone_correction' : 0,              # time zone of the obzerver, hours
    'daylight_savings' : False,         # adjustment for daylight savings, hours
    'time_zone_valid' : False,

    'geographical_longitude' : 0.0,     # geographical longitude, degrees
    'geographical_longitude_valid' : False,

    'geographical_latitude' : 0.0,      # geographical latitude, degrees
    'geographical_latitude_valid' : False,
}

def convert_to_time_mode(tmod):
    """
    Convert the current date/time to the specified mode.
    
    :param tmod: the mode to convert to
    :return:     True=conversion successful, False=invalid date/time
    """
    global data
    if data['time_mode_valid']:
        d0 = get_date(withMode=True)
        astrodate.DAYLIGHT_SAVINGS = data['daylight_savings']
        astrodate.ZONE_CORRECTION = data['zone_correction']
        if data['geographical_longitude_valid']:
            astrodate.LONGITUDE = data['geographical_longitude']
        else:
            astrodate.LONGITUDE = 0.0
        if data['geographical_longitude_valid']:
            astrodate.LATITUDE = data['geographical_latitude']
        else:
            astrodate.LATITUDE = 0.0
        d1 = None
        if tmod == astrodate.TIME_MODE_LCT:
            d1 = astrodate.to_lct(d0)
        elif tmod == astrodate.TIME_MODE_UT:
            d1 = astrodate.to_ut(d0)
        elif tmod == astrodate.TIME_MODE_TD:
            d1 = astrodate.to_td(d0)
        elif tmod == astrodate.TIME_MODE_GST:
            d1 = astrodate.to_gst(d0)
        elif tmod == astrodate.TIME_MODE_LST:
            d1 = astrodate.to_lst(d0)
        if d1:
            set_date(d1[0], d1[1], d1[2], d1[3], d1[4], d1[5])
            set_time_mode(d1[6])
            return True
    return False

def display_date(title=None, dateType='calendar', newline=True):
    """
    Display the current date/time.
    
    :param title: title to display before the date/time (default=None)
    :param dateType: 'calendar'=display as a calendar date/time (default), 'julian'=display as a julian date/time
    :param newline: True=output newline after date/time (default), False=no newline after date/time
    """
    global data
    if dateType == 'calendar':
        if data['date_valid']:
            astrodateio.print_pretty_date(title, get_date(True), newline)
    elif dateType == 'julian':
        if data['julian_date_valid']:
            sio.print_labeled_text(title, ("%2.5f" % data['julian_date']), False, newline)

def display_newline():
    """
    Output a newline.
    """
    sio.print_newline()

def display_string(s, newline=True):
    """
    Display the provided string.
    
    :param s: the string to display
    :param newline: True=output newline after date/time (default), False=no newline after date/time
    """
    if type(s) is str:
        sio.print_text(s, newline)

def display_title(t):
    """
    Display the provided string as a title. The title is centered on the position set
    in sio.TITLE_CENTER (default: 30).
    
    :param t: the string to display
    """
    if type(t) is str:
        sio.print_title(t)

def get_date(withMode=False):
    """
    Get the current date/time as a tuple. This will return a tuple containing as much
    valid data as has been entered and can be one of the following:
        (year,month,day)
        (year,month,day,hours,minutes,seconds)
        (year,month,day,hours,minutes,seconds,mode)
    
    :param withMode: True=return the mode if available, False=do not return the mode (default)
    :return: date tuple, date/time tuple, or None
    """
    global data
    if data['date_valid']:
        if data['time_mode_valid']:
            if withMode:
                return data['year'], data['month'], data['day'], data['hours'], data['minutes'], data['seconds'], data['time_mode']
        return data['year'], data['month'], data['day'], data['hours'], data['minutes'], data['seconds']
    return None

def input_date():
    """
    Get a date/time as input.
    """
    dat = astrodateio.read_datetime()
    # print dat
    set_date(dat[0], dat[1], dat[2], dat[3], dat[4], dat[5])
    set_time_mode(dat[6])

def input_latitude():
    """
    Get a latitude value as input (-90.0 to 90.0).
    """
    lat = astrodateio.read_latitude()
    # print lat
    set_latitude(lat)

def input_longitude():
    """
    Get a longitude value as input(-360.0 to 360.0).
    """
    lon = astrodateio.read_longitude()
    # print lon
    set_longitude(lon)

def input_zone_correction():
    """
    Get a zone correction as input (-24.0 to 24.0).
    """
    zc = astrodateio.read_zone_correction()
    # print zc
    set_zone_correction(zc)

def set_date(yr, mo, dy, hr, mn, sc):
    """
    Set the current date/time.
    
    :param yr: the year
    :param mo: the month (1 to 12)
    :param dy: the day (1 to 31)
    :param hr: the hours (0 to 23)
    :param mn: the minutes (0 to 59)
    :param sc: the seconds (o to 59)
    """
    global data
    data['day'] = dy
    data['month'] = mo
    data['year'] = yr
    data['hours'] = hr
    data['minutes'] = mn
    data['seconds'] = fix(sc, astrodate.TIME_SECONDS_PRECISION)
    data['date_valid'] = True
    data['julian_date_valid'] = False

def set_daylight_savings(ds=False):
    """
    Set the daylight savings condition.
    
    :param ds: True=is daylight savings, False=is not daylight savings (default)
    """
    global data
    data['daylight_savings'] = ds

def set_latitude(lat):
    """
    Set the latitude.
    """
    global data
    data['geographical_latitude'] = lat
    if -90 <= lat <= 90:
        data['geographical_latitude_valid'] = True
    else:
        data['geographical_latitude_valid'] = False
    data['julian_date_valid'] = False

def set_longitude(lon):
    """
    Set the longitude.
    """
    global data
    data['geographical_longitude'] = lon
    if -180 <= lon <= 180:
        data['geographical_longitude_valid'] = True
    else:
        data['geographical_longitude_valid'] = False
    data['julian_date_valid'] = False

def set_time_mode(tmod):
    """
    Set the time mode.
    """
    global data
    data['time_mode'] = tmod
    if tmod in data['valid_time_modes']:
        data['time_mode_valid'] = True
    else:
        data['time_mode_valid'] = False
    data['julian_date_valid'] = False

def set_zone_correction(zc):
    """
    Set the zone correction.
    """
    global data
    data['zone_correction'] = zc
    if -12 <= zc <= 12:
        data['time_mode_valid'] = True
    else:
        data['time_mode_valid'] = False
    data['julian_date_valid'] = False

def update_julian_date():
    """
    Update the julian date for the current date/time.
    """
    global data
    dat = get_date(True)
    data['julian_date'] = astrodate.to_julian_from_date_tuple(dat)
    data['julian_date_valid'] = True


if __name__ == '__main__':
    display_title("Astro Date-Time Utility")
    input_date()
    if data['time_mode'] == astrodate.TIME_MODE_LCT:
        input_zone_correction()
    if data['time_mode'] == astrodate.TIME_MODE_LST or data['time_mode'] == astrodate.TIME_MODE_GST:
        input_longitude()
    update_julian_date()
    display_date(title='Entered Date', dateType='calendar')
    display_date(title='Julian Date', dateType='julian')

    convert_to_time_mode(astrodate.TIME_MODE_UT)
    update_julian_date()
    display_date(title='Universal Time', dateType='calendar')
    display_date(title='Julian Date', dateType='julian')
