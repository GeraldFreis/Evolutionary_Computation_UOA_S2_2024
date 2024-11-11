from ..Mutation import Scramble
import unittest
import numpy as np

class ScrambleTest(unittest.TestCase):
    def test_Scramble(self):
        test = np.arange(10).tolist()
        self.assertEqual(Scramble(test), test)
        self.assertNotEqual(Scramble(test), test)
        self.assertNotEqual(Scramble(test), test)
if __name__ == '__main__':
    unittest.main()
