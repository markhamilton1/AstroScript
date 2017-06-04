import astrocoord
import astrodate
import earth
import math

# Sun Properties

SUN_MASS = 1.9891E30									# kg
SUN_VOLUME = 1.412E27									# m^3
SUN_EQUATORIAL_RADIUS = 6.955E8							# m
SUN_POLAR_RADIUS = 6356800.0							# m
SUN_MEAN_RADIUS = 6371000.0								# m
SUN_FLATTENING = 9E-6
SUN_MEAN_DENSITY = 1.408E3								# kg/m^3
SUN_SURFACE_GRAVITY = 27.94								# m/s^2 at equator
SUN_ESCAPE_VELOCITY = 617700.0							# m/s

#
# Sun CRN Calculations
#

def calculate_crn_with_dateTD(dat):
    jde = dat.get_julian()
    return calculate_crn_with_julianTD(jde)


def calculate_crn_with_julianTD(jde):
    """
    Calculate the Carrington rotation number (CRN).
    :param jde: 
    :return: 
    """
    d = (jde - 2444235.34 ) / 27.2753
    i = int(round(d))
    return 1690 + i

#
# Sun Position Calculations
#

VERNAL_EQUINOX = 0.0
SUMMER_SOLSTICE = 90.0
AUTUMNAL_EQUINOX = 180.0
WINTER_SOLSTICE = 270.0

