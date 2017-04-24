import astrodate
import earth
import math
import mathutils


COORD_MODE_HORIZON = u'hor'         # degrees (Azimuth)
COORD_MODE_EQUATORIAL = u'equ'      # hours or degrees (Right Ascension or Hour Angle)
COORD_MODE_ECLIPTIC = u'ecl'        # degrees (Longitude)
COORD_MODE_GALACTIC = u'gal'        # degrees (Longitude)
COORD_MODES = [COORD_MODE_HORIZON, COORD_MODE_EQUATORIAL, COORD_MODE_ECLIPTIC, COORD_MODE_GALACTIC]

COORD1_UNIT_DEGREES = u'deg'        #
COORD1_UNIT_HOURS = u'hrs'          # Equatorial Only
COORD1_UNITS = [COORD1_UNIT_DEGREES, COORD1_UNIT_HOURS]

COORD1_TYPE_RA = u'ra'              # Equatorial Only - Right Ascension
COORD1_TYPE_HA = u"ha"              # Equatorial Only - Hour Angle
COORD1_TYPES = [COORD1_TYPE_RA, COORD1_TYPE_HA]

MODE_DELIMITER = '|'


def dd_from_dms(d, m, s):
    d = mathutils.to_int(d, None)
    m = mathutils.to_int(m, None)
    s = mathutils.to_float(s, None)
    if (d is not None) and (m is not None) and (s is not None):
        if d < 0:
            sgn = -1
        else:
            sgn = 1
        dd = sgn * ((((s / 60.0) + float(m)) / 60.0) + float(abs(d)))
        return dd
    return None


def dms_from_dd(dd):
    dd = mathutils.to_float(dd, None)
    if dd is not None:
        d = int(dd)
        dm = abs(dd - d) * 60.0
        m = int(dm + 0.0005)
        s = mathutils.fix((dm - m) * 60.0, 2)
        return d, m, s
    return None


def make_mode(m, u=None, t=None):
    m = safe_lower(m)
    u = safe_lower(u)
    t = safe_lower(t)
    if (m is not None) and (m in COORD_MODES):
        if m == COORD_MODE_EQUATORIAL:
            if (u is not None) and (u in COORD1_UNITS):
                if (t is not None) and (t in COORD1_TYPES):
                    return "{}{}{}{}{}".format(m, MODE_DELIMITER, u, MODE_DELIMITER, t)
            return None
        return m
    return None


def normalize_dd1(dd, hrs):
    if hrs:
        dd = mathutils.normalize_hours(dd, 0.0, 24.0)
    else:
        dd = mathutils.normalize_degrees(dd, 0.0, 360.0)
    return dd


def normalize_dd2(dd):
    dd = mathutils.normalize_degrees(dd, -180.0, 180.0)
    return dd


def safe_lower(s):
    if s is not None:
        return s.lower()
    return None


def split_mode(mode):
    parts = mode.split(MODE_DELIMITER)
    m = None
    u = None
    t = None
    for p in parts:
        p = safe_lower(p)
        if (m is None) and (p in COORD_MODES):
            m = p
        elif (u is None) and (p in COORD1_UNITS):
            u = p
        elif (t is None) and (p in COORD1_TYPES):
            t = p
    return m, u, t


def validate_coord(coord):
    if coord is not None:
        d1, m1, s1 = coord.deg1, coord.min1, coord.sec1
        d2, m2, s2 = coord.deg2, coord.min2, coord.sec2
        mode_parts = split_mode(coord.mode)
        if (mode_parts[0] == COORD_MODE_EQUATORIAL) and (mode_parts[1] in COORD1_UNITS) and (mode_parts[2] in COORD1_TYPES):
            if validate_degrees(d2, m2, s2):
                if mode_parts[1] == COORD1_UNIT_HOURS:
                    if validate_hours(d1, m1, s1):
                        return d1, m1, s1, d2, m2, s2, coord.mode
                elif validate_degrees(d1, m1, s1):
                    return d1, m1, s1, d2, m2, s2, coord.mode
        else:
            if validate_degrees(d1, m1, s1):
                if validate_degrees(d2, m2, s2):
                    return d1, m1, s1, d2, m2, s2, coord.mode
    return None


