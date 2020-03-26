from typing import List


def IsOrdered(a, b, c) -> bool:
  """Returns True iff A < B < C OR A > B > C."""
  return (a - b) * (c - b) < 0


def PositionsBetween(a, b) -> List[int]:
  """Returns the board positions between spaces A and B inclusive."""
  # TODO: Python 2->3 migration revealed an issue where some positions or
  # ranges are floats instead of ints. This is a problem Python3's range() does
  # not accept float arguments even if they are whole numbers. Setting the if
  # condition to False instead of True exposes that behavior.
  if True:
    low, high = int(min(a, b)), int(max(a, b))
  else:
    low, high = min(a, b), max(a, b)

  return set(range(low, high+1))
