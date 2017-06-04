import unittest
import astrodate
import neptune

class Test_Neptune(unittest.TestCase):
    def setUp(self):
        pass

    def test_position(self):
        p = neptune.Position(neptune.TERMS_VSOP87D)

        jde = astrodate.calculate_julian(1998, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, 0.3745111145247912)
        self.assertEqual(longitude, 299.546754568677)
        self.assertEqual(radius, 30.145211309963376)

        jde = astrodate.calculate_julian(2008, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, -0.2952703665730311)
        self.assertEqual(longitude, 321.4728593378659)
        self.assertEqual(radius, 30.04242600523542)

        jde = astrodate.calculate_julian(2018, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, -0.9264709585814667)
        self.assertEqual(longitude, 343.56386354496607)
        self.assertEqual(radius, 29.944701179744804)


if __name__ == '__main__':

    unittest.main()
