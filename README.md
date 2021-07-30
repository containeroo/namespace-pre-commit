# namespace pre-commit

## example

```yaml
fail_fast: false
repos:
- repo: https://github.com/containeroo/namespace-pre-commit
  rev: v0.0.4
  hooks:
  - id: namespaced
    args:
    - --ignored-kind
    - namespace
    - -i
    - GlobalNetworkPolicy
```
