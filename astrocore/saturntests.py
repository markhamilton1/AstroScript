import unittest
import astrodate
import saturn

class Test_Saturn(unittest.TestCase):
    def setUp(self):
        pass

    def test_position(self):
        p = saturn.Position(saturn.TERMS_VSOP87D)

        jde = astrodate.calculate_julian(1998, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, -2.4798143896218066)
        self.assertEqual(longitude, 19.779644001582255)
        self.assertEqual(radius, 9.366709083172355)

        jde = astrodate.calculate_julian(2008, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, 1.5827657392464183)
        self.assertEqual(longitude, 153.22998324863892)
        self.assertEqual(radius, 9.266136560404153)

        jde = astrodate.calculate_julian(2018, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, 0.9829772740784639)
        self.assertEqual(longitude, 270.51396993626645)
        self.assertEqual(radius, 10.064742444221443)


if __name__ == '__main__':

    unittest.main()
