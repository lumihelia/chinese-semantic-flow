# Downstream Integration

[中文](./downstream-integration.md) · English

Task-specific skills often need only a subset of Chinese Semantic Flow. Two integration models are recommended.

## A. Runtime composition

Load the Chinese Semantic Flow core, the task skill, and only the extensions the current task actually needs.

This keeps rules current, but requires a host that can compose multiple skills and means behavior can change as upstream evolves.

## B. Vendored profile

Copy a task-scoped subset into the downstream skill's references when the package must distribute independently or freeze behavior.

Record at least:

```yaml
upstream: chinese-semantic-flow@0.2.0
scope:
  - core-proposition
  - forward-progression
  - chinese-parataxis
  - evidence-bound-specificity
local-additions:
  - transcript-fidelity
  - publishable-essay-structure
```

Document which rules are upstream, which are task-local, when drift review is required, and which personal extensions were intentionally excluded.

## Avoid untracked copying

Unmarked duplication causes definitions to drift, upstream fixes to miss downstream packages, and personal taste to leak into supposedly general rules.

## Drift review triggers

Review downstream copies when:

- the core proposition or contrast gate changes;
- fact/inference/stance boundaries change;
- a rule moves between core and extension scope;
- a new benchmark adds a counterexample that changes previous behavior;
- the downstream skill repeatedly patches the same Chinese-generation failure locally.

## Known downstream

### `lumihelia/video-to-chinese-essay`

Its `style-diagnostics.md` predates Chinese Semantic Flow and already contains early parataxis, connective, and contrast-first judgments.

After `chinese-semantic-flow@0.2.0` merges, it should be aligned as a vendored profile: preserve its standalone task package while adding an upstream version marker, B-first generation rule, valid-contrast boundary case, and drift-review convention.
