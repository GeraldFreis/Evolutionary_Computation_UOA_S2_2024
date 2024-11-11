from ..Mutation import Insert

import unittest
import numpy as np

class InsertTest(unittest.TestCase):
    def test_Insert(self):
        test = np.arange(10).tolist()
        self.assertEqual(Insert(test), test)
        self.assertNotEqual(Insert(test), test)
        self.assertNotEqual(Insert(test), test)

if __name__ == '__main__':
    unittest.main()
