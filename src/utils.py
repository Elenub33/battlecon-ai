import itertools
import math
import logging
from typing import List


log = logging.getLogger(__name__)


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

  return set(range(low, high + 1))


def TypesafeRange(*args):
  """Range, but with all arguments coerced to integers."""
  typesafe_args = tuple(map(int, args))
  if typesafe_args != args:
    log.warning(f"Nontrivial coercion of {args} to Tuple[int]")
  return range(*typesafe_args)


def IterChunks(iterable, chunk_size, fill=None):
  """Iterate over non-overlapping groups of CHUNK_SIZE elements from ITERABLE.

  If the length of ITERABLE is not evenly divisible by CHUNK_SIZE, fill the
  remaining slots in the last chunk with FILL.
  """
  for _, group in itertools.groupby(
    enumerate(iterable), lambda pair: pair[0] // chunk_size
  ):
    items = list(pair[1] for pair in group)
    while len(items) < chunk_size:
      items.append(fill)
    yield tuple(items)


# raised at fork points to throw simulation back up to main simulate() method
class ForkException(Exception):
  def __init__(self, n_options, player):
    self.n_options = int(n_options)
    self.forking_player = player


# Raised whenever a player wins, for easy program flow control
class WinException(Exception):
  def __init__(self, winner):
    self.winner = winner


# Cumulative Gaussian function
def phi(x):
  return 0.5 + 0.5 * math.erf(x / (2 ** 0.5))


def MenuPrompt(options, num_columns=1):
  """Display OPTIONS as a columned menu and solicit a numeric selection.

  Returns:
    The selected index (int)."""
  numbered_options = [f"[{idx}] {item}" for idx, item in enumerate(options)]
  column_length = int(math.ceil(len(options) / num_columns))
  columns = list(IterChunks(enumerate(numbered_options), column_length, fill=(-1, "")))
  column_width = max(map(len, numbered_options))

  for items in itertools.zip_longest(*columns):
    row = "  ".join(map(lambda item: item[1].ljust(column_width), items))
    print("  " + row)

  idx = ReadNumber(0, len(options))
  return idx


def ReadNumber(a, b):
  """Prompt user for a number N such that A <= N < B.

  Returns:
    An integer in the range [`a`, `b`)."""
  while True:
    response = input(f"[{a}-{b-1}] >> ").strip()
    try:
      result = int(response)
      if result < a or result >= b:
        print(f"Please enter an integer between {a} and {b-1} inclusive.")
      else:
        break
    except ValueError:
      print(f"Please enter an integer between {a} and {b-1} inclusive.")
  return result
