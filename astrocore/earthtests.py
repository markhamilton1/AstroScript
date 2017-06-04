import unittest
import astrodate
import earth

class Test_Earth(unittest.TestCase):
    def setUp(self):
        pass

    def test_nutation(self):
        d = astrodate.AstroDate().alloc_with_tuple((1987, 4, 10, 0, 0, 0.0, u'td'))
        jde = d.get_julian()
        n = earth.Nutation()
        n.calculate_with_julianTD(jde)
        nutation_in_longitude = n.get_nutation_in_longitude()
        nutation_in_obliquity = n.get_nutation_in_obliquity()
        mean_obliquity = n.get_mean_obliquity()
        true_obliquity = n.get_true_obliquity()
        self.assertEqual(nutation_in_longitude, -0.001052332550403307)
        self.assertEqual(nutation_in_obliquity, 0.002622947155040129)
        self.assertEqual(mean_obliquity, 23.440946290957324)
        self.assertEqual(true_obliquity, 23.443569238112364)

    def test_position(self):
        p = earth.Position(earth.TERMS_VSOP87D)

        jde = astrodate.calculate_julian(1998, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, 2.1651204901319734e-05)
        self.assertEqual(longitude, 100.363323142225)
        self.assertEqual(radius, 0.9833333560780444)

        jde = astrodate.calculate_julian(2008, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, 0.00011901318043573914)
        self.assertEqual(longitude, 99.92973010197568)
        self.assertEqual(radius, 0.983289338510011)

        jde = astrodate.calculate_julian(2018, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, 4.95339099701003e-05)
        self.assertEqual(longitude, 100.51614552278916)
        self.assertEqual(radius, 0.9833010058152097)


if __name__ == '__main__':

    unittest.main()
