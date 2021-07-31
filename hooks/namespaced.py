import argparse
import os
import sys
from typing import List

import yaml


def is_kubernetes_manifest(filename: str) -> List[dict]:
    """is_kubernetes_manifest test if a file is a Kubernetes manifest by loading
    the 'filename' is a valid yaml and has a the key 'apiVersion'. A file can
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


def kubernetes_manifest_has_namespace(manifest: dict) -> bool:
    """kubernetes_manifest_has_namespace check if a dict has the key 'metadata.namespace'

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

    kind = manifest.get("kind", "invalid_value").lower()

    if kind in ignored_kinds:
        return True

    if kind == "kustomization" and "kustomize.config.k8s.io" in manifest.get("apiVersion"):
        return True

    return False


def main(argv: List = None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Check if 'filenames' are Kubernetes manifests and have the key 'metadata.namespace'.
Kinds passed with '--ignore-kind' will not be checked.
""")

    parser.add_argument('filenames',
                        nargs='+',
                        help='filenames to check')
    parser.add_argument('--ignore-kind', '-i',
                        action='extend',
                        default=["Namespace",
                                 "ClusterRole",
                                 "ClusterRoleBinding",
                                 "PersistentVolume",
                                 "StorageClass",
                                 "IngressClass",
                                 "CustomResourceDefinition"
                                 ],
                        dest="ignored_kinds",
                        help="kind to ignore. defaults to %(default)s",
                        nargs=1,
                        metavar="Kind")
    args = parser.parse_args(argv)

    ignored_kinds = [k.lower() for k in args.ignored_kinds]

    return_code = 0
    for fname in args.filenames:
        manifests = is_kubernetes_manifest(filename=fname)

        for manifest in manifests:
            if not manifest:
                continue

            if is_ignored_kubernetes_kind(manifest=manifest,
                                          ignored_kinds=ignored_kinds):
                continue

            if not kubernetes_manifest_has_namespace(manifest=manifest):
                print(f"Kubernetes manifest missing namespace: {fname}")
                return_code = 1
                continue

    return return_code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
