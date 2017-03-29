import astrodate

# deltat historical data - ftp://maia.usno.navy.mil/ser7/deltat.data
# deltat predictions - ftp://maia.usno.navy.mil/ser7/deltat.preds

DATE_DELTA_T_VALUES = \
[
124.0,      119.0,      115.0,      110.0,      106.0,      102.0,       98.0,       95.0,       91.0,       88.0,      # 1620
85.0,       82.0,       79.0,       77.0,       74.0,       72.0,       70.0,       67.0,       65.0,       63.0,       # 1630
62.0,       60.0,       58.0,       57.0,       55.0,       54.0,       53.0,       51.0,       50.0,       49.0,       # 1640
48.0,       47.0,       46.0,       45.0,       44.0,       43.0,       42.0,       41.0,       40.0,       38.0,       # 1650
37.0,       36.0,       35.0,       34.0,       33.0,       32.0,       31.0,       30.0,       28.0,       27.0,       # 1660
26.0,       25.0,       24.0,       23.0,       22.0,       21.0,       20.0,       19.0,       18.0,       17.0,       # 1670
16.0,       15.0,       14.0,       14.0,       13.0,       12.0,       12.0,       11.0,       11.0,       10.0,       # 1680
10.0,        9.0,        9.0,        9.0,        9.0,        9.0,        9.0,        9.0,        9.0,        9.0,       # 1690
10.0,        9.0,        9.0,        9.0,        9.0,        9.0,        9.0,        9.0,       10.0,       10.0,       # 1700
10.0,       10.0,       10.0,       10.0,       10.0,       10.0,       10.0,       11.0,       11.0,       11.0,       # 1710
11.0,       11.0,       11.0,       11.0,       11.0,       11.0,       11.0,       11.0,       11.0,       11.0,       # 1720
11.0,       11.0,       11.0,       11.0,       12.0,       12.0,       12.0,       12.0,       12.0,       12.0,       # 1730
12.0,       12.0,       12.0,       12.0,       13.0,       13.0,       13.0,       13.0,       13.0,       13.0,       # 1740
13.0,       14.0,       14.0,       14.0,       14.0,       14.0,       14.0,       14.0,       15.0,       15.0,       # 1750
15.0,       15.0,       15.0,       15.0,       15.0,       16.0,       16.0,       16.0,       16.0,       16.0,       # 1760
16.0,       16.0,       16.0,       16.0,       16.0,       17.0,       17.0,       17.0,       17.0,       17.0,       # 1770
17.0,       17.0,       17.0,       17.0,       17.0,       17.0,       17.0,       17.0,       17.0,       17.0,       # 1780
17.0,       17.0,       16.0,       16.0,       16.0,       16.0,       15.0,       15.0,       14.0,       14.0,       # 1790
13.7,       13.4,       13.1,       12.9,       12.7,       12.6,       12.5,       12.5,       12.5,       12.5,       # 1800
12.5,       12.5,       12.5,       12.5,       12.5,       12.5,       12.5,       12.4,       12.3,       12.2,       # 1810
12.0,       11.7,       11.4,       11.1,       10.6,       10.2,        9.6,        9.1,        8.6,        8.0,       # 1820
7.5,        7.0,        6.6,        6.3,        6.0,        5.8,        5.7,        5.6,        5.6,        5.6,        # 1830
5.7,        5.8,        5.9,        6.1,        6.2,        6.3,        6.5,        6.6,        6.8,        6.9,        # 1840
7.1,        7.2,        7.3,        7.4,        7.5,        7.6,        7.7,        7.7,        7.8,        7.8,        # 1850
7.88,       7.82,       7.54,       6.97,       6.40,       6.02,       5.41,       4.10,       2.92,       1.81,       # 1860
1.61,       0.10,      -1.02,      -1.28,      -2.69,      -3.24,      -3.64,      -4.54,      -4.71,      -5.11,       # 1870
-5.40,      -5.42,      -5.20,      -5.46,      -5.46,      -5.79,      -5.63,      -5.64,      -5.80,     -5.66,       # 1880
-5.87,      -6.01,      -6.19,      -6.64,      -6.44,      -6.47,      -6.09,      -5.76,      -4.66,     -3.74,       # 1890
-2.72,      -1.54,      -0.02,       1.24,       2.64,       3.86,       5.37,       6.14,       7.75,      9.13,       # 1900
10.46,      11.53,      13.36,      14.65,      16.01,      17.20,      18.24,      19.06,      20.25,     20.95,       # 1910
21.16,      22.25,      22.41,      23.03,      23.49,      23.62,      23.86,      24.49,      24.34,     24.08,       # 1920
24.02,      24.00,      23.87,      23.95,      23.86,      23.93,      23.73,      23.92,      23.96,     24.02,       # 1930
24.33,      24.83,      25.30,      25.70,      26.24,      26.77,      27.28,      27.78,      28.25,     28.71,       # 1940
29.15,      29.57,      29.97,      30.36,      30.72,      31.07,      31.35,      31.68,      32.18,     32.68,       # 1950
33.15,      33.59,      34.00,      34.47,      35.03,      35.73,      36.54,      37.43,      38.29,     39.20,       # 1960
40.18,      41.17,      42.23,      43.37,      44.4841,    45.4761,    46.4567,    47.5214,    48.5344,   49.5862,     # 1970
50.5387,    51.3808,    52.1668,    52.9565,    53.7882,    54.3427,    54.8713,    55.3222,    55.8197,   56.30,       # 1980
56.8553,    57.5653,    58.3092,    59.1218,    59.9845,    60.7853,    61.6287,    62.2950,    62.9659,   63.4473,     # 1990
63.8285,    64.0908,    64.2998,    64.4734,    64.5736,    64.6876,    64.8452,    65.1464,    65.4573,   65.7768,     # 2000
66.0699,    66.3246,    66.6030,    66.9069,    67.281,     67.6439,    68.1024,    68.5928,    69.1,      69.6,        # 2010
70.2,       71.0,       71.0,       72.0,       72.0,       73.0,       73.0                                            # 2020
]

