import astrodate
import deltat
import math
import mathutils
import sun

#
# Earth Properties
#

EARTH_MASS = 5.9736E24 									        # kg
EARTH_VOLUME = 1.0832073E21     								# m^3
EARTH_EQUATORIAL_RADIUS = 6378140.0     						# m
EARTH_POLAR_RADIUS = 6356800.0      							# m
EARTH_MEAN_RADIUS = 6371000.0       							# m
EARTH_FLATTENING = EARTH_POLAR_RADIUS/EARTH_EQUATORIAL_RADIUS
EARTH_MEAN_DENSITY = 5515.3     								# kg/m^3
EARTH_SURFACE_GRAVITY = 9.780327        						# m/s^2 at equator
EARTH_ESCAPE_VELOCITY = 11186.0     							# m/s
EARTH_SIDEREAL_ORBIT_PERIOD = 365.256       					# days
EARTH_MEAN_ORBITAL_VELOCITY = 29783.0       					# m/s
EARTH_SIDEREAL_ROTATION_PERIOD = 23.9345        				# hours

#
# Earth Nutation and Obliquity Calculations
#

N_TERMS = 63
C_MEMS = [
    0.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0,  0.0,  0.0, -2.0,
    -2.0, -2.0,  0.0,  2.0,  0.0,  2.0,  0.0,  0.0, -2.0,  0.0,
    2.0,  0.0,  0.0, -2.0,  0.0, -2.0,  0.0,  0.0,  2.0, -2.0,
    0.0, -2.0,  0.0,  0.0,  2.0,  2.0,  0.0, -2.0,  0.0,  2.0,
    2.0, -2.0, -2.0,  2.0,  2.0,  0.0, -2.0, -2.0,  0.0, -2.0,
    -2.0,  0.0, -1.0, -2.0,  1.0,  0.0,  0.0, -1.0,  0.0,  0.0,
    2.0,  0.0,  2.0
]
C_MAS = [
    0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  1.0,  0.0,  0.0, -1.0,
    0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
    0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  2.0,  0.0,  2.0,
    1.0,  0.0, -1.0,  0.0,  0.0,  0.0,  1.0,  1.0, -1.0,  0.0,
    0.0,  0.0,  0.0,  0.0,  0.0, -1.0, -1.0,  0.0,  0.0,  0.0,
    1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0, -1.0,  1.0, -1.0,
    -1.0,  0.0, -1.0
]
C_MAM = [
    0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  0.0,
    1.0,  0.0, -1.0,  0.0,  1.0, -1.0, -1.0,  1.0,  2.0, -2.0,
    0.0,  2.0,  2.0,  1.0,  0.0,  0.0, -1.0,  0.0, -1.0,  0.0,
    0.0,  1.0,  0.0,  2.0, -1.0,  1.0,  0.0,  1.0,  0.0,  0.0,
    1.0,  2.0,  1.0, -2.0,  0.0,  1.0,  0.0,  0.0,  2.0,  2.0,
    0.0,  1.0,  1.0,  0.0,  0.0,  1.0, -2.0,  1.0,  1.0,  1.0,
    -1.0,  3.0,  0.0
]
C_MAL = [
    0.0,  2.0,  2.0,  0.0,  0.0,  0.0,  2.0,  2.0,  2.0,  2.0,
    0.0,  2.0,  2.0,  0.0,  0.0,  2.0,  0.0,  2.0,  0.0,  2.0,
    2.0,  2.0,  0.0,  2.0,  2.0,  2.0,  2.0,  0.0,  0.0,  2.0,
    0.0,  0.0,  0.0, -2.0,  2.0,  2.0,  2.0,  0.0,  2.0,  2.0,
    0.0,  2.0,  2.0,  0.0,  0.0,  0.0,  2.0,  0.0,  2.0,  0.0,
    2.0, -2.0,  0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  2.0,
    2.0,  2.0,  2.0
]
C_LAN_MOE = [
    1.0,  2.0,  2.0,  2.0,  0.0,  0.0,  2.0,  1.0,  2.0,  2.0,
    0.0,  1.0,  2.0,  0.0,  1.0,  2.0,  1.0,  1.0,  0.0,  1.0,
    2.0,  2.0,  0.0,  2.0,  0.0,  0.0,  1.0,  0.0,  1.0,  2.0,
    1.0,  1.0,  1.0,  0.0,  1.0,  2.0,  2.0,  0.0,  2.0,  1.0,
    0.0,  2.0,  1.0,  1.0,  1.0,  0.0,  1.0,  1.0,  1.0,  1.0,
    1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  2.0,  0.0,  0.0,  2.0,
    2.0,  2.0,  2.0
]
C_SIN = [
    -17.1996,  -1.3187,  -0.2274,   0.2062,   0.1426,   0.0712,  -0.0517,  -0.0386,  -0.0301,   0.0217,
     -0.0158,   0.0129,   0.0123,   0.0063,   0.0063,  -0.0059,  -0.0058,  -0.0051,   0.0048,   0.0046,
     -0.0038,  -0.0031,   0.0029,   0.0029,   0.0026,  -0.0022,   0.0021,   0.0017,   0.0016,  -0.0016,
     -0.0015,  -0.0013,  -0.0012,   0.0011,  -0.0010,  -0.0008,   0.0007,  -0.0007,  -0.0007,  -0.0007,
      0.0006,   0.0006,   0.0006,  -0.0006,  -0.0006,   0.0005,  -0.0005,  -0.0005,  -0.0005,   0.0004,
      0.0004,   0.0004,  -0.0004,  -0.0004,  -0.0004,   0.0003,  -0.0003,  -0.0003,  -0.0003,  -0.0003,
     -0.0003,  -0.0003,  -0.0003
]
C_COS = [
    9.2025,  0.5736,  0.0977, -0.0895,  0.0054, -0.0007,  0.0224,  0.0200,  0.0129, -0.0095,
    0.0000, -0.0070, -0.0053,  0.0000, -0.0033,  0.0026,  0.0032,  0.0027,  0.0000, -0.0024,
    0.0016,  0.0013,  0.0000, -0.0012,  0.0000,  0.0000, -0.0010,  0.0000, -0.0008,  0.0007,
    0.0009,  0.0007,  0.0006,  0.0000,  0.0005,  0.0003, -0.0003,  0.0000,  0.0003,  0.0003,
    0.0000, -0.0003, -0.0003,  0.0003,  0.0003,  0.0000,  0.0003,  0.0003,  0.0003,  0.0000,
    0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,
    0.0000,  0.0000,  0.0000
]

