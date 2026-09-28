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

For example, one author's pronoun conventions or essay movement, or a conversational persona's tone and interaction boundaries. This repository ships no Layer E instances; see [`writing-extensions.md`](./writing-extensions.md).

Layer E should never be silently promoted into the core.

## Conflict priority

When rules conflict:

1. **The user's current instruction and the evidence boundary**, jointly highest. The instruction sets the task and what is licensed; the evidence boundary decides what may be written as fact. Explicit fiction or example tasks may license details (csf-004), but licensed content stays identifiable and never poses as fact.
2. **Preserving stance and the author's judgment.**
3. **Task function**, including dialogue density (§11).
4. **Chinese-expression rules** (Layer B).
5. **Style preferences and extensions** (Layer D / E).

The self-check does not conflict with dialogue density: it is the writer's check, not output content. A short reply runs only the dialogue checks.

An author-style rule such as "keep half-formed thought" versus "mechanism before slogan" (core §5) is decided by whose thought it is and what the text is for, as written in core §5: when editing an author's text, do not supply mechanism; when generating text readers will judge or act on, ask for mechanism; when generating text that presents thinking in progress, keep it half-formed but marked unfinished. Private versus public is not the criterion.

## Promotion gate

A new observation normally moves through:

> taste reaction → articulation → candidate rule → examples → boundary conditions → benchmark → repeated validation → possible promotion

Before promotion, ask whether the rule generalizes, what legitimate writing it could suppress, whether a conditional gate is better than a prohibition, whether a valid counterexample exists, and whether the behavior can be tested with a regression case.

## Demotion / relocation

Rules can move down as well as up. If later evidence shows that a core rule is actually author-, persona-, or scenario-specific, relocate it to an extension instead of preserving a false universal claim for historical convenience.

v0.2 is such a relocation pass: portable proposition/evidence/agency rules remain in the core, while one author's essay movement, pronoun conventions, persona playfulness, dynamic self-modeling, and possibility → reality move to scoped extensions.

## Design stance

Chinese Semantic Flow is a revisable judgment system, not a prescriptive grammar of “good Chinese.” Rules stay open to counterexamples and revision.
