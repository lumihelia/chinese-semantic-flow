# Benchmark Cases

[中文](./cases.md) · English

These cases test whether the rules change generation decisions. Core and extension cases are separated, and valid counterexamples prevent conditional rules from turning into word bans.

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

If the material supports attention and action only, do not invent “identity” just to complete a triad.

## Core 009 — Rewrite upgrades uncertainty

Input: `我现在会怀疑，这可能和工作环境有关。`

Bad: `我意识到，问题的根源就在工作环境。`

Better: `我开始怀疑，这件事可能也和工作环境有关。`

## Core 010 — Abstraction replaces mechanism

Bad: `这个产品重塑了人与城市之间的关系。`

Better: describe the added actions—staying, responding, participating with strangers—and how those actions expand ways of relating to the city.

## Core 011 — Over-complete reply

User: `不知道呢，可能只是顺手也不一定。`

Better: `嗯，也完全可能只是顺手。`

## Extension 101 — Unknown gender → TA

Applies only under `extensions/helia-language.md`.

## Extension 102 — Pronoun economy

Weak: `当你使用这个功能时，你可以看到你保存过的所有材料。`

Better: `这个页面会显示已保存的全部材料。`

## Extension 103 — Preserve thought formation over time

Applies under `extensions/helia-writing.md`; do not rewrite a later realization as something the author “always knew.”

## Extension 104 — Contextual playfulness

Applies under `extensions/merva-dialogue.md`; the playful reaction must call back to something that actually happened in the conversation.

## Extension 105 — Template cuteness

Generic childish phrasing without context is a failure even if it sounds “cute.”

## Extension 106 — Automatic soothing

Merva should not default to reassurance when the more useful response is accurate acknowledgment and situation analysis.
