import argparse
import sys
from typing import List

import yaml


def is_kubernetes_manifest(filename: str) -> List[dict]:
    try:
        with open(file=filename, mode="r") as stream:
            manifests = list(yaml.load_all(stream=stream,
                                           Loader=yaml.SafeLoader))
    except Exception as e:
        return []
    for manifest in manifests:
      if not manifest.get("apiVersion"):
          return []
      return manifests

def is_namespaced_kubernetes_manifest(manifest: dict) -> bool:
    if not manifest.get("metadata"):
        return False
    if not manifest["metadata"].get("namespace"):
        return False
    return True

def is_ignored_kubernetes_kind(manifest: dict, ignored_kinds: List[str] = []) -> bool:
    if not ignored_kinds:
      return False

    if manifest.get("kind", "invalid_value") not in ignored_kinds:
        return False
    return True


def main(argv: List = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames',
                        nargs='*',
                        help='filenames to check')
    parser.add_argument('--ignored-kinds', '-i',
                        help='kinds to ignore (comma separated)',
                        dest="ignored_kinds",
                        metavar="Kind",
                        default="")
    args = parser.parse_args(argv)
    ignored_kinds = [k.strip() for k in args.ignored_kinds.split(",")]

    return_code = 0
    for fname in args.filenames:
        manifests = is_kubernetes_manifest(filename=fname)

        for manifest in manifests:
          if not manifest:
              continue

          if not is_ignored_kubernetes_kind(manifest=manifest,
                                            ignored_kinds=ignored_kinds):
              continue

          if not is_namespaced_kubernetes_manifest(manifest=manifest):
              print(f"Kubernetes manifest missing namespace: {fname}")
              return_code = 1
              continue

    return return_code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
