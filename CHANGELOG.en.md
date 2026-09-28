# Changelog

[中文](./CHANGELOG.md) · English

## v0.4.1 — first public release

- The repository is public and contains only the core Skill, core benchmarks, the diagnostic toolkit, and docs. Personal extensions, author calibration records, and research experiments stay in the author's private repository.
- The diagnostic dataset holds 34 core cases; source excerpts are re-pinned to this repository's first commit.
- The case `profile` field accepts `core` or any extension slug.
- Adds `docs/writing-extensions.md` on writing your own author-style or persona extension.
- SKILL.md rules are unchanged from v0.4.0; only references to private records and personal extensions were removed.

## v0.4.0

Answers one round of external review and includes one author calibration.

- **High-leverage rules**: B and the contrast gate (§0 + §16), native Chinese syntax (§4.1 / 4.2), the evidence boundary (§6–7) and stance preservation (§13–14) are core; the rest are supporting and become core when triggered.
- **Tiered final self-check**: four checks every time; the rest trigger by task. The self-check never adds content to output.
- **Text-evidence gate**: A must point to the text; without a basis, generate from B.
- **Operational B-first**: B must be settled in planning; genre decides where output starts.
- **Half-formed thought vs mechanism** (§5): decided by whose thought it is and what the text is for.
- **Conflict priority** (`docs/rule-taxonomy.en.md`).
- **Positive shapes** (§5.1): explanation, product copy, and dialogue examples chosen or rewritten by the author.
- **§4 counter-direction**: in causal explanations, explicit connectors often carry real relations. Evidence: rewriting an explanation, the author restored the 因为 / 然后 / 于是 / 所以 the Agent had dropped.

## v0.3.1 – v0.3.3

- Adds §4.2: keep the event when compressing into titles or UI copy (result complements, `是……的` for "how", no redundant reciprocity, a question stays a question); navigation labels are exempt.
- From one real author correction and follow-up judgments: topic anchoring and `那些……，它们……` resumption are not necessary; resumption is a colloquial register choice.
- Adds minimal pairs csf-041 / 042 / 043.

## v0.3.0

Moves translationese diagnostics below vocabulary and connectives to native Chinese syntax and discourse information order: topic/comment, given/new information, temporal and spatial framing, action relations, and attention movement. Legal counterexamples keep `person-first` from becoming a template.

## v0.2.0

First rule-architecture pass: the core narrows to portable semantic, Chinese-expression, interaction, and editing judgments; personal writing taste and persona rules move to extensions.
