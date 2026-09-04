# Chinese Semantic Flow

**让语言忠实于思考的运动。**

Chinese Semantic Flow 是一个持续迭代的中文生成、改写、编辑与对话 Skill。它把重点放在语义关系、推断边界、对话自然度和人的 agency 上。

它把生成判断本身作为主要对象，重点检查：

- 一句话是否从真正成立的命题出发；
- 后一句是否从前一句自然长出来；
- 因果、递进、并列、包含、时间变化和冲突是否被准确表达；
- AI 是否为了制造力度，凭空搭建一个较弱观点再推翻；
- AI 是否替人补足情绪、动机和结论；
- “活人感”是否来自上下文连续性，而不是语气词、撒娇、舞台动作和模板化表演；
- 编辑是否保留了原作者自己的判断和声音。

## 核心原则

最重要的一条规则：

> 先确定真正成立的核心命题，直接从它开始生成。只有当需要修正的观点已经真实存在，而且处理它会增加信息时，才引入转折或对照。

默认的思考运动是：

> 观察 → 判断 → 机制 → 后果 → 反馈 → 新的理解

它不是固定文章模板，而是一种“继续向前”的生成方向。

## 主要模块

- Semantic-first generation
- Forward semantic progression
- Contrast-first detection
- Chinese parataxis
- Evidence-bound specificity
- Inference restraint
- Agency-preserving dialogue
- Conversational density control
- Cognitive / relational playfulness
- Personal essay movement
- Dynamic self-modeling
- System-level analysis
- Benchmark-driven iteration

## 安装

如果你的 Agent / Coding Agent 支持 Skill 目录，可以把整个仓库放入对应 skills 目录，并加载 `SKILL.md`。

Claude Code 常见用法：

```bash
git clone https://github.com/lumihelia/chinese-semantic-flow.git ~/.claude/skills/chinese-semantic-flow
```

也可以只复制 `SKILL.md` 到你自己的 Agent instruction system 中。

## 使用示例

### 生成

```text
请使用 chinese-semantic-flow 写一段中文，解释为什么 AI 长期记忆会改变人机协作。
```

### 改写

```text
请用 chinese-semantic-flow 改写下面这段话，保留我的观点和语气，不要增加新事实：
[文本]
```

### 对话

```text
请使用 chinese-semantic-flow 的 inference restraint 和 agency-preserving dialogue 规则回应。
```

## 它和 Humanizer 类工具有什么区别？

Humanizer 常从表面语言模式识别 AI 痕迹，再进行清理。

Chinese Semantic Flow 更靠前一步：它试图约束**生成判断本身**。语言是否自然只是结果之一。更重要的是，句子为什么这样开始、关系为什么这样排列、哪些东西可以推断、哪些地方应当停住。

## 设计原则

这个项目刻意区分三类规则：

1. **通用语义规则**：例如从真实成立的命题出发。
2. **中文表达规则**：例如意合推进、减少无必要的显性逻辑连接。
3. **个人 taste / 场景扩展**：例如某种随笔运动、某个对话 AI 的可爱气质。

个人 taste 不自动升级为普遍规则。

## 迭代方式

每次出现“这句话味道不对”，都可以把一次直觉反应提炼为可测试判断：

> taste reaction → articulation → rule → example → benchmark → revision

仓库中的 `benchmarks/cases.md` 用来保存这些案例。

## 当前版本

`v0.1.0`：第一版规则系统。

这是一份会继续生长的 Skill，不追求一次完成。

## 可选扩展

仓库把个人 / persona taste 单独拆开：

- `extensions/helia-writing.md`：第一人称长文、思想形成时间、从我经过世界抵达我们。
- `extensions/merva-dialogue.md`：对话密度、推断边界、agency、cognitive / relational playfulness。

核心 Skill 可以单独使用；需要特定风格时再加载扩展。

## License

MIT License. See `LICENSE`.
