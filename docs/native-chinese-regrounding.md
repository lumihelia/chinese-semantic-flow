# Native Chinese Re-grounding

> Status: candidate core elaboration. This document deepens v0.3's Chinese-native syntax / information-order rule. It is informed by author calibration on 2026-09-08 and should continue to be tested against independent Chinese sources, counterexamples, and multiple genres before being treated as a complete universal rule.

## 1. Problem

Translationese can survive after vocabulary, connectors, passive voice, and word order have already been cleaned up.

A model may preserve the **conceptual skeleton** of an English proposition:

- an abstract noun remains the actor because English naturally lets it act;
- an English metaphor is translated literally;
- every clause is completed with explicit subjects and relations;
- a proposition is rendered into Chinese without rebuilding the event in Chinese.

The result can be grammatical, understandable Chinese that still feels translated.

## 2. Rebuild the event, not the sentence

When a sentence feels translated, do not begin by replacing individual words.

Recover the underlying event:

1. Who is actually acting, perceiving, deciding, losing, gaining, or changing?
2. What changed in the world?
3. What does Chinese normally call this action or state?
4. Which information is already active in the discourse?
5. What needs to be said now, and what can remain implicit?

Then generate the sentence again from that event.

A practical reminder:

> **先把句子放回现实，再让现实按中文重新发生一次。**

## 3. Abstract actor → native action

Example from author calibration:

Translated-feeling:

> AI 帮我做完越来越多的事，为什么时间没有一起回来？

Native revision:

> AI 能帮我做更多的事，为什么我还是省不下时间？

The important change is not merely `回来 → 省下`. The event structure changes:

- first version: `AI completes more → time should return → time does not return`;
- second version: `AI enables more work → I should save time → I still cannot save time`.

The second uses an established Chinese action relation: `省时间`.

### Boundary

Do not ban abstract subjects. Chinese can naturally say:

> 时间过去了。

> 信息进入系统以后会被重新排序。

> 记忆慢慢模糊了。

The diagnostic question is whether the abstract actor and action are native to the current Chinese expression or inherited from a source-language metaphor.

## 4. Contextual recoverability over local completeness

Chinese discourse often permits subjects, objects, possessors, and relations to remain unspoken when they are recoverable from context.

Example from author calibration:

> 每次换一个 AI，为什么我还得把项目重新跟他讲一遍？

The first clause does not need to become:

> 每次我换一个 AI 的时候……

The subject is already recoverable from the discourse. Completing the clause may be grammatically valid while making the sentence heavier and less natural for the current genre.

### Working principle

> **局部句法不必每次独立完备；篇章里的意义必须持续可恢复。**

This extends the repository's parataxis rule. Chinese can distribute information across several clauses and sentences instead of rebuilding the full proposition each time.

## 5. Do not repeat what the reader already knows

AI systems often optimize for local safety and completeness. This can create repeated explicitness:

- repeating the same subject in adjacent clauses;
- renaming an object that is already active;
- adding connectors for relations already visible from order and action;
- restating the premise before every conclusion;
- turning natural pronoun or zero-anaphora chains into textbook exposition.

A useful editing question:

> **删掉这个成分以后，读者能不能从当前语境自然恢复它？**

If yes, omission may be the more native choice. If no, keep or restore the explicit information.

## 6. Local imperfection is not the goal

Natural Chinese can contain omission, compression, asymmetry, restart, and colloquial sequencing. This does not imply that “human writing” should contain deliberate grammatical errors.

Two failure modes should both be avoided:

### Over-correction

Turning every private or conversational sentence into a textbook-complete sentence.

### Decorative imperfection

Adding fragments, errors, random jumps, or broken grammar merely to simulate a human voice.

The target is **contextual economy**:

> 已经建立的信息少说，真正新增的信息继续往前。

## 7. Genre boundary

Contextual omission is more available in:

- conversation;
- private writing;
- essays;
- memoir-like narration;
- reflective writing;
- scenes where the reader shares a continuous local context.

More explicit local grammar may be useful or necessary in:

- legal writing;
- safety-critical instructions;
- technical specifications;
- contracts;
- reusable API / policy text;
- sentences expected to be quoted independently;
- cross-context handoff where the reader may not share the previous discourse.

Naturalness is therefore not a command to maximize omission. The amount of explicitness follows the reading environment.

## 8. Editing procedure

When a sentence is grammatically correct but still feels translated:

1. Write the actual proposition in plain terms.
2. Identify the current topic and already-known information.
3. Recover the real event and action relation.
4. Remove the existing sentence skeleton from consideration.
5. Generate the sentence again from Chinese-native predicates, collocations, topic/comment structure, and context.
6. Remove repeated information that is safely recoverable.
7. Read the sentence inside the paragraph, not only in isolation.
8. Restore explicit material where omission creates real ambiguity.

## 9. Evaluation tags

Future before/after analysis can use:

- `english_skeleton -> chinese_rebuild`
- `source_metaphor -> native_relation`
- `abstract_actor -> human/action grounding`
- `overexplicit -> recoverable_ellipsis`
- `textbook_completion -> contextual_economy`
- `legitimate_ellipsis -> preserve`
- `real_ambiguity -> explicit_repair`

These tags describe visible output differences. They do not prove what hidden language or proposition the model used internally.

## 10. Relationship to v0.3

v0.3 already states:

> 先用中文理解这句话里的世界，再用中文安排这个世界。

This document adds two operational consequences:

1. **重新着地**：when a conceptual metaphor or abstract actor comes from another language's skeleton, rebuild the event through Chinese-native actions and predicates.
2. **相信语境**：when information is already recoverable, do not repeat it merely to make each sentence locally complete.

The current evidence is strong enough to use these as the calibrating author's house-style rules and as candidate core diagnostics. Wider promotion should keep counterexamples and genre boundaries visible.
