import itertools
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

  return set(range(low, high+1))


def TypesafeRange(*args):
  """Range, but with all arguments coerced to integers."""
  typesafe_args = tuple(map(int, args))
  if typesafe_args != args:
    log.warning(f'Nontrivial coercion of {args} to Tuple[int]')
  return range(*typesafe_args)


def IterChunks(iterable, chunk_size, fill=None):
  """Iterate over non-overlapping groups of CHUNK_SIZE elements from ITERABLE.

  If the length of ITERABLE is not evenly divisible by CHUNK_SIZE, fill the
  remaining slots in the last chunk with FILL.
  """
  for _, group in itertools.groupby(enumerate(iterable), lambda pair: pair[0] // chunk_size):
    items = list(pair[1] for pair in group)
    while len(items) < chunk_size:
      items.append(fill)
    yield tuple(items)