class Nutation:

    def __init__(self):
        self.NUTATION_IN_LONGITUDE = 0.0
        self.NUTATION_IN_OBLIQUITY = 0.0
        self.MEAN_OBLIQUITY = 0.0

    def calculate_with_julianTD(self, jde_td):
        """
        Calculate the properties of nutation for the provided date.
        :param jde_td: the date (julian date in dynamical time)
        """
        # calculate the time, T, measured in julian centuries from J2000.0
        T = (jde_td - astrodate.J2000) / 36525.0
        # calculate the Mean Elongation of the Moon from the Sun
        MEMS = (((((T / 189474.0) - 0.0019142) * T) + 445267.11148) * T) + 297.85036
        # calculate the Mean Anomaly of the Sun
        MAS = (((((-T / 300000.0) - 0.0001603) * T) + 35999.05034) * T) + 357.52772
        # calculate the Mean Anomaly of the Moon
        MAM = (((((T / 56250.0) + 0.0086972) * T) + 477198.867398) * T) + 134.96298
        # calculate the Moon's Argument of Latitude
        MAL = (((((T / 327270.0) - 0.0036825) * T) + 483202.017538) * T) + 93.27191
        # calculate the Longitude of the  Ascending Node of the Moon's Mean Orbit on the Ecliptic
        LANMMOE = (((((T / 450000.0) + 0.0020708) * T) - 1934.136261) * T) + 125.04452
        # calculate the nutation
        tNUTATION_IN_LONGITUDE = 0.0
        tNUTATION_IN_OBLIQUITY = 0.0
        for i in xrange(0, N_TERMS):
            a = 0.0
            if C_MEMS[i] != 0.0:
                a += C_MEMS[i] * MEMS
            if C_MAS[i] != 0.0:
                a += C_MAS[i] * MAS
            if C_MAM[i] != 0.0:
                a += C_MAM[i] * MAM
            if C_MAL[i] != 0.0:
                a += C_MAL[i] * MAL
            if C_LAN_MOE[i] != 0.0:
                a += C_LAN_MOE[i] * LANMMOE
            a = a * math.pi / 180.0
            if C_SIN[i] != 0.0:
                tNUTATION_IN_LONGITUDE += C_SIN[i] * math.sin(a)
            if C_COS[i] != 0.0:
                tNUTATION_IN_OBLIQUITY += C_COS[i] * math.cos(a)
        self.NUTATION_IN_LONGITUDE = tNUTATION_IN_LONGITUDE / 3600.0
        self.NUTATION_IN_OBLIQUITY = tNUTATION_IN_OBLIQUITY / 3600.0
        # calculate the Mean Obliquity
        U = T / 100.0
        tMEAN_OBLIQUITY = (2.45 * U) + 5.79
        tMEAN_OBLIQUITY = (tMEAN_OBLIQUITY * U) + 27.87
        tMEAN_OBLIQUITY = (tMEAN_OBLIQUITY * U) + 7.12
        tMEAN_OBLIQUITY = (tMEAN_OBLIQUITY * U) - 39.05
        tMEAN_OBLIQUITY = (tMEAN_OBLIQUITY * U) - 249.67
        tMEAN_OBLIQUITY = (tMEAN_OBLIQUITY * U) - 51.38
        tMEAN_OBLIQUITY = (tMEAN_OBLIQUITY * U) + 1999.25
        tMEAN_OBLIQUITY = (tMEAN_OBLIQUITY * U) - 1.55
        tMEAN_OBLIQUITY = (tMEAN_OBLIQUITY * U) - 4680.93
        self.MEAN_OBLIQUITY = ((tMEAN_OBLIQUITY * U) + 84381.448) / 3600.0

    def get_mean_obliquity(self):
        """
        Get the mean obliquity in degrees.
        :return: the mean obliquity
        """
        return self.MEAN_OBLIQUITY

    def get_nutation_in_longitude(self):
        """
        Get the nutation in longitude in degrees.
        :return: the nutation in longitude
        """
        return self.NUTATION_IN_LONGITUDE

    def get_nutation_in_obliquity(self):
        """
        Get the nutation in obliquity in degrees.
        :return: the nutation in obliquity
        """
        return self.NUTATION_IN_OBLIQUITY

    def get_true_obliquity(self):
        """
        Get the true obliquity in degrees.
        :return: the true obliquity
        """
        return self.MEAN_OBLIQUITY + self.NUTATION_IN_OBLIQUITY

