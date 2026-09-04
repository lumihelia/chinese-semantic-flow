# Contributing

Chinese Semantic Flow grows from concrete language failures and concrete corrections.

The preferred unit of contribution is a **judgment case**, not a new prohibition.

## Propose a case

Please include:

1. **Context / prompt** — what was being written or discussed;
2. **Original output** — the sentence or response that felt wrong;
3. **Why it fails** — describe the semantic or interaction problem as precisely as possible;
4. **Better version** — one or more alternatives;
5. **Candidate judgment function** — what decision should change before generation;
6. **Boundary conditions** — when the original construction would actually be legitimate;
7. **Scope** — core semantic rule, Chinese-expression rule, dialogue rule, scenario rule, or personal taste;
8. **Benchmark value** — whether this deserves a regression case.

A useful pattern is:

> taste reaction → articulation → rule → example → benchmark → revision

## Contribution principles

- Do not turn a disliked phrase into a universal ban without explaining the mechanism.
- Prefer conditional gates over word blacklists.
- Preserve evidence boundaries; do not add invented facts to make examples vivid.
- Distinguish a personal voice preference from a general Chinese-generation failure.
- Keep authorial stance, uncertainty, and agency intact.
- Include counterexamples when a rule could easily overreach.

## Versioning

Patch releases may add examples, benchmarks, clarifications, or narrow fixes.

Minor releases may add or significantly revise rule modules while keeping the overall philosophy compatible.

Major releases are reserved for changes to the underlying generation philosophy or rule architecture.
