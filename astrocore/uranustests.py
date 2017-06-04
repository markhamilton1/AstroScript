import unittest
import astrodate
import uranus

class Test_Uranus(unittest.TestCase):
    def setUp(self):
        pass

    def test_position(self):
        p = uranus.Position(uranus.TERMS_VSOP87D)

        jde = astrodate.calculate_julian(1998, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertAlmostEqual(latitude, -0.6282134140759301, 14)
        self.assertEqual(longitude, 308.40566409553765)
        self.assertEqual(radius, 19.844051001140322)

        jde = astrodate.calculate_julian(2008, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertAlmostEqual(latitude, -0.7703622749278436, 14)
        self.assertEqual(longitude, 347.91917802519964)
        self.assertEqual(radius, 20.095402766570462)

        jde = astrodate.calculate_julian(2018, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertAlmostEqual(latitude, -0.5625095080138525, 14)
        self.assertEqual(longitude, 27.321376904656642)
        self.assertEqual(radius, 19.902712546938368)


if __name__ == '__main__':

    unittest.main()
