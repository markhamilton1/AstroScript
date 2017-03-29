import unittest
import astrodate

class Test_Date(unittest.TestCase):
    def setUp(self):
        self.lng0 = 64
        self.zc0 = 4
        self.dst0 = True
        self.lct0 = (2012, 7, 23, 3, 37, 0.0, 'lct')
        self.ut0 = (2012, 7, 22, 22, 37, 0.0, 'ut')

        self.lng1 = -64
        self.zc1 = 5
        self.dst1 = False
        self.lct1 = (1980, 4, 22, 19, 36, 51.67, 'lct')
        self.ut1 = (1980, 4, 22, 14, 36, 51.67, 'ut')
        self.gst1 = (1980, 4, 22, 4, 40, 5.23, 'gst')
        self.lst1 = (1980, 4, 22, 0, 24, 5.23, 'lst')
        self.td1 = (1980, 4, 22, 14, 37, 42.21, 'td')

    def test_get_date_of_easter(self):
        e = astrodate.get_date_of_easter(1959)
        self.assertTupleEqual(e, (1959, 3, 29))
        e = astrodate.get_date_of_easter(2013)
        self.assertTupleEqual(e, (2013, 3, 31))
        e = astrodate.get_date_of_easter(2014)
        self.assertTupleEqual(e, (2014, 4, 20))

    def test_get_days_in_month(self):
        d = astrodate.get_days_in_month((2012, 2, 1))
        self.assertEquals(d, 29)
        d = astrodate.get_days_in_month((2014, 1, 1))
        self.assertEquals(d, 31)
        d = astrodate.get_days_in_month((2014, 2, 1))
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
        jd = astrodate.to_julian_from_date_tuple((-4712, 1, 1, 12, 0, 0))
        self.assertEquals(jd, 0.0)
        jd = astrodate.to_julian_from_date_tuple((1582, 10, 15))
        self.assertEquals(jd, 2299160.5)
        jd = astrodate.to_julian_from_date_tuple((1990, 12, 25, 19, 30, 0))
        self.assertEquals(jd, 2448251.3125)
        jd = astrodate.to_julian_from_date_tuple((1993, 1, 1))
        self.assertEquals(jd, 2448988.5)
        jd = astrodate.to_julian_from_date_tuple((1993, 1, 1, 12, 0, 0))
        self.assertEquals(jd, 2448989.0)
        jd = astrodate.to_julian_from_date_tuple((1993, 4, 1))
        self.assertEquals(jd, 2449078.5)
        jd = astrodate.to_julian_from_date_tuple((2000, 1, 1, 12, 0, 0))
        self.assertEquals(jd, 2451545.0)

    def test_to_date_tuple_from_julian(self):
        d = astrodate.to_date_tuple_from_julian(0.0)
        self.assertTupleEqual(d, (-4712, 1, 1, 12, 0, 0, 'ut'))
        d = astrodate.to_date_tuple_from_julian(2299160.5)
        self.assertTupleEqual(d[0:3], (1582, 10, 15))
        d = astrodate.to_date_tuple_from_julian(2448251.3125)
        self.assertTupleEqual(d, (1990, 12, 25, 19, 30, 0, 'ut'))
        d = astrodate.to_date_tuple_from_julian(2448988.5)
        self.assertTupleEqual(d[0:3], (1993, 1, 1))
        d = astrodate.to_date_tuple_from_julian(2448989.0)
        self.assertTupleEqual(d, (1993, 1, 1, 12, 0, 0, 'ut'))
        d = astrodate.to_date_tuple_from_julian(2449078.5)
        self.assertTupleEqual(d[0:3], (1993, 4, 1))
        d = astrodate.to_date_tuple_from_julian(2451545.0)
        self.assertTupleEqual(d, (2000, 1, 1, 12, 0, 0, 'ut'))

    def test_to_gst(self):
        astrodate.set_longitude(self.lng1)
        astrodate.set_zone_correction(self.zc1)
        astrodate.set_daylight_savings(self.dst1)

        gst = astrodate.to_gst(self.gst1)
        self.assertTupleEqual(gst, self.gst1)

        gst = astrodate.to_gst(self.lct1)
        self.assertTupleEqual(gst, self.gst1)

        gst = astrodate.to_gst(self.ut1)
        self.assertTupleEqual(gst, self.gst1)

        gst = astrodate.to_gst(self.lst1)
        self.assertTupleEqual(gst, self.gst1)

        gst = astrodate.to_gst(self.td1)
        self.assertTupleEqual(gst, self.gst1)

    def test_to_lct(self):
        astrodate.set_longitude(self.lng0)
        astrodate.set_zone_correction(self.zc0)
        astrodate.set_daylight_savings(self.dst0)
        lct = astrodate.to_lct(self.lct0)
        self.assertTupleEqual(lct, self.lct0)
        lct = astrodate.to_lct(self.ut0)
        self.assertTupleEqual(lct, self.lct0)

        astrodate.set_longitude(self.lng1)
        astrodate.set_zone_correction(self.zc1)
        astrodate.set_daylight_savings(self.dst1)
        lct = astrodate.to_lct(self.lct1)
        self.assertTupleEqual(lct, self.lct1)
        lct = astrodate.to_lct(self.ut1)
        self.assertTupleEqual(lct, self.lct1)
        lct = astrodate.to_lct(self.gst1)
        self.assertTupleEqual(lct, self.lct1)
        lct = astrodate.to_lct(self.lst1)
        self.assertTupleEqual(lct, self.lct1)
        lct = astrodate.to_lct(self.td1)
        self.assertTupleEqual(lct, self.lct1)

    def test_to_lst(self):
        astrodate.set_longitude(self.lng1)
        astrodate.set_zone_correction(self.zc1)
        astrodate.set_daylight_savings(self.dst1)
        lst = astrodate.to_lst(self.lst1)
        self.assertTupleEqual(lst, self.lst1)
        lst = astrodate.to_lst(self.ut1)
        self.assertTupleEqual(lst, self.lst1)
        lst = astrodate.to_lst(self.gst1)
        self.assertTupleEqual(lst, self.lst1)
        lst = astrodate.to_lst(self.lct1)
        self.assertTupleEqual(lst, self.lst1)
        lst = astrodate.to_lst(self.td1)
        self.assertTupleEqual(lst, self.lst1)

    def test_to_td(self):
        astrodate.set_longitude(self.lng1)
        astrodate.set_zone_correction(self.zc1)
        astrodate.set_daylight_savings(self.dst1)
        td = astrodate.to_td(self.td1)
        self.assertTupleEqual(td, self.td1)
        td = astrodate.to_td(self.ut1)
        self.assertTupleEqual(td, self.td1)
        td = astrodate.to_td(self.lct1)
        self.assertTupleEqual(td, self.td1)
        td = astrodate.to_td(self.gst1)
        self.assertTupleEqual(td, self.td1)
        td = astrodate.to_td(self.lst1)
        self.assertTupleEqual(td, self.td1)

    def test_to_ut(self):
        astrodate.set_longitude(self.lng0)
        astrodate.set_zone_correction(self.zc0)
        astrodate.set_daylight_savings(self.dst0)
        ut = astrodate.to_ut(self.ut0)
        self.assertTupleEqual(ut, self.ut0)
        ut = astrodate.to_ut(self.lct0)
        self.assertTupleEqual(ut, self.ut0)

        astrodate.set_longitude(self.lng1)
        astrodate.set_zone_correction(self.zc1)
        astrodate.set_daylight_savings(self.dst1)
        ut = astrodate.to_ut(self.ut1)
        self.assertTupleEqual(ut, self.ut1)
        ut = astrodate.to_ut(self.lct1)
        self.assertTupleEqual(ut, self.ut1)
        ut = astrodate.to_ut(self.gst1)
        self.assertTupleEqual(ut, self.ut1)
        ut = astrodate.to_ut(self.lst1)
        self.assertTupleEqual(ut, self.ut1)
        ut = astrodate.to_ut(self.td1)
        self.assertTupleEqual(ut, self.ut1)

if __name__ == '__main__':
    unittest.main()