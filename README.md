# Chinese Semantic Flow

中文 · [English](./README.en.md)

**让语言忠实于思考的运动。**

Chinese Semantic Flow 是一个持续迭代的中文生成、改写、编辑与对话 Agent Skill。它把主要约束放在生成判断本身：一句话从什么命题开始、后文如何继续、语言关系是否忠实映射思想关系、事实与推断有没有越界、改写有没有替原作者改变立场。

**当前版本：`v0.2.0`**

## 核心原则

生成句子前，先确定真正成立的核心命题 B。

B 已经成立时，直接从 B 开始，让后文沿 B 的语义继续向前。只有当需要回应的 A 已经真实存在，而且处理 A 会增加理解时，才引入转折、否定或纠正。

这里的重点发生在生成之前：

> **避免 contrast-first 的正确实现，是 A 不成为默认起点。**

默认的思考运动可以写成：

> 观察 → 判断 → 机制 → 后果 → 反馈 → 新的理解

这是一种推进方向，不是固定文章模板。

## v0.2：从“大而全”变成分层系统

v0.1 先把长期积累的规则尽可能收进同一份 Skill，方便建立完整地图。它也因此把通用中文规则、对话原则、Helia 的个人写作 taste、Merva persona 和系统分析习惯混在了一起。

v0.2 把规则按作用域重新分层：

| 层 | 内容 | 默认加载 |
| --- | --- | --- |
| Core semantic | proposition-first、关系忠实、事实/推断边界、立场保真 | 是 |
| Chinese expression | forward progression、意合、contrast gate、翻译腔检查 | 是 |
| Interaction | inference restraint、agency、动态信息密度 | 是 |
| Scenario / house style | 特定作者、persona、系统视角、playfulness | 按需 |

这样，同一份 core 可以迁移到其他作者和产品；个人 taste 继续保留，而且不会被悄悄包装成“普遍的好中文”。

## Core 现在负责什么

- Semantic-first generation
- Core proposition / B-first generation
- Forward semantic progression
- Contrast gate
- Chinese parataxis
- Relation fidelity：因果、递进、并列、条件、时间、冲突、不确定性
- Evidence-bound specificity
- Retractable inference
- Agency-preserving dialogue
- Conversational density control
- Authorial stance preservation
- Anti-template checks：三段式惯性、过度总结、虚假抽象、装饰性“人味”

## 可选扩展

### `extensions/helia-language.md`

跨场景 house style：

- 性别未知时使用 `TA`；
- 减少无功能的「你」；
- 优先显式对象、自然省略主语，或在共同主体成立时使用「我们」；
- 代词需要承担信息功能。

### `extensions/helia-writing.md`

Helia 的长文与思考运动：

- 保留思想形成的时间；
- 从具体私人经验进入公共问题；
- 从我出发，经过世界，最后抵达我们；
- 系统变量与 possibility → reality；
- 动态自我理解。

### `extensions/merva-dialogue.md`

Merva 的 persona / dialogue layer：

- acknowledge without soothing；
- 信息不足时把话匣子交回对方；
- contextual cognitive / relational playfulness；
- 克制舞台动作和角色表演；
- 关系连续性高于语言装饰。

## 为什么把 extensions 拆出去

一个规则是否有效，和它适用于谁、什么场景，是两个不同问题。

例如 `TA` 是 Helia 明确采用的中文约定，但它不是中文语法的普遍结论；Merva 的可爱气质也可以设计得很好，却不应该进入每个中文 Agent 的默认行为。

分层以后，core 保存可迁移的判断函数，extensions 保存特定作者、persona 与场景的 taste。

## 安装

这个仓库符合 Agent Skills 的 `SKILL.md` 目录形态。把整个仓库放进宿主支持的 skills 目录即可保留 extensions、benchmarks 和 docs。

常见位置包括：

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

部分宿主也支持 `.agents/skills/` 或自己的 Skills UI。实际发现路径以当前宿主文档为准。

只复制 `SKILL.md` 也能使用 core；需要个人/场景规则时，应同时保留对应 extension 文件。

## 使用示例

### 生成

```text
请使用 chinese-semantic-flow 写一段中文，解释 AI 长期记忆会怎样改变人机协作。
```

### 改写

```text
请用 chinese-semantic-flow 改写下面这段话，保留原来的观点、语气和不确定性，不增加新事实：
[文本]
```

### Helia house style

```text
使用 chinese-semantic-flow，并加载 extensions/helia-language.md 与 extensions/helia-writing.md。
```

### Merva

```text
使用 chinese-semantic-flow core，并加载 extensions/merva-dialogue.md；如果需要继承 Helia 的代词规则，再加载 extensions/helia-language.md。
```

## 和 Humanizer 类工具的区别

Humanizer 常从表面语言模式识别 AI 痕迹，再清理可见特征。

Chinese Semantic Flow 把检查点放到更早的生成判断：真正成立的命题是什么、关系怎样排列、哪些内容可以推断、哪些地方应当停住。语言自然度是这些判断正确之后产生的结果之一。

## Rule taxonomy

规则分层与 promotion gate 见 [`docs/rule-taxonomy.md`](./docs/rule-taxonomy.md)。

一个新观察通常沿这条路径生长：

> taste reaction → articulation → candidate rule → boundary → benchmark → repeated validation → revision

仓库不会把一次个人偏好直接升级为普遍规则。

## Benchmarks

[`benchmarks/cases.md`](./benchmarks/cases.md) 保存 regression cases，同时包含“坏例子”和“合法反例”。合法反例很重要：它防止 contrast gate、意合和 inference restraint 逐渐变成机械禁令。

## 下游 Skill

任务型 Skill 可以复用 Chinese Semantic Flow 的一部分规则。推荐的两种方式、版本标记与 drift review 见 [`docs/downstream-integration.md`](./docs/downstream-integration.md)。

`video-to-chinese-essay` 是当前已知需要回头对齐的早期下游：它的 style diagnostics 形成得更早，核心方向一致，但还没有 v0.2 的分层与 upstream-version 约定。

## 仓库结构

```text
SKILL.md                         # portable core
extensions/
  helia-language.md              # Helia house-style language rules
  helia-writing.md               # Helia writing/thinking extension
  merva-dialogue.md              # Merva persona/dialogue extension
benchmarks/
  cases.md
  cases.en.md
docs/
  rule-taxonomy.md
  rule-taxonomy.en.md
  downstream-integration.md
  downstream-integration.en.md
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