#
# Earth Heliocentric Position Calculations
#

L0a = [
    175347046.0, 3341656.0, 34894.0, 3497.0, 3418.0, 3136.0, 2676.0, 2343.0, 1324.0, 1273.0,
    1199.0, 990.0, 902.0, 857.0, 780.0, 753.0, 505.0, 492.0, 357.0, 317.0,
    284.0, 271.0, 243.0, 206.0, 205.0, 202.0, 156.0, 132.0, 126.0, 115.0,
    103.0, 102.0, 102.0, 99.0, 98.0, 86.0, 85.0, 85.0, 80.0, 79.0,
    75.0, 74.0, 74.0, 70.0, 62.0, 61.0, 57.0, 56.0, 56.0, 52.0,
    52.0, 51.0, 49.0, 41.0, 41.0, 39.0, 37.0, 37.0, 36.0, 36.0,
    33.0, 30.0, 30.0, 25.0
]
L0b = [
    0.0, 4.6692568, 4.6261, 2.7441, 2.8289, 3.6277, 4.4181, 6.1352, 0.7425, 2.0371,
    1.1096, 5.233, 2.045, 3.508, 1.179, 2.533, 4.583, 4.205, 2.92, 5.849,
    1.899, 0.315, 0.345, 4.806, 1.869, 2.458, 0.833, 3.411, 1.083, 0.645,
    0.636, 0.976, 4.267, 6.21, 0.68, 5.98, 1.3, 3.67, 1.81, 3.04,
    1.76, 3.5, 4.68, 0.83, 3.98, 1.82, 2.78, 4.39, 3.47, 0.19,
    1.33, 0.28, 0.49, 5.37, 2.4, 6.17, 6.04, 2.57, 1.71, 1.78,
    0.59, 0.44, 2.74, 3.16
]
L0c = [
    0.0, 6283.07585, 12566.1517, 5753.3849, 3.5231, 77713.7715, 7860.4194, 3930.2097, 11506.7698, 529.691,
    1577.3435, 5884.927, 26.298, 398.149, 5223.694, 5507.553, 18849.228, 775.523, 0.067, 11790.629,
    796.298, 10977.079, 5486.778, 2544.314, 5573.143, 6069.777, 213.299, 2942.463, 20.775, 0.98,
    4694.003, 15720.839, 7.114, 2146.17, 155.42, 161000.69, 6275.96, 71430.7, 17260.15, 12036.46,
    5088.63, 3154.69, 801.82, 9437.76, 8827.39, 7084.9, 6286.6, 14143.5, 6279.55, 12139.55,
    1748.02, 5856.48, 1194.45, 8429.24, 19651.05, 10447.39, 10213.29, 1059.38, 2352.87, 6812.77,
    17789.85, 83996.85, 1349.87, 4690.48
]

