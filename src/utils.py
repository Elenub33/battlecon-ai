def IsOrdered(a, b, c):
  """Returns True iff a < b < c OR a > b > c."""
  return (a - b) * (c - b) < 0
