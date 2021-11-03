# containeroo pre-commit-hooks

## installation

Add a config `.pre-commit-hooks.yaml`

install hooks:

```bash
pre-commit install --install-hooks
```

## namespaced

The namespaced hook checks if Kubernetes manifests are namespaced.

It ignores `Namespaces, ClusterRoles, ClusterRoleBindings, PersistentVolumes, StorageClasses, IngressClasses and CustomResourceDefinitions`
by default.

It also ignores all `kustomization.kustomize.config.k8s.io` objects.

You can define other ignored kinds by setting the argument `--ignore-kind KINDNAME` (case insensitive).

### example

```yaml
fail_fast: false
repos:
- repo: https://github.com/containeroo/pre-commit-hooks
  rev: v0.0.12
  hooks:
  - id: namespaced
    args:
    - --ignore-kind
    - clusterpolicy
    - -i
    - GlobalNetworkPolicy
```

### forbidden_pattern

The forbidden_pattern hook checks if files contains not wanted patterns.

### example

```yaml
fail_fast: false
repos:
- repo: https://github.com/containeroo/pre-commit-hooks
  rev: v0.0.12
  hooks:
  - id: forbid_pattern
    args:
    - --forbidden_pattern
    - secret
    - -f
    - "name:\s+super-secret"
```