DATE_TD_YEAR_MIN = 1620
DATE_TD_YEAR_MAX = 2026

# The fourth edition of Montenbruck & Pfleger's Astronomy on the Personal Computer (2000)
# provides the following 3rd-order polynomials valid for the period between 1825 and 2000
# with a typical 1-second accuracy
DELTA_T_MONTENBRUCK_PFLEGER_POLYNOMIALS = (
    (1825, 1850, (10.4, -80.8, 413.9, -572.3), lambda year: (year - 1825.0) / 100.0),
    (1850, 1875, (6.6, 46.3, -358.4, 18.8), lambda year: (year - 1850.0) / 100.0),
    (1875, 1900, (-3.9, -10.8, -166.2, 867.4), lambda year: (year - 1875.0) / 100.0),
    (1900, 1925, (-2.6, 114.1, 327.5, -1467.4), lambda year: (year - 1900.0) / 100.0),
    (1925, 1950, (24.2, -6.3, -8.2, 483.4), lambda year: (year - 1925.0) / 100.0),
    (1950, 1975, (29.3, 32.5, -3.8, 550.7), lambda year: (year - 1950.0) / 100.0),
    (1975, 2000, (45.3, 130.5, -570.5, 1516.7), lambda year: (year - 1975.0) / 100.0)
)

# Jean Meeus, in the second edition of his Astronomical Algorithms (1998), gives two lower-order
# polynomials covering the same time span with a maximum error of 0.9 seconds
DELTA_T_MEEUS_POLYNOMIALS = (
    (1800, 1900, (-2.5, 228.95, 5218.61, 56282.84, 324011.78, 1061660.75, 2087298.89, 2513807.78, 1818961.41, 727058.63, 123563.95), lambda year: (year - 1900.0) / 100.0),
    (1900, 1997, (-2.44, 87.24, 815.2, -2637.8, -18756.33, 124906.15, -303191.19, 372919.88, -232424.66, 58353.42), lambda year: (year - 1900.0) / 100.0)
)