L1a = [
    628331966747.0, 206059.0, 4303.0, 425.0, 119.0, 109.0, 93.0, 72.0, 68.0, 67.0,
    59.0, 56.0, 45.0, 36.0, 29.0, 21.0, 19.0, 19.0, 17.0, 16.0,
    16.0, 15.0, 12.0, 12.0, 12.0, 12.0, 11.0, 10.0, 10.0, 9.0,
    9.0, 8.0, 6.0, 6.0
]
L1b = [
    0.0, 2.678235, 2.6351, 1.59, 5.796, 2.966, 2.59, 1.14, 1.87, 4.41,
    2.89, 2.17, 0.4, 0.47, 2.65, 5.34, 1.85, 4.97, 2.99, 0.03,
    1.43, 1.21, 2.83, 3.26, 5.27, 2.08, 0.77, 1.3, 4.24, 2.7,
    5.64, 5.3, 2.65, 4.67
]
L1c = [
    0.0, 6283.07585, 12566.1517, 3.523, 26.298, 1577.344, 18849.23, 529.69, 398.15, 5507.55,
    5223.69, 155.42, 796.3, 775.52, 7.11, 0.98, 5486.78, 213.3, 6275.96, 2544.31,
    2146.17, 10977.08, 1748.02, 5088.63, 1194.45, 4694.0, 553.57, 6286.6, 1349.87, 242.73,
    951.72, 2352.87, 9437.76, 4690.48
]

L2a = [
    52919.0, 8720.0, 309.0, 27.0, 16.0, 16.0, 10.0, 9.0, 7.0, 5.0,
    4.0, 4.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.0, 2.0
]
L2b = [
    0.0, 1.0721, 0.867, 0.05, 5.19, 3.68, 0.76, 2.06, 0.83, 4.66,
    1.03, 3.44, 5.14, 6.05, 1.19, 6.12, 0.31, 2.28, 4.38, 3.75
]
L2c = [
    0.0, 6283.0758, 12566.152, 3.52, 26.3, 155.42, 18849.23, 77713.77, 775.52, 1577.34,
    7.11, 5573.14, 796.3, 5507.55, 242.73, 529.69, 398.15, 553.57, 5223.69, 0.98
]

