# Rule Taxonomy

Chinese Semantic Flow deliberately separates rules by epistemic status and scope. A recurring taste reaction is useful evidence, but it does not automatically become a universal rule of Chinese writing.

## Layer A — Core semantic rules

These rules are intended to travel across genres and users.

Examples:

- identify the proposition that actually needs to be expressed before choosing rhetoric;
- preserve the difference between fact, inference, uncertainty, and example;
- do not invent concrete details to create vividness;
- preserve causal, conditional, temporal, and contrast relations as they actually exist;
- do not let a rewrite silently change the author’s stance.

## Layer B — Chinese-expression rules

These rules concern recurring tendencies in Chinese generation rather than universal logic.

Examples:

- prefer semantic continuity over mechanically translated connective scaffolding;
- let action, time, causality, and context carry relations when explicit connectors are unnecessary;
- detect contrast-first patterns such as “不是 A，而是 B” when A was never present;
- avoid importing an English argumentative skeleton when Chinese can move by parataxis.

These remain falsifiable. A construction is not banned simply because a model often misuses it.

## Layer C — Interaction rules

These govern dialogue and interpretation.

Examples:

- do not infer emotion or motive when the speaker has only stated a fact;
- do not narrow an unfinished narrative with premature A/B choices;
- let response density follow the moment;
- keep interpretation retractable;
- preserve the other person’s agency and self-definition.

## Layer D — Scenario extensions

These are reusable only when the scenario calls for them.

Examples:

- personal essay movement;
- system-level analysis;
- product/brand/AI explanation;
- conversational playfulness.

## Layer E — Personal taste / persona layers

These belong to a particular author, brand, or conversational persona.

Current examples:

- `extensions/helia-writing.md`
- `extensions/merva-dialogue.md`

They should never be silently promoted into the core Skill.

## Promotion rule

A new observation should normally move through:

> taste reaction → articulation → candidate rule → examples → boundary conditions → benchmark → repeated validation → possible promotion

Questions before promoting a rule:

1. Is the problem semantic, linguistic, conversational, or merely stylistic?
2. Does the rule generalize beyond one author or one example?
3. What legitimate writing would this rule accidentally suppress?
4. Is the rule better expressed as a gate or condition than as a prohibition?
5. Can it be evaluated with a concrete regression case?

## Design stance

The repository is an evolving judgment system, not a prescriptive grammar of “good Chinese.” The goal is to make generation decisions more faithful to thought, evidence, context, and agency while keeping the system open to revision.