class Position:

    def __init__(self):
        self.dL_FK5 = 0.0
        self.dL_ABERRATION = 0.0
        self.dB = 0.0
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.earth_position = None
        self.earth_nutation = None

    def calculate_aberration_with_julianTD(self, jde):
        t = (jde - astrodate.J2000) / 365250.0
        t2 = t * t
        t3 = t2 * t
        d = 3548.193 + \
            118.568 * math.sin((87.5287 + (359993.7286 * t)) * math.pi / 180.0) + \
            2.476 * math.sin((85.0561 + (719987.4571 * t)) * math.pi / 180.0) + \
            1.376 * math.sin((27.8502 + (4452671.1152 * t)) * math.pi / 180.0) + \
            0.119 * math.sin((73.1375 + (450368.8564 * t)) * math.pi / 180.0) + \
            0.114 * math.sin((337.2264 + (329644.6718 * t)) * math.pi / 180.0) + \
            0.086 * math.sin((222.54 + (659289.3436 * t)) * math.pi / 180.0) + \
            0.078 * math.sin((162.8136 + (9224659.7915 * t)) * math.pi / 180.0) + \
            0.054 * math.sin((82.5823 + (1079981.1857 * t)) * math.pi / 180.0) + \
            0.052 * math.sin((171.5189 + (225184.4282 * t)) * math.pi / 180.0) + \
            0.034 * math.sin((30.3214 + (4092677.3866 * t)) * math.pi / 180.0) + \
            0.033 * math.sin((119.8105 + (337181.4711 * t)) * math.pi / 180.0) + \
            0.023 * math.sin((247.5418 + (299295.6151 * t)) * math.pi / 180.0) + \
            0.023 * math.sin((325.1526 + (315559.556 * t)) * math.pi / 180.0) + \
            0.021 * math.sin((155.1241 + (675553.2846 * t)) * math.pi / 180.0) + \
            (7.311 * t) * math.sin((333.4515 + (359993.7286 * t)) * math.pi / 180.0) + \
            (0.305 * t) * math.sin((330.9814 + (719987.4571 * t)) * math.pi / 180.0) + \
            (0.01 * t) * math.sin((328.517 + (1079981.1857 * t)) * math.pi / 180.0) + \
            (0.309 * t2) * math.sin((241.4518 + (359993.7286 * t)) * math.pi / 180.0) + \
            (0.021 * t2) * math.sin((205.0482 + (719987.4571 * t)) * math.pi / 180.0) + \
            (0.004 * t2) * math.sin((297.861 + (4452671.1152 * t)) * math.pi / 180.0) + \
            (0.01 * t3) * math.sin((154.7066 + (359993.7286 * t)) * math.pi / 180.0)
        a = -0.005775518 * self.get_earth_sun_radius() * d
        return a

    def calculate_approximate_season_start(self, year, season):
        jde0 = 0.0
        year = int(year)
        if (year >= -1000) and (year < 1000):
            yr = year / 1000.0
            if season == VERNAL_EQUINOX:
                jde0 = (((((((-0.00071 * yr) + 0.00111) * yr) + 0.06134) * yr) + 365242.1374) * yr) + 1721139.29189
            elif season == SUMMER_SOLSTICE:
                jde0 = (((((((0.00025 * yr) + 0.00907) * yr) - 0.05323) * yr) + 365241.72562) * yr) + 1721233.25401
            elif season == AUTUMNAL_EQUINOX:
                jde0 = (((((((0.00074 * yr) - 0.00297) * yr) - 0.11677) * yr) + 365242.49558) * yr) + 1721325.70455
            elif season == WINTER_SOLSTICE:
                jde0 = (((((((-0.00006 * yr) - 0.00933) * yr) - 0.00769) * yr) + 365242.88257) * yr) + 1721414.39987
        elif (year >= 1000) and (year <= 3000):
            yr = (year - 2000) / 1000.0
            if season == VERNAL_EQUINOX:
                jde0 = (((((((-0.00057 * yr) - 0.00411) * yr) + 0.05169) * yr) + 365242.37404) * yr) + 2451623.80984
            elif season == SUMMER_SOLSTICE:
                jde0 = (((((((-0.0003 * yr) + 0.00888) * yr) + 0.00325) * yr) + 365241.62603) * yr) + 2451716.56767
            elif season == AUTUMNAL_EQUINOX:
                jde0 = (((((((0.00078 * yr) + 0.00337) * yr) - 0.11575) * yr) + 365242.01767) * yr) + 2451810.21715
            elif season == WINTER_SOLSTICE:
                jde0 = (((((((0.00032 * yr) - 0.00823) * yr) - 0.06223) * yr) + 365242.74049) * yr) + 2451900.05952
        return jde0

    def calculate_eccentricity_of_orbit_with_julianTD(self, jde1900):
        return 0.01675104 + (jde1900 * (-0.0000418 + (jde1900 * -0.000000126)))

    def calculate_ecliptic_longitude_of_perigee_with_julianTD(self, jde1900):
        return 281.2208444 + (jde1900 * (1.719175 + (jde1900 * 0.000452778)))

    def calculate_mean_ecliptic_longitude_with_julianTD(self, jde1900):
        return 279.6966778 + (jde1900 * (36000.76892 + (jde1900 * 0.0003025)))

    def calculate_position_with_dateTD(self, dateTD, useSun2000=False):
        if dateTD is None:
            raise ValueError, "Date (TD) is required!"
        dateTD.to_td()
        jde = dateTD.get_julian()
        self.calculate_position_with_julianTD(jde, useSun2000)

    def calculate_position_with_julianTD(self, jde, useSun2000=False):
        self.earth_position = earth.calculate_position_with_julianTD(jde)
        self.earth_nutation = earth.Nutation()
        self.earth_nutation.calculate_with_julianTD(jde)
        t = (jde - astrodate.J2000) / 36525.0
        Lp = (self.get_true_longitude() + (((-0.00031 * t) - 1.397) * t)) * math.pi / 180.0
        self.dL_FK5 = -0.09033 / 3600.0
        self.dL_ABERRATION = self.calculate_aberration_with_julianTD(jde) / 3600.0
        self.dB = (0.03916 * (math.cos(Lp) - math.sin(Lp))) / 3600.0
        self.calculate_xyz(useSun2000)

    def calculate_season_start(self, year, season, useSun2000=False):
        jde = self.calculate_approximate_season_start(year, season)
        if jde != 0.0:
            djde = 0.0
            while True:
                jde += djde
                self.calculate_position_with_julianTD(jde, useSun2000)
                ap_long = self.get_apparent_longitude()
                djde = 58.0 * math.sin(season - ap_long) * math.pi / 180.0
                adjde = abs(djde)
                if adjde < 0.000005:
                    break
        return jde

    def calculate_xyz(self, useSun2000=False):
        toRad = math.pi / 180.0
        lat = self.get_latitude() * toRad
        lng = self.get_true_longitude() * toRad
        cosLat = math.cos(lat)
        sinLat = math.sin(lat)
        cosLong = math.cos(lng)
        sinLong = math.sin(lng)
        r = self.earth_position.get_radius()
        self.x = r * cosLat * cosLong
        if useSun2000:
            self.y = r * cosLat * sinLong
            self.z = r * sinLat
        else:
            mo = self.earth_nutation.get_mean_obliquity() * toRad
            cosMObl = math.cos(mo)
            sinMObl = math.sin(mo)
            cosLatSinLong = cosLat * sinLong
            self.y = r * ((cosLatSinLong * cosMObl) - (sinLat * sinMObl))
            self.z = r * ((cosLatSinLong * sinMObl) - (sinLat * cosMObl))

    def get_apparent_longitude(self):
        tr_long = self.get_true_longitude()
        ea_nut = self.earth_nutation.get_nutation_in_longitude()
        aber = self.dL_ABERRATION
        l = tr_long + ea_nut + aber
        if l >= 360.0:
            l -= 360.0
        return l

    def get_earth_sun_radius(self):
        return self.earth_position.get_radius()

    def get_ecliptic_coordinate(self, apparent):
        if apparent:
            lng = self.get_apparent_longitude()
            lat = self.get_latitude()
        else:
            lng = self.get_true_longitude()
            lat = self.get_latitude()
        mode = astrocoord.make_mode(astrocoord.COORD_MODE_ECLIPTIC)
        c = astrocoord.AstroCoord().alloc_with_degrees(lng, lat, mode)
        return c

    def get_equatorial_ra(self, apparent, epochTD):
        c = self.get_ecliptic_coordinate(apparent)
        c.to_equatorial(epochTD)
        return c

    def get_latitude(self):
        return self.get_latitude0() + self.dB

    def get_latitude0(self):
        return -self.earth_position.get_latitude0()

    def get_true_longitude(self):
        return self.get_true_longitude0() + self.dL_FK5

    def get_true_longitude0(self):
        l = self.earth_position.get_longitude0() + 180.0
        if l >= 360.0:
            l -= 360.0
        return l

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z


