import unittest
import astrodate

class Test_Date(unittest.TestCase):
    def setUp(self):
        self.lng_ref1 = -64
        self.ut_ref1 = (1980, 4, 22, 14, 36, 51.67, 'ut')
        self.gst_ref1 = (1980, 4, 22, 4, 40, 5.23, 'gst')
        self.lst_ref1 = (1980, 4, 22, 0, 24, 5.23, 'lst')

        self.lng0 = 64
        self.zc0 = 4
        self.dst0 = True
        self.lct0 = (2012, 7, 23, 3, 37, 0.0, 'lct')
        self.ut0 = (2012, 7, 22, 22, 37, 0.0, 'ut')

        self.lng1 = -75
        self.zc1 = -5
        self.dst1 = False
        self.lct1 = (1980, 4, 22, 10, 36, 51.67, 'lct')
        self.ut1 = (1980, 4, 22, 15, 36, 51.67, 'ut')
        self.gst1 = (1980, 4, 22, 5, 40, 15.09, 'gst')
        self.lst1 = (1980, 4, 22, 0, 40, 15.09, 'lst')
        self.td1 = (1980, 4, 22, 15, 37, 42.21, 'td')

        self.lng2 = -111.660833
        self.zc2 = -7
        self.dst2 = False
        self.lct2 = (2017, 4, 17, 15, 2, 30.0, 'lct')
        self.ut2 = (2017, 4, 17, 22, 2, 30.0, 'ut')
        self.gst2 = (2017, 4, 17, 11, 47, 23.23, 'gst')
        self.lst2 = (2017, 4, 17, 4, 20, 44.63, 'lst')
        self.td2 = (2017, 4, 17, 22, 3, 38.59, 'td')

    def test_get_date_of_easter(self):
        e = astrodate.get_date_of_easter(1959)
        self.assertTupleEqual(e, (1959, 3, 29))

        e = astrodate.get_date_of_easter(2013)
        self.assertTupleEqual(e, (2013, 3, 31))

        e = astrodate.get_date_of_easter(2014)
        self.assertTupleEqual(e, (2014, 4, 20))

        e = astrodate.get_date_of_easter("2017")
        self.assertTupleEqual(e, (2017, 4, 16))

    def test_get_days_in_month(self):
        d = astrodate.get_days_in_month(2, 2012)
        self.assertEquals(d, 29)

        d = astrodate.get_days_in_month(1, 2014)
        self.assertEquals(d, 31)

        d = astrodate.get_days_in_month(2, 2014)
        self.assertEquals(d, 28)

    def test_is_leap_year(self):
        i = astrodate.is_leap_year(1901)
        self.assertFalse(i)

        i = astrodate.is_leap_year(2000)
        self.assertTrue(i)

        i = astrodate.is_leap_year(2001)
        self.assertFalse(i)

        i = astrodate.is_leap_year(2014)
        self.assertFalse(i)

    def test_to_julian_from_date_tuple(self):
        dat = astrodate.AstroDate()

        dat.set_from_tuple((-4712, 1, 1, 12, 0, 0))
        jd = dat.get_julian()
        self.assertEquals(jd, 0.0)

        dat.set_from_tuple((1582, 10, 15))
        jd = dat.get_julian()
        self.assertEquals(jd, 2299160.5)

        dat.set_from_tuple((1980, 2, 17))
        jd = dat.get_julian()
        self.assertEquals(jd, 2444286.5)

        dat.set_from_tuple((1985, 2, 17))
        jd = dat.get_julian()
        self.assertEquals(jd, 2446113.5)

        dat.set_from_tuple((1990, 12, 25, 19, 30, 0))
        jd = dat.get_julian()
        self.assertEquals(jd, 2448251.3125)

        dat.set_from_tuple((1993, 1, 1))
        jd = dat.get_julian()
        self.assertEquals(jd, 2448988.5)

        dat.set_from_tuple((1993, 1, 1, 12, 0, 0))
        jd = dat.get_julian()
        self.assertEquals(jd, 2448989.0)

        dat.set_from_tuple((1993, 4, 1))
        jd = dat.get_julian()
        self.assertEquals(jd, 2449078.5)

        dat.set_from_tuple((2000, 1, 1, 12, 0, 0))
        jd = dat.get_julian()
        self.assertEquals(jd, 2451545.0)

    def test_to_date_tuple_from_julian(self):
        dat = astrodate.AstroDate()

        dat.set_from_julian(0.0)
        d = dat.get_tuple()
        self.assertTupleEqual(d, (-4712, 1, 1, 12, 0, 0, 'ut'))

        dat.set_from_julian(2299160.5)
        d = dat.get_tuple()
        self.assertTupleEqual(d, (1582, 10, 15, 0, 0, 0, 'ut'))

        dat.set_from_julian(2448251.3125)
        d = dat.get_tuple()
        self.assertTupleEqual(d, (1990, 12, 25, 19, 30, 0, 'ut'))

        dat.set_from_julian(2448988.5)
        d = dat.get_tuple()
        self.assertTupleEqual(d, (1993, 1, 1, 0, 0, 0, 'ut'))

        dat.set_from_julian(2448989.0)
        d = dat.get_tuple()
        self.assertTupleEqual(d, (1993, 1, 1, 12, 0, 0, 'ut'))

        dat.set_from_julian(2449078.5)
        d = dat.get_tuple()
        self.assertTupleEqual(d, (1993, 4, 1, 0, 0, 0, 'ut'))

        dat.set_from_julian(2451545.0)
        d = dat.get_tuple()
        self.assertTupleEqual(d, (2000, 1, 1, 12, 0, 0, 'ut'))

    def test_ref1(self):
        dat = astrodate.AstroDate()
        dat.set_longitude(self.lng_ref1)

        dat.set_from_tuple(self.ut_ref1)
        dat.to_gst()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.gst_ref1)

        dat.to_lst()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.lst_ref1)

        dat.to_gst()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.gst_ref1)

        dat.to_ut()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.ut_ref1)

    def test_0(self):
        dat = astrodate.AstroDate()
        dat.set_longitude(self.lng0)
        dat.set_zone_correction(self.zc0)
        dat.set_daylight_savings(self.dst0)

        dat.set_from_tuple(self.lct0)
        dat.to_lct()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.lct0)

        dat.to_ut()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.ut0)

        dat.to_lct()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.lct0)

    def test_1(self):
        dat = astrodate.AstroDate()
        dat.set_longitude(self.lng1)
        dat.set_zone_correction(self.zc1)
        dat.set_daylight_savings(self.dst1)

        dat.set_from_tuple(self.lct1)
        dat.to_lct()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.lct1)

        dat.to_ut()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.ut1)

        dat.to_lct()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.lct1)

        dat.set_from_tuple(self.ut1)
        dat.to_gst()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.gst1)

        dat.to_ut()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.ut1)

        dat.set_from_tuple(self.gst1)
        dat.to_lst()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.lst1)

        dat.to_gst()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.gst1)

        dat.set_from_tuple(self.ut1)
        dat.to_td()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.td1)

        dat.to_ut()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.ut1)

        dat.set_from_tuple(self.lct1)
        dat.to_lst()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.lst1)

        dat.to_lct()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.lct1)

        dat.set_from_tuple(self.lct1)
        dat.to_td()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.td1)

        dat.to_lct()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.lct1)

    def test_2(self):
        dat = astrodate.AstroDate()
        dat.set_longitude(self.lng2)
        dat.set_zone_correction(self.zc2)
        dat.set_daylight_savings(self.dst2)

        dat.set_from_tuple(self.lct2)
        dat.to_lct()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.lct2)

        dat.to_ut()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.ut2)

        dat.to_lct()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.lct2)

        dat.set_from_tuple(self.ut2)
        dat.to_gst()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.gst2)

        dat.to_ut()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.ut2)

        dat.set_from_tuple(self.gst2)
        dat.to_lst()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.lst2)

        dat.to_gst()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.gst2)

        dat.set_from_tuple(self.ut2)
        dat.to_td()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.td2)

        dat.to_ut()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.ut2)

        dat.set_from_tuple(self.lct2)
        dat.to_lst()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.lst2)

        dat.to_lct()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.lct2)

        dat.set_from_tuple(self.lct2)
        dat.to_td()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.td2)

        dat.to_lct()
        t = dat.get_tuple()
        self.assertTupleEqual(t, self.lct2)


if __name__ == '__main__':


    unittest.main()