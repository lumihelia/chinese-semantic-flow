# Chinese Semantic Flow

[中文](./README.md) · English

**Make language follow the movement of thought.**

Chinese Semantic Flow is an evolving Agent Skill for Chinese generation, rewriting, editing, and dialogue. It focuses on generation decisions before surface style: what proposition a sentence starts from, how the next sentence grows from it, whether linguistic relations match the underlying reasoning, whether Chinese syntax and information order fit the discourse, whether evidence and inference remain distinct, and whether a rewrite preserves the author's stance.

**Current version: `v0.4.1`**

The repository contains the core Skill, traceable regression cases, and a diagnostic evaluation toolkit that never calls a model. A cross-source quality benefit from the core has not been established; `Better` labels are repository judgments, not gold keys.

## Core principle

Identify the proposition B that is actually true and relevant before generating the sentence.

If B already stands on its own, state B. Introduce a contrast, negation, or correction only when the proposition A being corrected can be traced to the text and handling it adds information; when no basis can be named, generate from B.

The important change happens before wording:

> **Avoiding contrast-first means A should not become the default starting point.**

A common forward movement is:

> observation → judgment → mechanism → consequence → feedback → new understanding

This is a direction of thought, not a fixed essay template. B only needs to be settled before writing; where the output starts is decided by genre.

## v0.4: tiering, gate evidence, positive shapes

v0.4 answers one round of external review and includes one author calibration:

- **High-leverage rules**: B and the contrast gate, native Chinese syntax, the evidence boundary, and stance preservation are core; the rest are supporting and become core when a task triggers them.
- **Tiered self-check**: four checks every time; the rest trigger by generation, rewriting, dialogue, compression into UI copy, or extension loading. The self-check never adds content to output.
- **Text-evidence gate**: A must point to the text; without a nameable basis, generate from B.
- **Operational B-first**: B must be settled in planning; the text need not open with its conclusion.
- **Conflict priority** and the half-formed-thought criterion live in `docs/rule-taxonomy.md` and core §5.
- **Positive shapes** (core §5.1): explanation, product copy, and dialogue examples chosen or rewritten by the author.
- In causal explanations, explicit connectors often carry real relations; deleting them for parataxis breaks the mechanism chain.

## v0.3: native Chinese syntax and information order

v0.3 moves translationese diagnostics below the vocabulary/connective layer.

A model can produce sentences made entirely of correct Chinese words while still organizing them around an English proposition. The result may preserve English subject placement, static property statements, passive structure, nominalization, adverbial placement, or an English-style requirement to state every component explicitly.

The new core rule is:

> **Organize the sentence through Chinese discourse structure before realizing it as wording.**

Sentence order should serve Chinese topic/comment structure, given/new information, temporal and spatial framing, action relations, and attention movement.

For example, when the discourse is grounded in ordinary perception:

> 投影、追踪、巨型灯光这些技术，平时很容易出现在广告、商业活动中。

may become:

> 我们平时经常在广告、商业活动中看到类似投影、追踪、巨型灯光这些技术。

The point is not to create a new person-first template. These are also natural when their framing function is real:

> 到了晚上，一整面建筑外墙会出现互动投影。

> 在 Body Movies 中，我们只需要走进光里，在墙上留下影子。

A compact reminder:

> **Understand the sentence's world in Chinese first; then arrange that world in Chinese.**

## v0.2: a layered rule system

v0.1 intentionally collected a wide set of accumulated rules in one place. That made the map visible, but it also mixed portable Chinese-generation rules with one author's writing taste, persona behavior, and system-analysis habits.

v0.2 separates scope:

| Layer | Covers | Loaded by default |
| --- | --- | --- |
| Core semantic | proposition-first, relation fidelity, evidence/inference, stance preservation | yes |
| Chinese expression | forward progression, parataxis, native syntax/information order, contrast gate, translationese checks | yes |
| Interaction | inference restraint, agency, dynamic response density | yes |
| Scenario / house style | author, persona, system lens, playfulness | on demand |

The core can travel across authors and products. Personal taste remains available without being presented as a universal rule of Chinese.

## Extensions

The core carries no personal taste. One author's pronoun conventions or essay movement, or a persona's tone and soothing boundaries, belong in a separate extension loaded on demand. This repository ships no personal extensions; see [`docs/writing-extensions.md`](./docs/writing-extensions.md).

## Installation

Install the whole directory in a host-supported Agent Skills location so benchmarks and docs remain available.

Common locations include:

```text
# Codex
~/.codex/skills/chinese-semantic-flow/

# Claude Code
~/.claude/skills/chinese-semantic-flow/

# Windsurf global
~/.codeium/windsurf/skills/chinese-semantic-flow/

# Windsurf workspace
.windsurf/skills/chinese-semantic-flow/
```

Some hosts also discover `.agents/skills/` or provide a Skills UI. Follow current host documentation for exact discovery behavior.

Copying only `SKILL.md` gives you the portable core. Write author- or persona-specific rules as your own extension and load it alongside the core.

## Usage

```text
Use chinese-semantic-flow to rewrite this Chinese paragraph. Preserve the author's stance, uncertainty, and voice; do not add facts.
```

```text
Use chinese-semantic-flow and load extensions/my-house-style.md.
```

## Why this is different from a Humanizer

A Humanizer usually detects visible AI-writing patterns and cleans them up afterward.

Chinese Semantic Flow moves the intervention earlier: which proposition should exist at all, how Chinese discourse should order the information, which relation is being expressed, what can be inferred, and where generation should stop. Natural language is one outcome of better judgment rather than the sole target.

## Rule taxonomy and evaluation

Rule layers, conflict priority, and the promotion gate: [`docs/rule-taxonomy.en.md`](./docs/rule-taxonomy.en.md). New observations move through taste reaction → articulation → candidate rule → boundary → benchmark → repeated validation → revision. v0.3 deliberately stores counterexamples to the narrower person-first hypothesis so a useful insight does not harden into another template.

[`benchmarks/cases.en.md`](./benchmarks/cases.en.md) keeps regression cases with bad examples and legal counterexamples. [`evaluation/`](./evaluation/README.md) turns them into blind-review diagnostics: 34 core cases, pinned rule excerpts, a six-dimension rubric, and a standard-library harness.

```sh
python3 -m evaluation.harness validate
python3 -m unittest discover -s tests -v
```

## Downstream skills

Task-specific skills can compose with the core at runtime or vendor a scoped profile. Version markers and drift rules are documented in [`docs/downstream-integration.en.md`](./docs/downstream-integration.en.md).

## Contributing

The most useful contribution is a concrete judgment case: the sentence that fails, why, a better version, boundaries, and legal counterexamples. See [`CONTRIBUTING.en.md`](./CONTRIBUTING.en.md).

## License

MIT
