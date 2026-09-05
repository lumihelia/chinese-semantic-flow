# Rule Taxonomy

[中文](./rule-taxonomy.md) · English

Chinese Semantic Flow separates rules by scope and evidence. A recurring taste reaction can become a candidate rule without becoming a universal claim about Chinese.

## Layer A — Core semantic rules

Portable across authors and genres:

- identify the proposition that actually needs to be expressed;
- preserve distinctions among fact, inference, uncertainty, and example;
- keep specificity evidence-bound;
- represent causal, conditional, temporal, parallel, inclusion, and conflict relations faithfully;
- do not let rewriting silently change authorial stance.

## Layer B — Chinese-expression rules

Recurring Chinese-generation tendencies that remain falsifiable:

- prefer semantic continuity over mechanical connective scaffolding;
- let action, time, causality, and context carry relations when explicit connectors are unnecessary;
- gate contrast-first constructions on whether A actually exists;
- avoid importing an English argumentative skeleton when Chinese can move naturally by parataxis.

Frequent model misuse does not make a construction inherently forbidden.

## Layer C — Interaction rules

Portable dialogue and interpretation boundaries:

- do not infer emotion or motive from insufficient evidence;
- do not narrow an unfinished narrative with premature A/B choices;
- keep interpretations retractable;
- let response density follow the moment;
- preserve the other person's agency and self-definition.

## Layer D — Scenario extensions

Reusable only when the scenario calls for them, such as personal essay movement, system analysis, product/brand/AI explanation, or conversational playfulness.

## Layer E — House style / persona

Rules tied to a particular author, brand, or conversational persona.

Current examples:

- `extensions/helia-language.md`
- `extensions/helia-writing.md`
- `extensions/merva-dialogue.md`

Layer E should never be silently promoted into the core.

## Promotion gate

A new observation normally moves through:

> taste reaction → articulation → candidate rule → examples → boundary conditions → benchmark → repeated validation → possible promotion

Before promotion, ask whether the rule generalizes, what legitimate writing it could suppress, whether a conditional gate is better than a prohibition, whether a valid counterexample exists, and whether the behavior can be tested with a regression case.

## Demotion / relocation

Rules can move down as well as up. If later evidence shows that a core rule is actually author-, persona-, or scenario-specific, relocate it to an extension instead of preserving a false universal claim for historical convenience.

v0.2 is such a relocation pass: portable proposition/evidence/agency rules remain in the core, while Helia essay movement, `TA`, playfulness, dynamic self-modeling, and possibility → reality move to scoped extensions.

## Design stance

Chinese Semantic Flow is a revisable judgment system, not a prescriptive grammar of “good Chinese.” Rules stay open to counterexamples and revision.
