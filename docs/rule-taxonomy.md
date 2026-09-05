# Rule Taxonomy

中文 · [English](./rule-taxonomy.en.md)

Chinese Semantic Flow 按规则的作用域与证据状态分层。一次稳定的 taste reaction 可以成为规则候选，但不会自动变成普遍中文规律。

## Layer A — Core semantic rules

跨作者、跨体裁都应优先成立的语义判断：

- 先确定真正需要表达的命题；
- 保留事实、推断、不确定性与示例之间的区别；
- 具体化不能脱离证据；
- 因果、条件、时间、并列、包含和冲突按照真实关系进入语言；
- 改写不偷偷改变作者立场。

## Layer B — Chinese-expression rules

与中文生成习惯直接相关，而且保持可证伪：

- 语义连续性优先于机械连接词脚手架；
- 动作、时间、因果和上下文足以承载关系时，允许意合；
- contrast-first 需要检查 A 是否真实存在；
- 中文能自然推进时，不机械保留英文论证骨架。

某个结构经常被模型滥用，不等于它本身被禁止。

## Layer C — Interaction rules

对话与解释中的通用边界：

- 信息不足时不替对方补情绪或动机；
- 不用过早的 A/B 候选收窄未完成叙述；
- 解释保持可撤回；
- 回复密度跟随互动阶段；
- 判定权与自我定义留给当事人。

## Layer D — Scenario extensions

只有特定场景需要的可复用规则，例如：

- personal essay movement；
- system-level analysis；
- product / brand / AI explanation；
- conversational playfulness。

这些规则可能跨作者复用，但不默认加载。

## Layer E — House style / persona

属于特定作者、品牌或对话 persona 的规则。

当前实例：

- `extensions/helia-language.md`
- `extensions/helia-writing.md`
- `extensions/merva-dialogue.md`

Layer E 不应被静默提升到 core。

## Promotion gate

一个新观察通常沿这条路径移动：

> taste reaction → articulation → candidate rule → examples → boundary conditions → benchmark → repeated validation → possible promotion

升级规则前问：

1. 这个问题属于语义、中文表达、互动，还是个人 style？
2. 它能否跨作者、跨例子成立？
3. 它会误伤哪些本来合法的表达？
4. 更适合写成条件 gate，还是明确 prohibition？
5. 有没有合法反例证明边界？
6. 能否形成具体 regression case？

## Demotion / relocation

规则也可以向下移动。

如果后续发现一条 core rule 实际只适用于 Helia、Merva 或某种场景，应把它迁到 extension，而不是为了维护历史稳定性继续留在 core。

v0.2 的主要工作就是一次 relocation：保留 core proposition、证据与 agency 等可迁移判断，把 Helia 长文、TA 约定、playfulness、动态 self-modeling 与 possibility → reality 等规则移回对应 extension。

## Design stance

Chinese Semantic Flow 是可修订的 judgment system，不是“好中文”的规定语法。

目标是让生成更忠实于思想、证据、语境与 agency，同时让每条规则都保留反例与修订空间。
