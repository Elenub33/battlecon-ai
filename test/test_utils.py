import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import utils

class TestIterChunks(unittest.TestCase):

    DATA = "ABCDEFGHIJKLMNOP"

    def test_EvenlySizedChunks(self):
        self.assertTrue(all(len(chunk) == 4 for chunk in utils.IterChunks(self.DATA, 4)))

    def test_EvenlySizedChunksWithUnevenDivisor(self):
        self.assertTrue(all(len(chunk) == 3 for chunk in utils.IterChunks(self.DATA, 3)))

    def test_NoMissingItems(self):
        reconstructed = ""
        for chunk in utils.IterChunks(self.DATA, 4):
            reconstructed += "".join(chunk)
        self.assertEqual(self.DATA, reconstructed)

    def test_FillWithSpecifiedItem(self):
        reconstructed = ""
        for chunk in utils.IterChunks(self.DATA, 5, fill="X"):
            reconstructed += "".join(chunk)
        self.assertEqual(self.DATA + "XXXX", reconstructed)


if __name__ == "__main__":
    unittest.main()