L3a = [289.0, 35.0, 17.0, 3.0, 1.0, 1.0, 1.0]
L3b = [5.844, 0.0, 5.49, 5.2, 4.72, 5.3, 5.97]
L3c = [6283.076, 0.0, 12566.15, 155.42, 3.52, 18849.23, 242.73]

L4a = [114.0, 8.0, 1.0]
L4b = [3.142, 4.13, 3.84]
L4c = [0.0, 6283.08, 12566.15]

L5a = [1.0]
L5b = [3.14]
L5c = [0.0]


L1a2000 = [
    628307584999.0, 206059.0, 4303.0, 425.0, 119.0, 109.0, 93.0, 72.0, 68.0, 67.0,
    59.0, 56.0, 45.0, 36.0, 29.0, 21.0, 19.0, 19.0, 17.0, 16.0,
    16.0, 15.0, 12.0, 12.0, 12.0, 12.0, 11.0, 10.0, 10.0, 9.0,
    9.0, 8.0, 6.0, 6.0
]

L2a2000 = [
    8722.0, 991.0, 295.0, 27.0, 16.0, 16.0, 9.0, 9.0, 7.0, 5.0,
    4.0, 4.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.0, 2.0
]
L2b2000 = [
    1.0725, 3.1416, 0.437, 0.05, 5.19, 3.69, 0.3, 2.06, 0.83, 4.66,
    1.03, 3.44, 5.14, 6.05, 1.19, 6.12, 0.3, 2.28, 4.38, 3.75
]
L2c2000 = [
    6283.0758, 0.0, 12566.152, 3.52, 26.3, 155.42, 18849.23, 77713.77, 775.52, 1577.34,
    7.11, 5573.14, 796.3, 5507.55, 242.73, 529.69, 398.15, 553.57, 5223.69, 0.98
]

L3a2000 = [289.0, 21.0, 3.0, 3.0, 1.0, 1.0, 1.0]
L3b2000 = [5.842, 6.05, 5.2, 3.14, 4.72, 5.97, 5.54]
L3c2000 = [6283.076, 12566.15, 155.42, 0.0, 3.52, 242.73, 18849.23]

L4a2000 = [8.0, 1.0]
L4b2000 = [4.14, 3.28]
L4c2000 = [6283.08, 12566.15]


# terms to calculate Earth's heliocentric ecliptical latitude
B0a = [280.0, 102.0, 80.0, 44.0, 32.0]
B0b = [3.199, 5.422, 3.88, 3.7, 4.0]
B0c = [84334.663, 5507.553, 5223.69, 2352.87, 1577.34]

B1a = [9.0, 6.0]
B1b = [3.9, 1.73]
B1c = [5507.55, 5223.69]

B1a2000 = [227778.0, 3806.0, 3620.0, 72.0, 8.0, 8.0, 6.0]
B1b2000 = [3.413766, 3.3706, 0.0, 3.33, 3.89, 1.79, 5.2]
B1c2000 = [6283.07585, 12566.1517, 0.0, 18849.23, 5507.55, 5223.69, 2352.87]

B2a2000 = [9721.0, 233.0, 134.0, 7.0]
B2b2000 = [5.1519, 3.1416, 0.644, 1.07]
B2c2000 = [6283.07585, 0.0, 12566.152, 18849.23]

B3a2000 = [276.0, 17.0, 4.0]
B3b2000 = [0.595, 3.14, 0.12]
B3c2000 = [6283.076, 0.0, 12566.15]

B4a2000 = [6.0, 1.0]
B4b2000 = [2.27, 0.0]
B4c2000 = [6283.08, 0.0]


