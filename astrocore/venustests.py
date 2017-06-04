import unittest
import astrodate
import venus

class Test_Venus(unittest.TestCase):
    def setUp(self):
        pass

    def test_position(self):
        p = venus.Position(venus.TERMS_VSOP87D)

        jde = astrodate.calculate_julian(1998, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, 0.8454455696475623)
        self.assertEqual(longitude, 91.06983954587166)
        self.assertEqual(radius, 0.719596069699695)

        jde = astrodate.calculate_julian(2008, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, 3.253578332266348)
        self.assertEqual(longitude, 183.34794389977853)
        self.assertEqual(radius, 0.7202648234694472)

        jde = astrodate.calculate_julian(2018, 1, 1)
        p.calculate_with_julianTD(jde)
        latitude = p.get_latitude()
        longitude = p.get_longitude()
        radius = p.get_radius()
        self.assertEqual(latitude, -1.1077565827266298)
        self.assertEqual(longitude, 275.8648465097962)
        self.assertEqual(radius, 0.7273119838277067)


if __name__ == '__main__':

    unittest.main()
