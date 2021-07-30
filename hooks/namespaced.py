import argparse
import os
import sys
from typing import List

import yaml


class CustomHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog):
        # change max_help_position
        super(CustomHelpFormatter, self).__init__(prog, max_help_position=42)

    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return metavar
        else:
            parts = []
            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                parts.extend(action.option_strings)

            # if the Optional takes a value, format is:
            #    -s, --long ARGS
            else:
                default = action.dest.upper()
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append('%s' % option_string)
                parts[-1] += ' %s' % args_string
            return ', '.join(parts)


class CustomFormatter(CustomHelpFormatter,
                      argparse.RawDescriptionHelpFormatter):
    pass


def is_kubernetes_manifest(filename: str) -> List[dict]:
    """is_kubernetes_manifest test if a file is a Kubernetes manifest by loading
    the 'filename' is a vaild yaml and has a the key 'apiVersion'. A file can
    contain multiple yaml-files.

    Args:
        filename (str): path to the file to check

    Returns:
        List[dict]: List of loaded yaml files
    """
    try:
      fname = os.path.expanduser(filename)

      with open(file=fname, mode="r") as stream:
          manifests = list(yaml.load_all(stream=stream,
                                         Loader=yaml.SafeLoader))
    except Exception as e:
        return []
    for manifest in manifests:
      if not manifest.get("apiVersion"):
          return []
      return manifests


def is_namespaced_kubernetes_manifest(manifest: dict) -> bool:
    """is_namespaced_kubernetes_manifest check if a dict has the key 'metadata.namespace'

    Args:
        manifest (dict): Kubernetes manifest (loaded as dict) to search for the key 'metadata.namespace'

    Returns:
        bool: True if 'metadata.namespace' was found, False if not
    """
    if not manifest.get("metadata"):
        return False
    if not manifest["metadata"].get("namespace"):
        return False
    return True

def is_ignored_kubernetes_kind(manifest: dict, ignored_kinds: List[str] = []) -> bool:
    """is_ignored_kubernetes_kind check if a dict has a key which is in a list of kinds
    who shouldn't be checked

    Args:
        manifest (dict): Kubernetes manifest (loaded as dict) to check if the key 'kind' is in the 'ignored_kinds' list
        ignored_kinds (List[str], optional): list of kinds to be skip. Defaults to [].

    Returns:
        bool: True if 'kind' is in the 'ignored_kinds' list, False if not
    """
    if not ignored_kinds:
      return False

    if manifest.get("kind", "invalid_value") not in ignored_kinds:
        return False
    return True


def main(argv: List = None):
    parser = argparse.ArgumentParser(
        formatter_class=CustomFormatter,
        description="""
Check if 'filenames' are Kubernetes manifests and have the key 'metadata.namespace'.
Kinds passed with '--ignored-kinds' will not be checked.
""")

    parser.add_argument('filenames',
                        nargs='+',
                        help='filenames to check')
    parser.add_argument('--ignored-kinds', '-i',
                        help='kinds to ignore',
                        dest="ignored_kinds",
                        nargs="*",
                        metavar="Kind",
                        default=[])
    args = parser.parse_args(argv)

    return_code = 0
    for fname in args.filenames:
        manifests = is_kubernetes_manifest(filename=fname)

        for manifest in manifests:
            if not manifest:
                continue

            if not is_ignored_kubernetes_kind(manifest=manifest,
                                                ignored_kinds=args.ignored_kinds):
                continue

            if not is_namespaced_kubernetes_manifest(manifest=manifest):
                print(f"Kubernetes manifest missing namespace: {fname}")
                return_code = 1
                continue

    return return_code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
