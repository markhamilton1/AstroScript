"""
Calculate the heliocentric position of a planet using the VSOP87 ephemeris technique.
The original planetary ephemeris can be found at:

ftp://ftp.imcce.fr/pub/ephem/planets/vsop87

This implementation uses the heliocentric ephemerides of the VSOP87D files.

The computed positions of the planets can be compared to the values returned at this website:

https://omniweb.gsfc.nasa.gov/coho/helios/planet.html
"""

import astrodate
import math
import mathutils


class Position:

    def __init__(self, terms):
        self.terms = terms
        self.T = 0.0
        self.L = 0.0
        self.B = 0.0
        self.R = 0.0
        self.dL = 0.0
        self.dB = 0.0

    def __calculate_cos_component(self, terms):
        v = 0.0
        for i in range(0, len(terms)):
            ta = terms[i][0]
            tb = terms[i][1]
            tc = terms[i][2]
            v += ta * math.cos(tb + (tc * self.T))
        return v

    def __calculate_series(self, terms):
        v = 0.0
        t = 0.0
        for i in range(0, len(terms)):
            c = self.__calculate_cos_component(terms[i])
            t = self.T ** i
            v += t * c
        return v

    def __calculate_B(self, terms):
        tB = self.__calculate_series(terms)
        tB *= 180.0 / math.pi
        self.B = mathutils.normalize_degrees(tB, -360.0, 360.0)

    def __calculate_L(self, terms):
        tL = self.__calculate_series(terms)
        tL *= 180.0 / math.pi
        self.L = mathutils.normalize_degrees(tL)

    def __calculate_R(self, terms):
        self.R = self.__calculate_series(terms)

    def calculate_with_dateTD(self, dateTD):
        """
        Calculate the position properties for a solar body (in the standard FK5 system).
        :param dateTD: the date (in dynamical time)
        """
        if dateTD.is_td():
            self.calculate_with_julianTD(dateTD.get_julian())
        else:
            raise ValueError, "Invalid date mode! Must be TD."

    def calculate_with_julianTD(self, jde):
        """
        Calculate the position properties for a solar body (in the standard FK5 system).
        :param jde: the julian date (in dynamical time)
        """
        toRad = math.pi / 180.0
        self.T = (jde - astrodate.J2000) / 365250.0
        self.__calculate_L(self.terms[0])
        self.__calculate_B(self.terms[1])
        self.__calculate_R(self.terms[2])
        t = self.T * 10.0
        Lp = (self.L + (((-0.00031 * t) - 1.397) * t)) * toRad
        self.dL = (-0.09033 + (0.03916 * (math.cos(Lp) + math.sin(Lp)) * math.tan(self.B * toRad))) / 3600.0
        self.dB = (0.03916 * (math.cos(Lp) - math.sin(Lp))) / 3600.0

    def get_latitude0(self):
        """
        Get the mean ecliptical latitude (in degrees).
        :return: the mean latitude
        """
        return self.B

    def get_latitude(self):
        """
        Get the corrected ecliptical latitude (in degrees).
        :return: the corrected latitude
        """
        return self.B + self.dB

    def get_longitude0(self):
        """
        Get the mean ecliptical longitude (in degrees).
        :return: the mean longitude
        """
        return self.L

    def get_longitude(self):
        """
        Get the corrected ecliptical longitude (in degrees).
        :return: the corrected longitude
        """
        return self.L + self.dL

    def get_radius(self):
        """
        Get the radius (in astronomical units).
        :return: the radius
        """
        return self.R
