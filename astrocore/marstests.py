import unittest
import astrodate
import mars

class Test_Mars(unittest.TestCase):
    def setUp(self):
        pass

    def test_position(self):
        p = mars.Position(mars.TERMS_VSOP87D)

        jde = astrodate.calculate_julian(1998, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertAlmostEqual(latitude, -1.8068684712918077, 14)
        self.assertEqual(longitude, 331.9059416711147)
        self.assertEqual(radius, 1.3816313510653964)

        jde = astrodate.calculate_julian(2008, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertAlmostEqual(latitude, 1.3413650151739689, 14)
        self.assertEqual(longitude, 96.09842753476634)
        self.assertEqual(radius, 1.5840682142081786)

        jde = astrodate.calculate_julian(2018, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertAlmostEqual(latitude, 1.078229523934518, 14)
        self.assertEqual(longitude, 194.05289858575324)
        self.assertEqual(radius, 1.631044330391502)


if __name__ == '__main__':

    unittest.main()
