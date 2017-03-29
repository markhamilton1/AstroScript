import unittest
import distance

class Test_Distance(unittest.TestCase):
    def setUp(self):
        pass

    def test_ft(self):
        v = distance.ft_to_km(distance.KILOMETER_ft)
        self.assertEqual(v, 1)
        
        v = distance.ft_to_m(distance.METER_ft)
        self.assertAlmostEqual(v, 1, 15)
        
        v = distance.ft_to_mi(distance.STATUTE_MILE_ft)
        self.assertEqual(v, 1)
        
        v = distance.ft_to_nmi(distance.NAUTICAL_MILE_ft)
        self.assertEqual(v, 1)

if __name__ == '__main__':
    unittest.main()