def validate_degrees(d, m, s):
    if (d is not None) and (d == mathutils.to_int(d)) and (d >= -360.0) and (d <= 360.0):
        if (m is not None) and (m == mathutils.to_int(m)) and (m >= 0.0) and (m <= 59.0):
            if (s is not None) and (s == mathutils.to_float(s)) and (s >= 0.0) and (s < 60.0):
                return True
    return False


def validate_hours(h, m, s):
    if (h is not None) and (h == mathutils.to_int(h)) and (h > -24.0) and (h <= 24.0):
        if (m is not None) and (m == mathutils.to_int(m)) and (m >= 0.0) and (m <= 59.0):
            if (s is not None) and (s == mathutils.to_float(s)) and (s >= 0.0) and (s < 60.0):
                return True
    return False


class AstroCoord:

    def __init__(self):
        self.deg1 = None
        self.min1 = None
        self.sec1 = None
        self.deg2 = None
        self.min2 = None
        self.sec2 = None
        self.mode = None
        self.date = None
        self.latitude = None

    @staticmethod
    def alloc(deg1=None, min1=None, sec1=None, deg2=None, min2=None, sec2=None, mode=None):
        c = AstroCoord()
        c.set(deg1, min1, sec1, deg2, min2, sec2, mode)
        return c

    @staticmethod
    def alloc_with_degrees(dd1, dd2, mode):
        c = AstroCoord()
        c.set_with_degrees(dd1, dd2, mode)
        return c

    @staticmethod
    def alloc_with_tuple(coord):
        c = AstroCoord()
        c.set_with_tuple(coord)
        return c

    def add_coord1(self, d):
        dd1 = self.get_dd1() + d
        dd1 = normalize_dd1(dd1, self.is_hours())
        d1, m1, s1 = dms_from_dd(dd1)
        self.set_deg1(d1)
        self.set_min1(m1)
        self.set_sec1(s1)

    def add_coord2(self, d):
        dd2 = self.get_dd2() + d
        dd2 = normalize_dd2(dd2)
        d2, m2, s2 = dms_from_dd(dd2)
        self.set_deg2(d2)
        self.set_min2(m2)
        self.set_sec2(s2)

    def calculate_angular_separation(self, coord2):
        if (self.mode == coord2.mode) and (self.is_equatorial() or self.is_ecliptic()):
            c1_1 = self.get_dd1()
            c2_1 = coord2.get_dd1()
            if self.is_hours():
                c1_1 *= 15.0
                c2_1 *= 15.0
            diff_c1_1_c2_1 = c1_1 - c2_1
            diff_c1_1_c2_1_rad = diff_c1_1_c2_1 * math.pi / 180.0
            c1_2 = self.get_dd2()
            c1_2_rad = c1_2 * math.pi / 180.0
            c2_2 = coord2.get_dd2()
            c2_2_rad = c2_2 * math.pi / 180.0
            cos_d = (math.sin(c1_2_rad) * math.sin(c2_2_rad)) + (math.cos(c1_2_rad) * math.cos(c2_2_rad) * math.cos(diff_c1_1_c2_1_rad))
            dd = math.acos(cos_d) * 180.0 / math.pi
            if (dd <= 0.16666667) or (dd >= 179.83333333):
                t1 = math.cos((c1_2 + c2_2) / 2.0)
                t2 = c1_1 - c2_1
                t3 = c1_2 - c2_2
                t = (t1 * t1) * (t2 * t2) + (t3 * t3)
                dd = math.sqrt(t)
            d, m, s = dms_from_dd(dd)
            return d, m, mathutils.fix(s, 2)
        raise ValueError, "Invalid coordinate! (Must be Equatorial or Ecliptic)"

    def calculate_mean_obliquity(self, epochTD=None):
        if epochTD is not None:
            d = astrodate.AstroDate().alloc_with_epochTD(epochTD)
        else:
            if self.date is None:
                raise ValueError, "Date (TD) is required!"
            self.date.to_tdt()
            d = self.date
        n = earth.Nutation()
        n.calculate_with_julianTD(d.get_julian())
        return n.get_mean_obliquity()

    def get_dd1(self):
        return dd_from_dms(self.deg1, self.min1, self.sec1)

    def get_dd2(self):
        return dd_from_dms(self.deg2, self.min2, self.sec2)

    def get_pretty_string(self, format="dms"):
        s = ""
        if format.lower() == "dms":
            d1 = int(self.deg1)
            m1 = int(self.min1)
            s1 = self.sec1
            d2 = int(self.deg2)
            m2 = int(self.min2)
            s2 = self.sec2
            if self.is_hours():
                s1 = "{:02d}h{:02d}m{:05.2f}s".format(d1, m1, s1)
            else:
                s1 = "{:02d}d{:02d}m{:05.2f}s".format(d1, m1, s1)
            s2 = " {:+02d}d{:02d}m{:05.2f}s".format(d2, m2, s2)
            s = s1 + s2
        elif format.lower() == "d":
            d1 = self.get_dd1()
            d2 = self.get_dd2()
            s = "{:09.6f} {:09.6f}".format(d1, d2)
        return s

    def get_tuple(self):
        return self.deg1, self.min1, self.sec1, self.deg2, self.min2, self.sec2, self.mode

    def is_degrees(self):
        mode = split_mode(self.mode)
        return not (mode[0] == COORD_MODE_EQUATORIAL) or (mode[0] == COORD_MODE_EQUATORIAL) and (mode[1] == COORD1_UNIT_DEGREES)

    def is_ecliptic(self):
        mode = split_mode(self.mode)
        return mode[0] == COORD_MODE_ECLIPTIC

    def is_equatorial(self):
        mode = split_mode(self.mode)
        return mode[0] == COORD_MODE_EQUATORIAL

    def is_galactic(self):
        mode = split_mode(self.mode)
        return mode[0] == COORD_MODE_GALACTIC

    def is_horizon(self):
        mode = split_mode(self.mode)
        return mode[0] == COORD_MODE_HORIZON

    def is_hours(self):
        mode = split_mode(self.mode)
        return (mode[0] == COORD_MODE_EQUATORIAL) and (mode[1] == COORD1_UNIT_HOURS)

    def is_hour_angle(self):
        mode = split_mode(self.mode)
        return (mode[0] == COORD_MODE_EQUATORIAL) and (mode[2] == COORD1_TYPE_HA)

    def is_right_ascension(self):
        mode = split_mode(self.mode)
        return (mode[0] == COORD_MODE_EQUATORIAL) and (mode[2] == COORD1_TYPE_RA)

    def set(self, deg1=None, min1=None, sec1=None, deg2=None, min2=None, sec2=None, mode=None):
        self.set_deg1(deg1)
        self.set_min1(min1)
        self.set_sec1(sec1)
        self.set_deg2(deg2)
        self.set_min2(min2)
        self.set_sec2(sec2)
        self.set_mode(mode)

    def set_date(self, date):
        if date is not None:
            self.date = date
        else:
            self.date = None

    def set_deg1(self, deg1):
        d = 0
        if deg1 is not None:
            d = mathutils.to_int(deg1, 0)
        self.deg1 = d

    def set_deg2(self, deg2):
        d = 0
        if deg2 is not None:
            d = mathutils.to_int(deg2, 0)
        self.deg2 = d

    def set_with_degrees(self, dd1, dd2, mode):
        d1, m1, s1 = dms_from_dd(dd1)
        d2, m2, s2 = dms_from_dd(dd2)
        self.set(d1, m1, s1, d2, m2, s2, mode)

    def set_with_tuple(self, coord):
        self.set(coord[0], coord[1], coord[2], coord[3], coord[4], coord[5], coord[6])

    def set_latitude(self, latitude):
        l = mathutils.to_float(latitude, 0.0)
        if l is not None:
            l = mathutils.normalize_degrees(l, -90, 90.0)
        self.latitude = l

    def set_min1(self, min1):
        m = 0
        if min1 is not None:
            m = mathutils.to_int(min1, 0)
        self.min1 = m

    def set_min2(self, min2):
        m = 0
        if min2 is not None:
            m = mathutils.to_int(min2, 0)
        self.min2 = m

    def set_mode(self, mode):
        self.mode = mode

    def set_sec1(self, sec1):
        s = 0
        if sec1 is not None:
            s = mathutils.to_float(sec1, 0.0)
        self.sec1 = s

    def set_sec2(self, sec2):
        s = 0
        if sec2 is not None:
            s = mathutils.to_float(sec2, 0.0)
        self.sec2 = s

    def to_degrees(self):
        if not self.is_equatorial():
            raise ValueError, "Invalid coord! (Must be Equatorial)"
        if self.is_hours():
            dd = self.get_dd1() * 15.0
            d1, m1, s1 = dms_from_dd(dd)
            mode_parts = split_mode(self.mode)
            mode = make_mode(mode_parts[0], COORD1_UNIT_DEGREES, mode_parts[2])
            self.set_deg1(d1)
            self.set_min1(m1)
            self.set_sec1(s1)
            self.set_mode(mode)

    def to_hour_angle(self):
        if not self.is_equatorial():
            raise ValueError, "Invalid coordinate! (Must be Equatorial)"
        if self.is_right_ascension():
            self.__equ_conv()
            mode_parts = split_mode(self.mode)
            mode = make_mode(mode_parts[0], mode_parts[1], COORD1_TYPE_HA)
            self.set_mode(mode)

    def to_hours(self):
        if not self.is_equatorial():
            raise ValueError, "Invalid coordinate! (Must be Equatorial)"
        if self.is_degrees():
            dd = self.get_dd1() / 15.0
            d1, m1, s1 = dms_from_dd(dd)
            mode_parts = split_mode(self.mode)
            mode = make_mode(mode_parts[0], COORD1_UNIT_HOURS, mode_parts[2])
            self.set_deg1(d1)
            self.set_min1(m1)
            self.set_sec1(s1)
            self.set_mode(mode)

    def to_ecliptic(self):
        if self.is_ecliptic():
            return
        self.to_equatorial()
        if not self.is_right_ascension():
            self.to_right_ascension()
        self.to_degrees()
        a1 = self.get_dd1() * math.pi / 180.0
        a2 = self.get_dd2() * math.pi / 180.0
        e = self.calculate_mean_obliquity() * math.pi / 180.0
        sin_a1 = math.sin(a1)
        sin_e = math.sin(e)
        cos_e = math.cos(e)
        a4 = math.asin((math.sin(a2) * cos_e) - (math.cos(a2) * sin_a1 * sin_e)) * 180.0 / math.pi
        y = (sin_a1 * cos_e) + (math.tan(a2) * sin_e)
        x = math.cos(a1)
        a3 = math.atan2(y, x) * 180.0 / math.pi
        d1, m1, s1 = dms_from_dd(a3)
        d2, m2, s2 = dms_from_dd(a4)
        mode = make_mode(COORD_MODE_ECLIPTIC)
        self.set_deg1(d1)
        self.set_min1(m1)
        self.set_sec1(s1)
        self.set_deg2(d2)
        self.set_min2(m2)
        self.set_sec2(s2)
        self.set_mode(mode)

    def to_equatorial(self, epochTD=None):
        if self.is_ecliptic():
            a1deg = self.get_dd1()
            a2deg = self.get_dd2()
            a1rad = a1deg * math.pi / 180.0
            a2rad = a2deg * math.pi / 180.0
            edeg = self.calculate_mean_obliquity(epochTD)
            erad = edeg * math.pi / 180.0
            sin_a1 = math.sin(a1rad)
            sin_e = math.sin(erad)
            cos_e = math.cos(erad)
            a4rad = math.asin((math.sin(a2rad) * cos_e) + (math.cos(a2rad) * sin_a1 * sin_e))
            a4deg = a4rad * 180.0 / math.pi
            y = (sin_a1 * cos_e) - (math.tan(a2rad) * sin_e)
            x = math.cos(a1rad)
            a3rad = math.atan2(y, x)
            a3deg = a3rad * 180.0 / math.pi
            d1, m1, s1 = dms_from_dd(a3deg / 15.0)
            d2, m2, s2 = dms_from_dd(a4deg)
            mode = make_mode(COORD_MODE_EQUATORIAL, COORD1_UNIT_HOURS, COORD1_TYPE_RA)
            self.set_deg1(d1)
            self.set_min1(m1)
            self.set_sec1(s1)
            self.set_deg2(d2)
            self.set_min2(m2)
            self.set_sec2(s2)
            self.set_mode(mode)
        if self.is_horizon():
            if self.latitude is None:
                raise ValueError, "Invalid latitude!"
            self.__to_equatorial_from_horizon()
            mode = make_mode(COORD_MODE_EQUATORIAL, COORD1_UNIT_HOURS, COORD1_TYPE_HA)
            self.mode = mode
        if self.is_galactic():
            a1 = (self.get_dd1() - 33.0) * math.pi / 180.0
            a2 = self.get_dd2() * math.pi / 180.0
            a4 = math.asin((math.cos(a2) * 0.887815 * math.sin(a1)) + (math.sin(a2) * 0.4602)) * 180.0 / math.pi
            y = math.cos(a2) * math.cos(a1)
            x = (math.sin(a2) * 0.887815) - (math.cos(a2) * 0.4602 * math.sin(a1))
            a3 = math.atan2(y, x) * 180.0 / math.pi
            a3 += 192.25
            if a3 >= 360.0:
                a3 -= 360.0
            d1, m1, s1 = dms_from_dd(a3 / 15.0)
            d2, m2, s2 = dms_from_dd(a4)
            mode = make_mode(COORD_MODE_EQUATORIAL, COORD1_UNIT_HOURS, COORD1_TYPE_RA)
            self.set_deg1(d1)
            self.set_min1(m1)
            self.set_sec1(s1)
            self.set_deg2(d2)
            self.set_min2(m2)
            self.set_sec2(s2)
            self.set_mode(mode)

    def to_galactic(self):
        if self.is_ecliptic() or self.is_horizon():
            self.to_equatorial()
        if self.is_equatorial():
            if self.is_hour_angle():
                self.to_right_ascension()
            self.to_degrees()
            a1 = self.get_dd1() * math.pi / 180.0
            a2 = self.get_dd2() * math.pi / 180.0
            sin_b = (math.cos(a2) * 0.887815 * math.cos(a1 - 3.355395)) + (math.sin(a2) * 0.4602)
            a3 = math.asin(sin_b) * 180.0 / math.pi
            y = math.sin(a2) - (sin_b * 0.4602)
            x = math.cos(a2) * math.sin(a1 - 3.355395) * 0.887815
            a4 = math.atan2(y, x) * 180.0 / math.pi
            if a4 < 0.0:
                a4 += 360.0
            a4 += 33.0
            if a4 >= 360.0:
                a4 -= 360.0
            d1, m1, s1 = dms_from_dd(a4)
            d2, m2, s2 = dms_from_dd(a3)
            mode = make_mode(COORD_MODE_GALACTIC)
            self.set_deg1(d1)
            self.set_min1(m1)
            self.set_sec1(s1)
            self.set_deg2(d2)
            self.set_min2(m2)
            self.set_sec2(s2)
            self.set_mode(mode)

    def to_horizon(self):
        if self.is_ecliptic() or self.is_galactic():
            self.to_equatorial()
        if self.is_equatorial():
            self.__to_horizon_from_equatorial()
            mode = make_mode(COORD_MODE_HORIZON)
            self.set_mode(mode)

    def to_right_ascension(self):
        if not self.is_equatorial():
            raise ValueError, "Invalid coordinate! (Must be Equatorial)"
        if self.is_hour_angle():
            self.__equ_conv()
            mode_parts = split_mode(self.mode)
            mode = make_mode(mode_parts[0], mode_parts[1], COORD1_TYPE_RA)
            self.set_mode(mode)

    def __equ_conv(self):
        if self.date is None:
            raise ValueError, "Date (LST) is required!"
        self.date.to_lst()
        self.to_hours()
        a1 = self.get_dd1()
        a2 = self.date.get_decimal_hours()
        a3 = a2 - a1
        while a3 < 0.0:
            a3 += 24.0
        d, m, s = dms_from_dd(a3)
        self.set_deg1(d)
        self.set_min1(m)
        self.set_sec1(s)

    def __to_equatorial_from_horizon(self):
        alt_deg = self.get_dd1()
        alt_rad = alt_deg * math.pi / 180.0
        az_deg = self.get_dd2()
        az_rad = az_deg * math.pi / 180.0
        geolat_rad = self.latitude * math.pi / 180.0
        sin_alt = math.sin(alt_rad)
        sin_az = math.sin(az_rad)
        sin_geolat = math.sin(geolat_rad)
        cos_alt = math.cos(alt_rad)
        cos_az = math.cos(az_rad)
        cos_geolat = math.cos(geolat_rad)
        sin_dec = (sin_alt * sin_geolat) + (cos_alt * cos_geolat * cos_az)
        dec_rad = math.asin(sin_dec)
        cos_dec = math.cos(dec_rad)
        dec_deg = dec_rad * 180.0 / math.pi
        cos_ha = (sin_alt - (sin_geolat * sin_dec)) / (cos_geolat * cos_dec)
        ha_deg = math.acos(cos_ha) * 180.0 / math.pi
        if sin_az >= 0.0:
            ha_deg = 360.0 - ha_deg
        ha_deg /= 15.0
        d1, m1, s1 = dms_from_dd(ha_deg)
        d2, m2, s2 = dms_from_dd(dec_deg)
        self.set_deg1(d1)
        self.set_min1(m1)
        self.set_sec1(s1)
        self.set_deg2(d2)
        self.set_min2(m2)
        self.set_sec2(s2)

    def __to_horizon_from_equatorial(self):
        self.to_hours()
        self.to_hour_angle()
        self.to_degrees()
        ha_deg = self.get_dd1()
        ha_rad = ha_deg * math.pi / 180.0
        dec_deg = self.get_dd2()
        dec_rad = dec_deg * math.pi / 180.0
        geolat_rad = self.latitude * math.pi / 180.0
        sin_ha = math.sin(ha_rad)
        sin_dec = math.sin(dec_rad)
        sin_geolat = math.sin(geolat_rad)
        cos_ha = math.cos(ha_rad)
        cos_dec = math.cos(dec_rad)
        cos_geolat = math.cos(geolat_rad)
        sin_alt = (sin_dec * sin_geolat) + (cos_dec * cos_geolat * cos_ha)
        alt_rad = math.asin(sin_alt)
        cos_alt = math.cos(alt_rad)
        alt_deg = alt_rad * 180.0 / math.pi
        cos_az = (sin_dec - (sin_geolat * sin_alt)) / (cos_geolat * cos_alt)
        az_deg = math.acos(cos_az) * 180.0 / math.pi
        if sin_ha >= 0.0:
            az_deg = 360.0 - az_deg
        d1, m1, s1 = dms_from_dd(alt_deg)
        d2, m2, s2 = dms_from_dd(az_deg)
        self.set_deg1(d1)
        self.set_min1(m1)
        self.set_sec1(s1)
        self.set_deg2(d2)
        self.set_min2(m2)
        self.set_sec2(s2)


if __name__ == "__main__":


    coord = AstroCoord()

    Rigel_Coord_Hrs = (5.0, 14.0, 32.3, -8.0, 12.0, 5.9, make_mode(COORD_MODE_EQUATORIAL, COORD1_UNIT_HOURS, COORD1_TYPE_RA))
    coord.set_with_tuple(Rigel_Coord_Hrs)
    print(coord.get_pretty_string())
    print(coord.get_pretty_string("d"))
    print

    M87_Coord_Hrs = (12, 30, 49, 12, 23,7, make_mode(COORD_MODE_EQUATORIAL, COORD1_UNIT_HOURS, COORD1_TYPE_RA))
    coord.set_with_tuple(M87_Coord_Hrs)
    print(coord.get_pretty_string())
    print(coord.get_pretty_string("d"))
    print

    coord.to_degrees()
    print(coord.get_pretty_string())
    print(coord.get_pretty_string("d"))
