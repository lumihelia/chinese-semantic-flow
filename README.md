# Chinese Semantic Flow

中文 · [English](./README.en.md)

**让语言忠实于思考的运动。**

Chinese Semantic Flow 是一个持续迭代的中文生成、改写、编辑与对话 Agent Skill。它把主要约束放在生成判断本身：一句话从什么命题开始、后文如何继续、语言关系是否忠实映射思想关系、中文句法与信息顺序是否自然、事实与推断有没有越界、改写有没有替原作者改变立场。

**当前版本：`v0.4.1`**

仓库包含 core Skill、可追溯的 regression cases 与一套不调用模型的诊断评估工具。当前尚未证明 core 的跨来源质量收益；`Better` 标签是仓库判断，不是金标准。

## 核心原则

生成句子前，先确定真正成立的核心命题 B。

B 已经成立时，直接表达 B，让后文沿 B 的语义继续向前。只有当需要回应的 A 能指向文本依据，而且处理 A 会增加理解时，才引入转折、否定或纠正；说不出依据时，默认从 B 生成。

这里的重点发生在生成之前：

> **避免 contrast-first 的正确实现，是 A 不成为默认起点。**

默认的思考运动可以写成：

> 观察 → 判断 → 机制 → 后果 → 反馈 → 新的理解

这是一种推进方向，不是固定文章模板。B 只需要在写之前想清楚，输出从哪里开始由文体决定。

## v0.4：分层、门控与正面形状

v0.4 回应了一轮外部评审，并经过一次作者校准：

- **高杠杆规则**：B 与对照 gate、中文原生句法、证据边界、立场不漂移四组为核心；其余为 supporting，任务触发时同样是核心；
- **分层自检**：每次必查 4 问，其余按生成、改写、对话、压缩成 UI 文案、加载 extension 触发；自检不往输出里加内容；
- **门控看文本依据**：A 必须能指向文本，说不出依据时默认从 B 生成；
- **B-first 操作化**：B 在规划里成立即可，不要求文章把结论放在开头；
- **冲突优先级**与“半成型 vs 机制”的判定写入 `docs/rule-taxonomy.md` 与 core §5；
- **正面形状**（core §5.1）：解释文、产品文案、对话三个经作者选择或改写的示例；
- 解释因果链时，显性连接词常常承担真实关系，为“意合”删掉会让机制链断开。

## v0.3：把“翻译腔”推进到句法与信息结构层

v0.3 增加一条新的 core 判断：**中文写作需要按中文自身的句法、篇章信息结构与注意力顺序组织句子。**

过去对“翻译腔”的检查容易停在词汇、连接词、名词化和被动语态。更深的一层是：模型可能先按英语习惯形成一个完整 proposition，再把词替换成中文。这样即使每个词都正确，句子的视角、动作顺序、话题推进和信息落点仍然可能带着英语骨架。

例如：

> 投影、追踪、巨型灯光这些技术，平时很容易出现在广告、商业活动中。

在强调人的日常感知时，可以自然写成：

> 我们平时经常在广告、商业活动中看到类似投影、追踪、巨型灯光这些技术。

这里没有产生“人必须放句首”的新模板。时间、地点、范围或话题承担真实 framing function 时，仍然可以自然前置：

> 到了晚上，一整面建筑外墙会出现互动投影。

> 在 Body Movies 中，我们只需要走进光里，在墙上留下影子。

因此 v0.3 真正要求的是：

> **让语序服务于中文语境中的已知 / 新信息、话题 / 述题、时间地点框架、动作关系和注意力移动。**

一句简化提醒：

> **先用中文理解这句话里的世界，再用中文安排这个世界。**

## v0.2：从“大而全”变成分层系统

v0.1 先把长期积累的规则尽可能收进同一份 Skill，方便建立完整地图。它也因此把通用中文规则、对话原则、个人写作 taste、persona 规则和系统分析习惯混在了一起。

v0.2 把规则按作用域重新分层：

