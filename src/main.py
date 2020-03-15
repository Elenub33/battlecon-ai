#!/usr/bin/env python3

from optparse import OptionParser

import battlecon


def main():
  parser = OptionParser()
  parser.add_option(
    "-t", "--test", action="store_true", dest="test", default=False, help="run test"
  )
  parser.add_option(
    "-f",
    "--from_file",
    dest="from_file",
    default="",
    help="run single beat from given file",
  )
  options, unused_args = parser.parse_args()
  if options.test:
    battlecon.test()
  elif options.from_file:
    battlecon.play_beat(options.from_file)
  else:
    battlecon.play()


if __name__ == "__main__":
  main()
