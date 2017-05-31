import unittest
import astrodate
import sun

class Test_Sun(unittest.TestCase):
    def setUp(self):
        pass

    def test_crn(self):
        d = astrodate.AstroDate().alloc_with_tuple((1975, 1, 27, 0, 0, 0.0, u'lct'))
        crn = sun.calculate_crn_with_dateTD(d)
        self.assertEqual(crn, 1624)


if __name__ == '__main__':
    
    
    unittest.main()
