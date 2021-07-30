# containeroo pre-commit-hooks

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
    - --ignored-kind
    - namespace
    - -i
    - GlobalNetworkPolicy
```
