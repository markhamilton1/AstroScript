import unittest
import astrocoord
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
        # print(astrocoord.dms_from_dd(mean_obliquity))
        self.assertEqual(true_obliquity, 23.443569238112364)
        # print(astrocoord.dms_from_dd(true_obliquity))


if __name__ == '__main__':
    unittest.main()