def calculate_position_with_dateTD(dateTD):
    p = Position()
    p.calculate_position_with_dateTD(dateTD)
    return p


def calculate_position_with_julianTD(jde):
    p = Position()
    p.calculate_position_with_julianTD(jde)
    return p


if __name__ == "__main__":


    jde = 2448908.5
    p = calculate_position_with_julianTD(jde)
    print("Latitude0: {}".format(p.get_latitude0()))
    print("Latitude: {}".format(p.get_latitude()))
    print("Apparent Longitude: {}".format(p.get_apparent_longitude()))
    print("True Longitude0: {}".format(p.get_true_longitude0()))
    print("True Longitude: {}".format(p.get_true_longitude()))
    print("Radius: {}".format(p.get_earth_sun_radius()))
    
    print

    year = 2017
    ad = astrodate.AstroDate().alloc_now_utc()

    jdve = p.calculate_season_start(year, VERNAL_EQUINOX)
    ad.set_with_julian(jdve, astrodate.TIME_MODE_TDT)
    ve = ad.get_pretty_string()
    print("Vernal Equinox: {} ({})".format(ve, jdve))

    jdss = p.calculate_season_start(year, SUMMER_SOLSTICE)
    ad.set_with_julian(jdss, astrodate.TIME_MODE_TDT)
    ss = ad.get_pretty_string()
    print("Summer Solstice: {} ({})".format(ss, jdss))

    jdae = p.calculate_season_start(year, AUTUMNAL_EQUINOX)
    ad.set_with_julian(jdae, astrodate.TIME_MODE_TDT)
    ae = ad.get_pretty_string()
    print("Autumnal Equinox: {} ({})".format(ae, jdae))

    jdws = p.calculate_season_start(year, WINTER_SOLSTICE)
    ad.set_with_julian(jdws, astrodate.TIME_MODE_TDT)
    ws = ad.get_pretty_string()
    print("Winter Solstice: {} ({})".format(ws, jdws))
    
    