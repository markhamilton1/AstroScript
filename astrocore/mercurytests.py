import unittest
import astrodate
import mercury

class Test_Mercury(unittest.TestCase):
    def setUp(self):
        pass

    def test_position(self):
        p = mercury.Position(mercury.TERMS_VSOP87D)

        jde = astrodate.calculate_julian(1998, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, 6.194758510915122)
        self.assertEqual(longitude, 166.25446998252286)
        self.assertEqual(radius, 0.3689447062980261)

        jde = astrodate.calculate_julian(2008, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, -6.890601940330963)
        self.assertEqual(longitude, 308.0020711769773)
        self.assertEqual(radius, 0.4265244131415521)

        jde = astrodate.calculate_julian(2018, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, 5.147097409406132)
        self.assertEqual(longitude, 181.4019565130787)
        self.assertEqual(radius, 0.3893565329208419)


if __name__ == '__main__':

    unittest.main()
