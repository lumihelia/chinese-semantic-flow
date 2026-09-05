# Chinese Semantic Flow

[中文](./README.md) · English

**Make language follow the movement of thought.**

Chinese Semantic Flow is an evolving Agent Skill for Chinese generation, rewriting, editing, and dialogue. It focuses on generation decisions before surface style: what proposition a sentence starts from, how the next sentence grows from it, whether linguistic relations match the underlying reasoning, whether evidence and inference remain distinct, and whether a rewrite preserves the author's stance.

**Current version: `v0.2.0`**

## Core principle

Identify the proposition B that is actually true and relevant before generating the sentence.

If B already stands on its own, start from B. Introduce a contrast, negation, or correction only when the proposition A being corrected already exists in the context and handling it adds information.

The important change happens before wording:

> **Avoiding contrast-first means A should not become the default starting point.**

A common forward movement is:

> observation → judgment → mechanism → consequence → feedback → new understanding

This is a direction of thought, not a fixed essay template.

## v0.2: a layered rule system

v0.1 intentionally collected a wide set of accumulated rules in one place. That made the map visible, but it also mixed portable Chinese-generation rules with Helia-specific writing taste, Merva persona behavior, and system-analysis habits.

v0.2 separates scope:

| Layer | Covers | Loaded by default |
| --- | --- | --- |
| Core semantic | proposition-first, relation fidelity, evidence/inference, stance preservation | yes |
| Chinese expression | forward progression, parataxis, contrast gate, translated-syntax checks | yes |
| Interaction | inference restraint, agency, dynamic response density | yes |
| Scenario / house style | author, persona, system lens, playfulness | on demand |

The core can travel across authors and products. Personal taste remains available without being presented as a universal rule of Chinese.

## Optional extensions

- `extensions/helia-language.md` — Helia's cross-surface pronoun and direct-address conventions, including unknown gender → `TA` and pronoun economy.
- `extensions/helia-writing.md` — thought formation over time, private-to-public essay movement, system variables, possibility → reality, dynamic self-modeling.
- `extensions/merva-dialogue.md` — acknowledge-without-soothing, open conversational floor, contextual playfulness, restrained stage directions, relationship continuity.

## Installation

Install the whole directory in a host-supported Agent Skills location so extensions, benchmarks, and docs remain available.

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

Copying only `SKILL.md` gives you the portable core. Keep the relevant extension files when you want author- or persona-specific behavior.

## Usage

```text
Use chinese-semantic-flow to rewrite this Chinese paragraph. Preserve the author's stance, uncertainty, and voice; do not add facts.
```

For Helia's house style:

```text
Use chinese-semantic-flow plus extensions/helia-language.md and extensions/helia-writing.md.
```

For Merva:

```text
Use the chinese-semantic-flow core plus extensions/merva-dialogue.md. Load extensions/helia-language.md when Merva should inherit Helia's pronoun conventions.
```

## Why this is different from a Humanizer

A Humanizer usually detects visible AI-writing patterns and cleans them up afterward.

Chinese Semantic Flow moves the intervention earlier: which proposition should exist at all, which relation is being expressed, what can be inferred, and where generation should stop. Natural language is one outcome of better judgment rather than the sole target.

## Rule taxonomy and benchmarks

See [`docs/rule-taxonomy.en.md`](./docs/rule-taxonomy.en.md) for scope and promotion rules, and [`benchmarks/cases.en.md`](./benchmarks/cases.en.md) for regression cases.

A new observation normally moves through:

> taste reaction → articulation → candidate rule → boundary → benchmark → repeated validation → revision

## Downstream skills

Task-specific skills can compose with the core at runtime or vendor a scoped profile. Version markers and drift rules are documented in [`docs/downstream-integration.en.md`](./docs/downstream-integration.en.md).

`video-to-chinese-essay` is a known early downstream candidate for alignment: its style diagnostics predate v0.2 and should adopt the upstream-version convention rather than evolve as an untracked duplicate.

## Repository map

```text
SKILL.md
extensions/
benchmarks/
docs/
README.md
README.en.md
CONTRIBUTING.md
CONTRIBUTING.en.md
CHANGELOG.md
CHANGELOG.en.md
LICENSE
```

## License

MIT. See [`LICENSE`](./LICENSE).