# The initial set of polynomials derived by Meeus Simon (2000) but has a maximum error up to
# 3.2s and the beginning of the series has a high absolute error which decreases as the year
# gets later
DELTA_T_MEEUS_SIMON_POLYNOMIALS = (
    (1620, 1690, (40.3, -107.0, 50.0, -454.0, 1244.0), lambda year: 3.45 + ((year - 2000.0) / 100.0)),
    (1690, 1770, (10.2, 11.3, -1.0, -16.0, 70.0), lambda year: 2.70 + ((year - 2000.0) / 100.0)),
    (1770, 1820, (14.7, -18.8, -22.0, 173.0, 6.0), lambda year: 2.05 + ((year - 2000.0) / 100.0)),
    (1820, 1870, (5.7, 12.7, 111.0, -534.0, -1654.0), lambda year: 1.55 + ((year - 2000.0) / 100.0)),
    (1870, 1900, (-5.8, -14.6, 27.0, 101.0, 8234.0), lambda year: 1.15 + ((year - 2000.0) / 100.0)),
    (1900, 1940, (21.4, 67.0, -443.0, 19.0, 4441.0), lambda year: 0.80 + ((year - 2000.0) / 100.0)),
    (1940, 1990, (36.2, 74.0, 189.0, -140.0, -1883.0), lambda year: 0.35 + ((year - 2000.0) / 100.0)),
    (1990, 2000, (60.8, 82.0, -188.0, -5034.0, 0.0), lambda year: 0.05 + ((year - 2000.0) / 100.0))
)

# An improved set of polynomials derived from the Meeus Simon set (2008)
DELTA_T_ISLAM_SADIQ_QURESHI_POLYNOMIALS = (
    (1620, 1690, (42.453, -108.62, 46.908, -451.441, 1273.369), lambda year: 3.45 + ((year - 2000.0) / 100.0)),
    (1690, 1770, (11.364, 9.234, 2.457, -1.194, 45.161), lambda year: 2.7 + ((year - 2000.0) / 100.0)),
    (1770, 1820, (15.304, -22.998, -27.101, 281.575, 122.178), lambda year: 2.05 + ((year - 2000.0) / 100.0)),
    (1820, 1870, (6.085, 14.218, 103.619, -598.093, -1496.75), lambda year: 1.55 + ((year - 2000.0) / 100.0)),
    (1870, 1900, (-5.571, -11.542, -40.46, -186.858, 11825.13), lambda year: 1.15 + ((year - 2000.0) / 100.0)),
    (1900, 1940, (21.462, 67.422, -448.338, -11.948, 4655.586), lambda year: 0.8 + ((year - 2000.0) / 100.0)),
    (1940, 1990, (36.126, 73.93, 212.64, -137.364, -2383.49), lambda year: 0.35 + ((year - 2000.0) / 100.0)),
    (1990, 2000, (60.798, 81.694, -174.854, -4823.23, -2039.63), lambda year: 0.05 + ((year - 2000.0) / 100.0))
)

# Calculate delta-t using a polynomial set.
# polys=the polynomial set to use
# dat=the date to calculate for
# returns delta-t in seconds (None=not available)
def calc_dt_poly(polys, dat):
    if polys and dat:
        for poly in polys:
            if poly[0] <= dat[0] < poly[1]:
                u = poly[3](dat[0])
                dt = 0.0
                for i, coef in reversed(list(enumerate(poly[2]))):
                    dt = coef + dt
                    if i != 0:
                        dt *= u
                return dt
    return None

