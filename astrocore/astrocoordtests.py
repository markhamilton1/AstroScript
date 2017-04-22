import unittest
import astrodate
from astrocoord import *


class Test_Coord(unittest.TestCase):

    def setUp(self):
        pass

    def test_angular_separation(self):
        coord1 = AstroCoord()
        coord1.set_from_tuple((5, 13, 31.7, -8, 13, 30, u'equ|hrs|ra'))
        coord2 = AstroCoord()
        coord2.set_from_tuple((6, 44, 13.4, -16, 41, 11, u'equ|hrs|ra'))
        d = coord1.calculate_angular_separation(coord2)
        # print(d)
        self.assertTupleEqual(d, (23, 40, 25.857919791091888))

        coord1.set_from_tuple((14, 15, 19.7, 19, 10, 57, u'equ|hrs|ra'))
        coord2.set_from_tuple((13, 25, 11.6, -11, 9, 41, u'equ|hrs|ra'))
        d = coord1.calculate_angular_separation(coord2)
        # print(d)
        self.assertTupleEqual(d, (32, 45, 43.041190343990365))

        coord1.set_from_tuple((14, 29, 42.95, -62, 40, 46.1, u'equ|hrs|ra'))
        coord2.set_from_tuple((14, 39, 36.5, -60, 50, 2.3, u'equ|hrs|ra'))
        d = coord1.calculate_angular_separation(coord2)
        # print(d)
        self.assertTupleEqual(d, (2, 11, 5.824363564898825))

        coord1.set_from_tuple((0, 47, 33.13, -25, 17, 17.8, u'equ|hrs|ra'))
        coord2.set_from_tuple((15, 34, 57.21, 23, 30, 9.5, u'equ|hrs|ra'))
        d = coord1.calculate_angular_separation(coord2)
        # print(d)
        self.assertTupleEqual(d, (141, 59, 52.08874228095283))

    def test_ecliptic_to_equatorial(self):
        d = astrodate.AstroDate().alloc_with_julian(astrodate.J1950, "td")
        c = AstroCoord()
        c.set_date(d)

        c.set_from_tuple((139, 41, 10, 4, 52, 31, u'ecl'))
        # print(c.get_pretty_coordinate())

        c.to_equatorial(1980.0)
        # print(c.get_pretty_coordinate())
        t = c.get_tuple()
        self.assertTupleEqual(t, (9, 34, 53.5848177944834, 19, 32, 14.183372805185286, u'equ|hrs|ra'))

    def test_equatorial_mode(self):
        d = astrodate.AstroDate()
        d.set_longitude(-64.0)
        d.set_from_tuple((1980, 4, 22, 14, 36, 51.67, u'ut'))
        d.to_lst()
        c = AstroCoord()
        c.set_date(d)

        c.set_from_tuple((18, 32, 21.0, -8, 12, 5.9, u'equ|hrs|ra'))
        # print(Rigel_Equ_Hrs_RA)

        c.to_hour_angle()
        # print(c.get_pretty_coordinate())
        t = c.get_tuple()
        self.assertTupleEqual(t, (5, 51, 44.22894010882828, -8, 12, 5.9, u'equ|hrs|ha'))

        c.to_degrees()
        # print(c.get_pretty_coordinate())
        t = c.get_tuple()
        self.assertTupleEqual(t, (87, 56, 3.4341016324242446, -8, 12, 5.9, u'equ|deg|ha'))

    def test_equatorial_to_ecliptic(self):
        d = astrodate.AstroDate().alloc_with_julian(astrodate.J1950, "td")
        c = AstroCoord()
        c.set_date(d)

        c.set_from_tuple((9, 34, 53.6, 19, 32, 14.2, u'equ|hrs|ra'))
        # print(c.get_pretty_coordinate())

        c.to_ecliptic()
        # print(c.get_pretty_coordinate())
        t = c.get_tuple()
        self.assertTupleEqual(t, (139, 41, 9.285573496426878, 4, 52, 22.000482436316844, u'ecl'))

    def test_equatorial_to_galactic(self):
        d = astrodate.AstroDate().alloc_with_julian(astrodate.J1950, "td")
        c = AstroCoord()
        c.set_date(d)

        c.set_from_tuple((10, 21, 0.0, 10, 3, 11, u'equ|hrs|ra'))
        # print(c.get_pretty_coordinate())

        c.to_galactic()
        # print(c.get_pretty_coordinate())
        t = c.get_tuple()
        self.assertTupleEqual(t, (232, 14, 52.50697306916891, 51, 7, 20.161085448536937, u'gal'))

    def test_equatorial_to_horizon(self):
        c = AstroCoord()
        c.set_latitude(52.0)

        c.set_from_tuple((5, 51, 44.0, 23, 13, 10.0, u'equ|hrs|ha'))
        # print(c.get_pretty_coordinate())

        c.to_horizon()
        # print(c.get_pretty_coordinate())
        t = c.get_tuple()
        self.assertTupleEqual(t, (19, 20, 3.6428077696939454, 283, 16, 15.69816218970118, u'hor'))

        # print

        d = astrodate.AstroDate()
        d.set_from_tuple((2017, 1, 1, 0, 0, 0.0, u'lst'))
        c.set_latitude(31.9583)
        c.set_date(d)

        c.set_from_tuple((10, 41, 4.488, 41, 16, 9.012, u'equ|deg|ra'))
        # print(c.get_pretty_coordinate())

        c.to_horizon()
        # print(c.get_pretty_coordinate())
        t = c.get_tuple()
        self.assertTupleEqual(t, (77, 21, 40.57145365949509, 39, 33, 35.19544189904707, u'hor'))

        # print

        d.set_longitude(-1.9166667)
        d.set_from_tuple((1998, 8, 10, 23, 10, 00, u'ut'))
        d.to_lst()
        c.set_latitude(52.5)
        c.set_date(d)

        c.set_from_tuple((16, 41, 42, 36, 28, 0.0, u'equ|hrs|ra'))
        # print(c.get_pretty_coordinate())

        c.to_horizon()
        # print(c.get_pretty_coordinate())
        t = c.get_tuple()
        self.assertTupleEqual(t, (49, 10, 7.926858207696341, 269, 8, 48.00834322929404, u'hor'))

    def test_galactic_to_equatorial(self):
        d = astrodate.AstroDate().alloc_with_julian(astrodate.J1950, "td")
        c = AstroCoord()
        c.set_date(d)

        c.set_from_tuple((232, 14, 52.51, 51, 7, 20.16, u'gal'))
        # print(c.get_pretty_coordinate())

        c.to_equatorial()
        # print(c.get_pretty_coordinate())
        t = c.get_tuple()
        self.assertTupleEqual(t, (10, 21, 0.0005059578982979929, 10, 3, 10.980488527537773, 'equ|hrs|ra'))

    def test_horizon_to_equatorial(self):
        c = AstroCoord()
        c.set_latitude(52.0)

        c.set_from_tuple((19, 20, 3.64, 283, 16, 15.7, u'hor'))
        # print(c.get_pretty_coordinate())

        c.to_equatorial()
        # print(c.get_pretty_coordinate())
        t = c.get_tuple()
        self.assertTupleEqual(t, (5, 51, 44.000228188612596, 23, 13, 9.999001910813092, 'equ|hrs|ha'))

        # print

        d = astrodate.AstroDate()
        d.set_from_tuple((2017, 1, 1, 0, 0, 0.0, u'lst'))
        c.set_latitude(31.9583)
        c.set_date(d)

        c.set_from_tuple((77, 21, 40.56, 39, 33, 35.22, u'hor'))
        # print(c.get_pretty_coordinate())

        c.to_equatorial()
        # print(c.get_pretty_coordinate())
        t = c.get_tuple()
        self.assertTupleEqual(t, (23, 17, 15.699738358052002, 41, 16, 9.016098350340371, 'equ|hrs|ha'))
        c.to_right_ascension()
        # print(c.get_pretty_coordinate())
        c.to_degrees()
        # print(c.get_pretty_coordinate())
        t = c.get_tuple()
        self.assertTupleEqual(t, (10, 41, 4.503924629219966, 41, 16, 9.016098350340371, 'equ|deg|ra'))

        # print

        d.set_longitude(-1.9166667)
        d.set_from_tuple((1998, 8, 10, 23, 10, 00, u'ut'))
        d.to_lst()
        c.set_latitude(52.5)
        c.set_date(d)

        c.set_from_tuple((49, 10, 7.93, 269, 8, 48.01, u'hor'))
        # print(c.get_pretty_coordinate())

        c.to_equatorial()
        # print(c.get_pretty_coordinate())
        t = c.get_tuple()
        self.assertTupleEqual(t, (3, 37, 31.929943132366958, 36, 28, 0.0028731920207292205, 'equ|hrs|ha'))
        c.to_right_ascension()
        # print(c.get_pretty_coordinate())
        t = c.get_tuple()
        self.assertTupleEqual(t, (16, 41, 42.000138443241894, 36, 28, 0.0028731920207292205, 'equ|hrs|ra'))


if __name__ == '__main__':


    unittest.main()
    
