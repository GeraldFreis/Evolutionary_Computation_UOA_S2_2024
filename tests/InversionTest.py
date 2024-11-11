from ..Mutation import Inversion

import unittest
import numpy as np

class InversionTest(unittest.TestCase):
    def test_Inversion(self):
        test = np.arange(10).tolist()
        self.assertEqual(Inversion(test), test)
        self.assertNotEqual(Inversion(test), test)
        self.assertNotEqual(Inversion(test), test)

if __name__ == '__main__':
    unittest.main()
