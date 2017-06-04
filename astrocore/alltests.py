import unittest
from astrocoordtests import Test_Coord
from astrodatetests import Test_Date
from datetimestringtests import Test_DateTimeString
from distancetests import Test_Distance
from earthtests import Test_Earth
from jupitertests import Test_Jupiter
from marstests import Test_Mars
from mercurytests import Test_Mercury
from neptunetests import Test_Neptune
from saturntests import Test_Saturn
from suntests import Test_Sun
from uranustests import Test_Uranus
from venustests import Test_Venus

test_cases = [Test_Coord, Test_Date, Test_DateTimeString, Test_Distance,
              Test_Earth, Test_Jupiter, Test_Mars, Test_Mercury, Test_Neptune,
              Test_Saturn, Test_Sun, Test_Uranus, Test_Venus]

testLoader = unittest.TestLoader()
tests = []
for test_case in test_cases:
    test_suite = testLoader.loadTestsFromTestCase(test_case)
    tests.append(test_suite)
 
new_suite = unittest.TestSuite(tests)

if __name__ == "__main__":

    unittest.main(verbosity=2)