# Calculate delta-t from a table of historic values.
# dat=the date to calculate for
# returns delta-t in seconds (None=not available)
def calc_dt_interp(dat):
    if dat:
        if (dat[0] < DATE_TD_YEAR_MIN - 70) or (dat[0] > DATE_TD_YEAR_MAX + 70):
            julian = astrodate.to_julian_from_date_tuple(dat)
            dy = julian - 2382148.0
            dt = ((dy * dy) / 41048480.0) - 15.0
        elif dat[0] < DATE_TD_YEAR_MIN:
            m = (DATE_DELTA_T_VALUES[1] - DATE_DELTA_T_VALUES[0]) / 2.0
            dt = ((dat[0] - DATE_TD_YEAR_MIN) * m) + DATE_DELTA_T_VALUES[0]
        elif dat[0] > DATE_TD_YEAR_MAX:
            last = (DATE_TD_YEAR_MAX - DATE_TD_YEAR_MIN) / 2
            m = (DATE_DELTA_T_VALUES[last] - DATE_DELTA_T_VALUES[last - 1]) / 2.0
            dt = ((dat[0] - DATE_TD_YEAR_MAX) * m) + DATE_DELTA_T_VALUES[last]
        else:
            i = dat[0] - DATE_TD_YEAR_MIN
            dt = DATE_DELTA_T_VALUES[i]
        return dt
    return None



# Compare the polynomial generated delta-t values to those interpolated from historical data.
# This method produces a table of values and their absolute error followed by a summary of the
# errors for the polynomial sets.
def show_delta_t_with_errors():
    polynomial_sets = (
        ("Meeus Polynomials", DELTA_T_MEEUS_POLYNOMIALS),
        ("Montenbruck Pfleger Polynomials", DELTA_T_MONTENBRUCK_PFLEGER_POLYNOMIALS),
        ("Meeus Simon Polynomials", DELTA_T_MEEUS_SIMON_POLYNOMIALS),
        ("Islam Sadiq, Qureshi Polynomials", DELTA_T_ISLAM_SADIQ_QURESHI_POLYNOMIALS)
    )
    error_sets = []
    for set in polynomial_sets:
        e_set = [0.0, 0.0, 0]        # max ae, sum ae^2, n
        error_sets.append(e_set)
    for y in xrange(DATE_TD_YEAR_MIN, DATE_TD_YEAR_MAX):
        dat = (y, 1, 1)
        dt_i = calc_dt_interp(dat)
        s = "%4i  %6.2f  " % (y, dt_i)
        print s,
        for i, poly_set in enumerate(polynomial_sets):
            dt_p = calc_dt_poly(poly_set[1], dat)
            if dt_p:
                ae = abs(dt_i - dt_p)
                if ae > error_sets[i][0]:
                    error_sets[i][0] = ae
                error_sets[i][1] += ae
                error_sets[i][2] += 1
                s = "%6.2f (%3.2f)  " % (dt_p, ae)
                print s,
            else:
                print "           na  ",
        print
    print
    for i, e_set in enumerate(error_sets):
        name = polynomial_sets[i][0]
        max_ae = e_set[0]
        avg_ae = e_set[1] / e_set[2]
        print "%s Error Summary" % name
        print "  Max Absolute Error: %3.3f" % max_ae
        print "  Avg Absolute Error: %3.3f" % avg_ae

# Calculate the error for a single polynomial from a set.
def calc_error_summary(poly):
    if poly:
        max_ae = 0.0
        sum_ae = 0.0
        n = 0
        for y in xrange(poly[0], poly[1]):
            dat = (y, 1, 1)
            dt_i = calc_dt_interp(dat)
            u = poly[3](dat[0])
            dt = 0.0
            for i, coef in reversed(list(enumerate(poly[2]))):
                dt = coef + dt
                if i != 0:
                    dt *= u
            ae = abs(dt_i - dt)
            if ae > max_ae:
                max_ae = ae
            sum_ae += ae
            n += 1
        return (max_ae, (sum_ae / n))
    return None


if __name__ == "__main__":

    show_delta_t_with_errors()