# terms to calculate Earth's distance from the Sun
R0a = [
    100013989.0, 1670700.0, 13956.0, 3084.0, 1628.0, 1576.0, 925.0, 542.0, 472.0, 346.0,
    329.0, 307.0, 243.0, 212.0, 186.0, 175.0, 110.0, 98.0, 86.0, 86.0,
    65.0, 63.0, 57.0, 56.0, 49.0, 47.0, 45.0, 43.0, 39.0, 38.0,
    37.0, 37.0, 36.0, 35.0, 33.0, 32.0, 32.0, 28.0, 28.0, 26.0
]
R0b = [
    0.0, 3.0984635, 3.05525, 5.1985, 1.1739, 2.8469, 5.453, 4.564, 3.661, 0.964,
    5.9, 0.299, 4.273, 5.847, 5.022, 3.012, 5.055, 0.89, 5.69, 1.27,
    0.27, 0.92, 2.01, 5.24, 3.25, 2.58, 5.54, 6.01, 5.36, 2.39,
    0.83, 4.9, 1.67, 1.84, 0.24, 0.18, 1.78, 1.21, 1.9, 4.59
]
R0c = [
    0.0, 6283.07585, 12566.1517, 77713.7715, 5753.3849, 7860.4194, 11506.77, 3930.21, 5884.927, 5507.553,
    5223.694, 5573.143, 11790.629, 1577.344, 10977.079, 18849.228, 5486.778, 6069.78, 15720.84, 16100.69,
    17260.15, 529.69, 83996.85, 71430.7, 2544.31, 775.52, 9437.76, 6275.96, 4694.0, 8827.39,
    19651.05, 12139.55, 12036.46, 2942.46, 7084.9, 5088.63, 398.15, 6286.6, 6279.55, 10447.39
]


R1a = [103019.0, 1721.0, 702.0, 32.0, 31.0, 25.0, 18.0, 10.0, 9.0, 9.0]
R1b = [1.10749, 1.0644, 3.142, 1.02, 2.84, 1.32, 1.42, 5.91, 1.42, 0.27]
R1c = [6283.07585, 12566.1517, 0.0, 18849.23, 5507.55, 5223.69, 1577.34, 10977.08, 6275.96, 5486.78]

R2a = [4359.0, 124.0, 12.0, 9.0, 6.0, 3.0]
R2b = [5.7846, 5.579, 3.14, 3.63, 1.87, 5.47]
R2c = [6283.0758, 12566.152, 0.0, 77713.77, 5573.14, 18849.23]

R3a = [145.0, 7.0]
R3b = [4.273, 3.92]
R3c = [6283.076, 12566.15]

R4a = [4.0]
R4b = [2.56]
R4c = [6283.08]


L0 = [L0a, L0b, L0c]
L1 = [L1a, L1b, L1c]
L2 = [L2a, L2b, L2c]
L3 = [L3a, L3b, L3c]
L4 = [L4a, L4b, L4c]
L5 = [L5a, L5b, L5c]

L1_2000 = [L1a2000, L1b, L1c]
L2_2000 = [L2a2000, L2b2000, L2c2000]
L3_2000 = [L3a2000, L3b2000, L3c2000]
L4_2000 = [L4a2000, L4b2000, L4c2000]

B0 = [B0a, B0b, B0c]
B1 = [B1a, B1b, B1c]

B1_2000 = [B1a2000, B1b2000, B1c2000]
B2_2000 = [B2a2000, B2b2000, B2c2000]
B3_2000 = [B3a2000, B3b2000, B3c2000]
B4_2000 = [B4a2000, B4b2000, B4c2000]

R0 = [R0a, R0b, R0c]
R1 = [R1a, R1b, R1c]
R2 = [R2a, R2b, R2c]
R3 = [R3a, R3b, R3c]
R4 = [R4a, R4b, R4c]

