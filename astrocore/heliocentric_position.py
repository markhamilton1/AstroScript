import astrodate
import math
import mathutils


# ftp://ftp.imcce.fr/pub/ephem/planets/vsop87


class Position:

    def __init__(self):
        self.T = 0.0
        self.L = 0.0
        self.B = 0.0
        self.R = 0.0
        self.dL = 0.0
        self.dB = 0.0

    def __calculate_cos_component(self, terms):
        v = 0.0
        for i in xrange(0, len(terms)):
            ta = terms[i][0]
            tb = terms[i][1]
            tc = terms[i][2]
            v += ta * math.cos(tb + (tc * self.T))
        return v

    def __calculate_series(self, terms):
        v = 0.0
        for i in xrange(len(terms) - 1, -1, -1):
            v += (v * self.T) + self.__calculate_cos_component(terms[i])
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

    def calculate_with_dateTD_terms(self, dateTD, terms):
        """
        Calculate the position properties for Mercury.
        :param dat: the date (in dynamical time)
        """
        if dateTD.is_td():
            self.calculate_with_julian_terms(dateTD.get_julian(), terms)
        else:
            raise ValueError, "Invalid date mode! Must be TD."

    def calculate_with_julian_terms(self, jde, terms):
        toRad = math.pi / 180.0
        self.T = (jde - astrodate.J2000) / 365250.0
        self.__calculate_L(terms[0])
        self.__calculate_B(terms[1])
        self.__calculate_R(terms[2])
        t = self.T * 10.0
        Lp = (self.L + (((-0.00031 * t) - 1.397) * t)) * toRad
        self.dL = (-0.09033 + (0.03916 * (math.cos(Lp) + math.sin(Lp)) * math.tan(self.B * toRad))) / 3600.0
        self.dB = (0.03916 * (math.cos(Lp) - math.sin(Lp))) / 3600.0

    def get_latitude0(self):
        return self.B

    def get_latitude(self):
        return self.B + self.dB

    def get_longitude0(self):
        return self.L

    def get_longitude(self):
        return self.L + self.dL

    def get_radius(self):
        return self.R
