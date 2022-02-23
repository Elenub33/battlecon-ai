import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import logging
import utils


# Global logging configuration
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
  logging.Formatter(
    "{filename}.{funcName}:{lineno:04d} -{levelname[0]}-> {message}", style="{"
  )
)
root_logger.addHandler(handler)

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
