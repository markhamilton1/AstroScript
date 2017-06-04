import unittest
import astrodate
import jupiter

class Test_Jupiter(unittest.TestCase):
    def setUp(self):
        pass

    def test_position(self):
        p = jupiter.Position(jupiter.TERMS_VSOP87D)

        jde = astrodate.calculate_julian(1998, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, -0.9894618542824553)
        self.assertEqual(longitude, 329.7713376559485)
        self.assertEqual(radius, 5.020988316386657)

        jde = astrodate.calculate_julian(2008, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, 0.20051130112254614)
        self.assertEqual(longitude, 271.7299034774712)
        self.assertEqual(radius, 5.247685790242188)

        jde = astrodate.calculate_julian(2018, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, 1.151630375278742)
        self.assertEqual(longitude, 218.56792143641388)
        self.assertEqual(radius, 5.432242090031535)


if __name__ == '__main__':

    unittest.main()
