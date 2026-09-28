# Benchmark Cases

[中文](./cases.md) · English

These cases preserve existing repository judgments; they are not independently calibrated gold labels. This file contains core cases only. Historical Bad/Better labels need context and fidelity review before use as scoring keys. Final text cannot establish a hidden generation path.

See the [diagnostic evaluation guide](../evaluation/README.md) for executable cases, blind review, and provenance. Original examples remain below for traceability.

## Core 001 — Unsupported contrast

Prompt: explain what a brand is.

Bad: `品牌不是一个 logo，而是一套完整的认知系统。`

Better: `品牌组织人们如何识别、记忆和理解一个对象，也参与身份与价值的形成。`

Rule: B-first / contrast gate.

## Core 002 — Mechanism before slogan

Bad: `AI 不只是工具，更是我们的认知环境。`

Better: `当 AI 持续参与信息选择、记忆调用、判断形成和行动反馈时，它会逐渐成为认知环境的一部分。`

## Core 003 — Valid contrast should survive

Context: the other speaker has explicitly said `品牌说到底就是 logo 和视觉。`

Valid response: `品牌不只由视觉识别构成。命名、叙事、产品体验和长期重复出现的行为，也会参与人们如何识别和记住它。`

Rule: the contrast gate is conditional, not a ban.

## Core 004 — Do not treat deleting A as the generation strategy

Prompt: explain why high-density communities need recovery space.

Weak shape: `社区不是越热闹越好。真正重要的是……`

Better: `高频互动会持续消耗注意力和社交能量。社区如果同时提供可退出、独处和恢复的空间，成员更容易长期留在高密度关系中。`

## Core 005 — Emotion inferred from insufficient evidence

User: `今天朋友没回我。`

Bad: `你是不是有点失落，也担心朋友在疏远你？`

Better: `怎么说？`

## Core 006 — Premature A/B narrowing

User: `我最近不太想去那个活动。`

Bad: `是因为你觉得社交太累，还是觉得那里的人不适合你？`

Better: `为什么不太想去？`

## Core 007 — Invented specificity

Input: `这家咖啡馆在杭州。`

Bad rewrite adds unsupported years, specialty, and architecture details.

Better: keep the known fact and add detail only from evidence.

## Core 008 — Three-item inertia

> 2026-09-08 Review: the Chinese Better also adds temporal/progressive structure; see csf-031/032.

If the material supports attention and action only, do not invent “identity” just to complete a triad.

## Core 009 — Rewrite upgrades uncertainty

> 2026-09-08 Review: Better adds onset and additive meaning through 开始/也. KEEP remains valid; see csf-025.

Input: `我现在会怀疑，这可能和工作环境有关。`

Bad: `我意识到，问题的根源就在工作环境。`

Better: `我开始怀疑，这件事可能也和工作环境有关。`

## Core 010 — Abstraction replaces mechanism

> 2026-09-08 Review: no product evidence is supplied here. The mechanism is illustrative only when supported; see csf-021/022.

Bad: `这个产品重塑了人与城市之间的关系。`

Better: describe the added actions—staying, responding, participating with strangers—and how those actions expand ways of relating to the city.

## Core 011 — Over-complete reply

User: `不知道呢，可能只是顺手也不一定。`

Better: `嗯，也完全可能只是顺手。`

## Core 012 — Correct Chinese words can still preserve an English sentence skeleton

> 2026-09-08 Review: this pair changes viewpoint, wording, and scene coverage together. It cannot isolate word-order effects or establish hidden thought language; see csf-013/014/039/040.

Context: the author is moving from ordinary experience into a judgment about interactive urban technology.

AI-ish:

`投影、追踪、巨型灯光这些技术，平时很容易出现在广告、商业活动和大型 spectacle 里。`

Native Chinese revision:

`其实，我们平时经常在广告、商业活动中看到类似投影、追踪、巨型灯光这些技术。`

The improvement is not simply “put the person first.” The revised sentence follows a lived perception sequence: we → usually → in these contexts → see → these technologies. The verb `看到` carries the relation between observer and object.

Valid counterexamples:

`到了晚上，一整面建筑外墙会出现互动投影。`

`在 Body Movies 中，我们只需要走进光里，在墙上留下影子。`

Temporal, spatial, scope, or topic framing can naturally come first when it has a real discourse function.

Rule: Chinese-native syntax and discourse information order. Do not form an English proposition first and replace its words with Chinese. Order the sentence through Chinese topic/comment structure, given/new information, framing, action relations, and attention movement.

## Core 013 — Compression into UI copy drops the event

From a real author correction of agent-written UI copy. The pair changes four things at once and cannot isolate a single mechanism; see csf-041/042/043 for split minimal pairs.

AI-ish: `写下来的问题，彼此怎么相连`

Author revision: `那些写下来的问题，它们是怎么连起来的？`

The compressed line keeps a noun-phrase topic and a stative reciprocal verb: no result complement, redundant `彼此` with `相连`, and a lost question mark. Legal counterexamples: navigation labels such as `问题地图` and `思想年表` are nominal by design. The author also accepted `写下来的问题是怎么连起来的？` (without `那些` or `它们`), so neither anchoring nor resumption is necessary. She later added that this version is more natural and suits most written presentation, while her own is more colloquial.

Rule: Core 4.2 — compress modifiers and argument, not the event.
