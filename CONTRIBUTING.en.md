# Contributing

[中文](./CONTRIBUTING.md) · English

Chinese Semantic Flow grows from concrete language failures and concrete corrections.

The preferred contribution unit is a **judgment case**, not a new prohibition.

## Propose a case

Please include:

1. context / prompt;
2. original output;
3. why it fails at the semantic, evidence, interaction, or scope level;
4. one or more better versions;
5. the candidate judgment function that should change before generation;
6. boundary conditions where the original construction is valid;
7. scope: core semantic, Chinese expression, interaction, scenario, or house style;
8. whether the case deserves a regression benchmark.

Preferred evolution path:

> taste reaction → articulation → candidate rule → boundary → benchmark → repeated validation → revision

## Principles

- Do not turn a disliked phrase into a universal ban without a mechanism.
- Prefer conditional gates over word blacklists.
- Keep specificity evidence-bound.
- Distinguish personal voice from portable Chinese-generation failures.
- Preserve authorial stance, uncertainty, and agency.
- Add counterexamples when a rule can suppress legitimate writing.
- Rules may be promoted, demoted, or relocated into extensions.

## Core changes

A core change should identify the reproducible failure, explain why it generalizes, name likely false positives, update benchmarks, and identify downstream vendored profiles that need drift review.

## Extension changes

State the author, persona, or scenario the rule belongs to. Extensions are allowed to be specific; they do not need to pretend to be universal.

## Versioning

- Patch: examples, benchmarks, boundary clarifications, narrow fixes.
- Minor: compatible rule modules or architecture refactors.
- Major: changes to the underlying generation philosophy or rule architecture.