L_TERMS = [[L0, L1, L2, L3, L4, L5], [L1_2000, L2_2000, L3_2000, L4_2000]]
B_TERMS = [[B0, B1], [B1_2000, B2_2000, B3_2000, B3_2000, B4_2000]]
R_TERMS = [R0, R1, R2, R3, R4]


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
        for i in xrange(0, len(terms[0])):
            ta = terms[0][i]
            tb = terms[1][i]
            tc = terms[2][i]
            v += ta * math.cos(tb + (tc * self.T))
        return v

    def __calculate_B(self, useSun2000):
        B0 = self.__calculate_cos_component(B_TERMS[0][0])
        if useSun2000 and len(B_TERMS) == 2:
            B1 = self.__calculate_cos_component(B_TERMS[1][0])
            B2 = self.__calculate_cos_component(B_TERMS[1][1])
            B3 = self.__calculate_cos_component(B_TERMS[1][2])
            B4 = self.__calculate_cos_component(B_TERMS[1][3])
            self.B = ((((((((B4 * self.T) + B3) * self.T) + B2) * self.T) + B1) * self.T) + B0) / 100000000.0
        else:
            B1 = self.__calculate_cos_component(B_TERMS[0][1])
            tB = ((B1 * self.T) + B0) / 100000000.0
            tB *= 180.0 / math.pi
            self.B = mathutils.normalize_degrees(tB, -360.0, 360.0)

    def __calculate_L(self, useSun2000):
        L0 = self.__calculate_cos_component(L_TERMS[0][0])
        if useSun2000 and len(L_TERMS) == 2:
            L1 = self.__calculate_cos_component(L_TERMS[1][0])
            L2 = self.__calculate_cos_component(L_TERMS[1][1])
            L3 = self.__calculate_cos_component(L_TERMS[1][2])
            L4 = self.__calculate_cos_component(L_TERMS[1][3])
            L5 = self.__calculate_cos_component(L_TERMS[0][5])
        else:
            L1 = self.__calculate_cos_component(L_TERMS[0][1])
            L2 = self.__calculate_cos_component(L_TERMS[0][2])
            L3 = self.__calculate_cos_component(L_TERMS[0][3])
            L4 = self.__calculate_cos_component(L_TERMS[0][4])
            L5 = 0
        tL = ((((((((((L5 * self.T) + L4) * self.T) + L3) * self.T) + L2) * self.T) + L1) * self.T) + L0) / 100000000.0
        tL *= 180.0 / math.pi
        self.L = mathutils.normalize_degrees(tL)

    def __calculate_R(self):
        R0 = self.__calculate_cos_component(R_TERMS[0])
        R1 = self.__calculate_cos_component(R_TERMS[1])
        R2 = self.__calculate_cos_component(R_TERMS[2])
        R3 = self.__calculate_cos_component(R_TERMS[3])
        R4 = self.__calculate_cos_component(R_TERMS[4])
        self.R = ((((((((R4 * self.T) + R3) * self.T) + R2) * self.T) + R1) * self.T) + R0) / 100000000.0

    def calculate_with_dateTD(self, dateTD, useSun2000=True):
        """
        Calculate the position properties for Earth.
        :param dateTD: the date (TD)
        :param useSun2000: 
        """
        if dateTD is None:
            raise ValueError, "Date (TD) is required!"
        dateTD.to_td()
        self.calculate_with_julianTD(dateTD.get_julian(), useSun2000)

    def calculate_with_julianTD(self, jde, useSun2000=True):
        """
        Calculate the position properties for Earth.
        :param jde: the julian date (TD)
        :param useSun2000: 
        """
        toRad = math.pi / 180.0
        self.T = (jde - astrodate.J2000) / 365250.0
        self.__calculate_L(useSun2000)
        self.__calculate_B(useSun2000)
        self.__calculate_R()
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


if __name__ == "__main__":


    date = astrodate.AstroDate()
    date.now()
    jde = date.get_julian(True)
    nutation = Nutation()
    nutation.calculate_with_julianTD(jde)
    print("Mean Obliquity: {}".format(nutation.get_mean_obliquity()))
    print("Nutation in Longitude: {}".format(nutation.get_nutation_in_longitude()))
    print("Nutation in Obliquity: {}".format(nutation.get_nutation_in_obliquity()))
    print("True Obliquity: {}".format(nutation.get_true_obliquity()))

    print

    position = Position()
    position.calculate_with_julianTD(jde)
    print("Latitude0: {}".format(position.get_latitude0()))
    print("Latitude: {}".format(position.get_latitude()))
    print("Longitude0: {}".format(position.get_longitude0()))
    print("Longitude: {}".format(position.get_longitude()))
    print("Radius: {}".format(position.get_radius()))
