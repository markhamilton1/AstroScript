import unittest
from astrocoordtests import Test_Coord
from astrodatetests import Test_Date
from datetimestringtests import Test_DateTimeString
from distancetests import Test_Distance
from earthtests import Test_Earth
from suntests import Test_Sun

test_cases = [Test_Coord, Test_Date, Test_DateTimeString, Test_Distance, Test_Earth, Test_Sun]

testLoader = unittest.TestLoader()
tests = []
for test_case in test_cases:
    test_suite = testLoader.loadTestsFromTestCase(test_case)
    tests.append(test_suite)
 
new_suite = unittest.TestSuite(tests)

if __name__ == "__main__":

    unittest.main()

