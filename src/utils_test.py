import unittest

import utils


class TestIterChunks(unittest.TestCase):

  DATA = "ABCDEFGHIJKLMNOP"

  def test_EvenlySizedChunks(self):
    self.assertTrue(all(len(chunk) == 4 for chunk in utils.IterChunks(self.DATA, 4)))


if __name__ == '__main__':
  unittest.main()
