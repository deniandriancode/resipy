import sys
sys.path.append("../")
import unittest
import resipy

class ResipyUnitTest(unittest.TestCase):
        def testNormalMessage(self):
                self.assertFalse(resipy.normal_message("input", "output"))

        def testVerboseMessage(self):
                self.assertFalse(resipy.verbose_message("input", "output"))

if __name__ == "__main__":
        unittest.main()
