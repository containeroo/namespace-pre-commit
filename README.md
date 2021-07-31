# containeroo pre-commit-hooks

## namespaced

The namespaced hook checks if Kubernetes manifests are namespaced.

It ignores `Namespaces, ClusterRoles, ClusterRoleBindings, PersistentVolumes, StorageClasses, IngressClasses and CustomResourceDefinitions`
by default.

It also ignores all `kustomization.kustomize.config.k8s.io` objects.

You can define other ignored kinds by setting the argument `--ignore-kind KINDNAME` (case insensitive).

## installation

Add a config `.pre-commit-hooks.yaml`

install hooks:

```bash
pre-commit install --install-hooks
```

## examples

### namespaced

```yaml
fail_fast: false
repos:
- repo: https://github.com/containeroo/pre-commit-hooks
  rev: v0.0.11
  hooks:
  - id: namespaced
    args:
    - --ignore-kind
    - clusterpolicy
    - -i
    - GlobalNetworkPolicy
```
