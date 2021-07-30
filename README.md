# containeroo pre-commit-hooks

## installation

add a config `.pre-commit-hooks.yaml`, for content see examples.

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
  rev: v0.0.4
  hooks:
  - id: namespaced
    args:
    - --ignore-kind
    - clusterpolicy
    - -i
    - GlobalNetworkPolicy
```
