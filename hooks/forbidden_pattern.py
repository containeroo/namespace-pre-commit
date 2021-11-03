import argparse
import os
import sys
from typing import List
import re

def has_forbidden_pattern(filename: str, patterns: List[re.Pattern] = []) -> List[str]:
    """has_forbidden_pattern checks if a file has forbidden words (regex pattern) inside

    Args:
        filename (str): path to file
        patterns (List[re.Pattern], optional): list of patterns. Defaults to [].

    Returns:
        List[str]: list with forbidden patterns found
    """
    try:
        forbidden_patterns = []
        fname = os.path.expanduser(filename)
        with open(file=fname, mode="r") as stream:
            content = stream.read()
            for pattern in patterns:
              found = pattern.findall(content)
              if found:
                  forbidden_patterns.append(pattern.pattern)
        return forbidden_patterns

    except Exception as e:
        return []


def main(argv: List = None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Check if 'filenames' contains forbidden patterns
""")

    parser.add_argument('filenames',
                        nargs='+',
                        help='filenames to check')
    parser.add_argument('--forbidden-pattern', '-f',
                        action='extend',
                        dest="forbidden_pattern",
                        help="word that is forbidden (will be compiled as regex)",
                        nargs=1,
                        metavar="Word")
    args = parser.parse_args(argv)

    patterns = [re.compile(w, re.IGNORECASE) for w in args.forbidden_pattern if w]

    return_code = 0
    for fname in args.filenames:
      forbidden_patterns = has_forbidden_pattern(filename=fname, patterns=patterns)
      if forbidden_patterns:
          print("File has forbidden pattern{PLURAL} ({PATTERN}): {FILE}".format(PLURAL="s" if len(forbidden_patterns) > 1 else "",
                                                                                PATTERN=", ".join(forbidden_patterns),
                                                                                FILE=fname))
          return_code = 1
          continue

    return return_code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
