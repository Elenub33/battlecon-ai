#!/usr/bin/env python3

import logging
from optparse import OptionParser

import battlecon


# Global logging configuration
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '{filename}.{funcName}:{lineno:04d} -{levelname[0]}-> {message}',
    style='{'))
root_logger.addHandler(handler)


log = logging.getLogger(__name__)


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
