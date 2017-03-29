
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
    global data
    if dateType == 'calendar':
        if data['date_valid']:
            astrodateio.print_pretty_date(title, get_date(True), newline)
    elif dateType == 'julian':
        if data['julian_date_valid']:
            sio.print_labeled_text(title, ("%2.5f" % data['julian_date']), False, newline)

def display_newline():
    sio.print_newline()

def display_string(s, newline=True):
    if type(s) is str:
        sio.print_text(s, newline)

def display_title(t):
    if type(t) is str:
        sio.print_title(t)

def get_date(withMode=False):
    global data
    if data['date_valid']:
        if withMode and data['time_mode_valid']:
            return data['year'], data['month'], data['day'], data['hours'], data['minutes'], data['seconds'], data['time_mode']
        return data['year'], data['month'], data['day'], data['hours'], data['minutes'], data['seconds']
    return None

def input_date():
    dat = astrodateio.read_datetime()
    # print dat
    set_date(dat[0], dat[1], dat[2], dat[3], dat[4], dat[5])
    set_time_mode(dat[6])

def input_latitude():
    lat = astrodateio.read_latitude()
    # print lat
    set_latitude(lat)

def input_longitude():
    lon = astrodateio.read_longitude()
    # print lon
    set_longitude(lon)

def input_zone_correction():
    zc = astrodateio.read_zone_correction()
    # print zc
    set_zone_correction(zc)

def set_date(yr, mo, dy, hr, mn, sc):
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
    global data
    data['daylight_savings'] = ds

def set_latitude(lat):
    global data
    data['geographical_latitude'] = lat
    data['geographical_latitude_valid'] = True
    data['julian_date_valid'] = False

def set_longitude(lon):
    global data
    data['geographical_longitude'] = lon
    data['geographical_longitude_valid'] = True
    data['julian_date_valid'] = False

def set_time_mode(tmod):
    global data
    data['time_mode'] = tmod
    if tmod in data['valid_time_modes']:
        data['time_mode_valid'] = True
    else:
        data['time_mode_valid'] = False
    data['julian_date_valid'] = False

def set_zone_correction(zc):
    global data
    data['zone_correction'] = zc
    if -12 <= zc <= 12:
        data['time_mode_valid'] = True
    else:
        data['time_mode_valid'] = False
    data['julian_date_valid'] = False

def update_julian_date():
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
