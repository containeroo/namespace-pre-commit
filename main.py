import argparse
import sys
import yaml


def is_namespaced_kubernetes_manifest(filename):
    try:
        with open(filename) as stream:
            manifest = yaml.safe_load(stream)
    except Exception as e:
        return None
    if not manifest.get("apiVersion"):
        return None
    if not manifest.get("metadata"):
        return None
    if not manifest["metadata"].get("namespace"):
        return None
    return manifest


def is_ignored_kubernetes_kind(manifest, ignored_kinds):
    if manifest.get("kind", "invalid_value") not in ignored_kinds:
        return False
    return True


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='filenames to check')
    parser.add_argument('--ignored-kinds', help='kinds to ignore (comma separated)', dest="ignored_kinds",
                        metavar="Kind", default="")
    args = parser.parse_args(argv)
    ignored_kinds = [k.strip() for k in args.ignored_kinds.split(",")]

    return_code = 0
    for fname in args.filenames:
        manifest = is_namespaced_kubernetes_manifest(filename=fname)
        if not manifest:
            print(f"")
        if not is_namespaced_kubernetes_manifest(filename=fname):
            print(f"Kubernetes manifest missing namespace: {invalid_manifest_file}")
            return_code = 1
            continue

        if not is_ignored_kubernetes_kind(manifest=manifest, )

    return return_code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