| 层 | 内容 | 默认加载 |
| --- | --- | --- |
| Core semantic | proposition-first、关系忠实、事实/推断边界、立场保真 | 是 |
| Chinese expression | forward progression、意合、中文原生句法与信息结构、contrast gate、翻译腔检查 | 是 |
| Interaction | inference restraint、agency、动态信息密度 | 是 |
| Scenario / house style | 特定作者、persona、系统视角、playfulness | 按需 |

这样，同一份 core 可以迁移到其他作者和产品；个人 taste 继续保留，而且不会被悄悄包装成“普遍的好中文”。

## Core 现在负责什么

- Semantic-first generation
- Core proposition / B-first generation
- Forward semantic progression
- Chinese-native syntax and discourse information order
- Contrast gate
- Chinese parataxis
- Relation fidelity：因果、递进、并列、条件、时间、冲突、不确定性
- Evidence-bound specificity
- Retractable inference
- Agency-preserving dialogue
- Conversational density control
- Authorial stance preservation
- Anti-template checks：三段式惯性、过度总结、虚假抽象、装饰性“人味”

## Extensions

Core 不携带个人 taste。某位作者的代词约定、长文运动，或某个对话 persona 的语气与安抚边界，写成单独的 extension，按需加载。

一个规则是否有效，和它适用于谁、什么场景，是两个不同问题。例如“性别未知时用 TA”可以是某位作者明确采用的约定，却不是中文语法的普遍结论。

本仓库不包含个人 extension。写法见 [`docs/writing-extensions.md`](./docs/writing-extensions.md)。

## 安装

这个仓库符合 Agent Skills 的 `SKILL.md` 目录形态。把整个仓库放进宿主支持的 skills 目录即可保留 benchmarks 和 docs。

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

只复制 `SKILL.md` 也能使用 core。个人或场景规则写成自己的 extension，与 core 一起加载。

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

### 加载自己的 extension

```text
使用 chinese-semantic-flow，并加载 extensions/my-house-style.md。
```

## Rule taxonomy

规则分层、冲突优先级与 promotion gate 见 [`docs/rule-taxonomy.md`](./docs/rule-taxonomy.md)。

一个新观察通常沿这条路径生长：

> taste reaction → articulation → candidate rule → boundary → benchmark → repeated validation → revision

仓库不会把一次个人偏好直接升级为普遍规则。v0.3 的 information-order rule 同时保存了 person-first 的反例，用来防止新领悟重新硬化成模板。

## Benchmarks 与评估

[`benchmarks/cases.md`](./benchmarks/cases.md) 保存 regression cases，同时包含“坏例子”和“合法反例”。合法反例防止 contrast gate、意合、information order 和 inference restraint 逐渐变成机械禁令。

[`evaluation/`](./evaluation/README.md) 把这些判断转成可盲评的诊断数据：34 个 core 案例、固定版本的规则摘录、六维 rubric 和只用 Python 标准库的 harness。它不调用模型，也不给中文打自动分。

```sh
python3 -m evaluation.harness validate
python3 -m unittest discover -s tests -v
```

## 下游 Skill

任务型 Skill 可以复用 Chinese Semantic Flow 的一部分规则。推荐的两种方式、版本标记与 drift review 见 [`docs/downstream-integration.md`](./docs/downstream-integration.md)。不要无标记复制 core。

## 贡献

最有价值的贡献是一个具体的 judgment case：哪句话不对、为什么、更好的版本、边界与合法反例。见 [`CONTRIBUTING.md`](./CONTRIBUTING.md)。

## 仓库结构

```text
SKILL.md                        # core Skill
docs/
  rule-taxonomy.md              # 规则分层、冲突优先级、promotion gate
  native-chinese-regrounding.md # 中文重新着地（candidate core elaboration）
  downstream-integration.md
  writing-extensions.md
benchmarks/
  cases.md
  data/                         # 诊断案例与固定版本来源摘录
evaluation/                     # rubric、数据契约与诊断工具
tests/
README.md / README.en.md
CONTRIBUTING.md / CONTRIBUTING.en.md
CHANGELOG.md / CHANGELOG.en.md
LICENSE
```

## License

MIT
