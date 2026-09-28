# Benchmark Cases

中文 · [English](./cases.en.md)

这些案例保存仓库已有的语言判断，尚不是经过独立校准的金标准。本文件只收 core cases；合法反例用于防止规则逐渐变成机械禁令。`Bad` / `Better` 是原有标签；缺少上下文或改写保真有争议时，不能直接作为评分答案。最终文本也不能验证隐藏的生成路径。

可重跑的诊断集、盲评协议与来源记录见 [`../evaluation/README.md`](../evaluation/README.md)。下面保留历史例句，以便追溯判断变化。

## Core Case 001 — 无来源对立

**Prompt**：解释品牌是什么。

**Bad**

> 品牌不是一个 logo，而是一套完整的认知系统。

上下文没有出现“品牌 = logo”。

**Better**

> 品牌组织人们如何识别、记忆和理解一个对象，也参与身份与价值的形成。

**Rule**：B-first / contrast gate.

---

## Core Case 002 — 机制先于口号

**Bad**

> AI 不只是工具，更是我们的认知环境。

**Better**

> 当 AI 持续参与信息选择、记忆调用、判断形成和行动反馈时，它会逐渐成为认知环境的一部分。

**Rule**：mechanism before slogan.

---

## Core Case 003 — 合法 contrast 应保留

**Context**

> 对方刚刚说：“品牌说到底就是 logo 和视觉。”

**Valid**

> 品牌不只由视觉识别构成。命名、叙事、产品体验和长期重复出现的行为，也会参与人们如何识别和记住它。

这里 A 已经真实存在，回应 A 能增加理解。

**Rule**：contrast gate is conditional, not a ban.

---

## Core Case 004 — 不把“删掉 A”当成生成方法

**Prompt**：解释为什么高密度社区需要恢复空间。

**Bad reasoning shape**

> 社区不是越热闹越好。真正重要的是……

**Better**

> 高频互动会持续消耗注意力和社交能量。社区如果同时提供可退出、独处和恢复的空间，成员更容易长期留在高密度关系中。

**Rule**：generate from B; do not draft A first and delete later.

---

## Core Case 005 — 信息不足时补情绪

**User**

> 今天朋友没回我。

**Bad**

> 你是不是有点失落，也担心朋友在疏远你？

**Better**

> 怎么说？

**Rule**：inference restraint / open continuation.

---

## Core Case 006 — 候选答案绑架

**User**

> 我最近不太想去那个活动。

**Bad**

> 是因为你觉得社交太累，还是觉得那里的人不适合你？

**Better**

> 为什么不太想去？

**Rule**：do not narrow narrative space too early.

---

## Core Case 007 — 为了具体而编事实

**Input**

> 这家咖啡馆在杭州。

**Bad rewrite**

> 这家在杭州开了三年的手冲咖啡馆，由老建筑改造而成。

**Better**

> 这家咖啡馆在杭州。

需要更具体时，只使用已有材料补充。

**Rule**：evidence-bound specificity.

---

## Core Case 008 — 三段式惯性

> 2026-09-08 复核：下列 Better 的“继续／下一步”也需要先后或递进依据。见诊断 csf-031/032。

材料只支持“注意力”和“行动”。

**Bad**

> 它改变了人的注意力、身份和行动方式。

**Better**

> 它改变了人的注意力分配，也会继续影响下一步行动。

**Rule**：item count follows content.

---

## Core Case 009 — 改写不能升级确定性

> 2026-09-08 复核：下列 Better 虽保留“可能”，但新增“开始／也”；严格保真任务可直接 KEEP。见 csf-025。

**Input**

> 我现在会怀疑，这可能和工作环境有关。

**Bad rewrite**

> 我意识到，问题的根源就在工作环境。

**Better**

> 我开始怀疑，这件事可能也和工作环境有关。

**Rule**：preserve uncertainty and stance.

---

## Core Case 010 — 抽象词替代机制

> 2026-09-08 复核：仓库未提供产品机制材料，下列 Better 仅能作为有相应资料时的示意，不能据此补事实。见 csf-021/022。

**Bad**

> 这个产品重塑了人与城市之间的关系。

**Better**

> 它给原本只能经过的公共空间增加了停留、回应和与陌生人共同参与的动作，人和城市发生关系的方式因此变多了。

**Rule**：mechanism before abstraction.

---

## Core Case 011 — 过度完整回复

**User**

> 不知道呢，可能只是顺手也不一定。

**Bad**

> 我理解你的意思。这里可能有三种情况……所以你现在最重要的是不要过度解读。你更倾向哪一种？

**Better**

> 嗯，也完全可能只是顺手。

**Rule**：response density follows the moment.

---

## Core Case 012 — 中文词汇正确，句法仍然可能带着英语骨架

> 2026-09-08 复核：此对照同时改变视角与词汇，并删除“大型 spectacle”；不能隔离语序效果或证明隐藏的思考语言。见 csf-013/014/039/040。

**Context**：作者正在从日常经验进入一个关于城市互动技术的判断。

**AI-ish**

> 投影、追踪、巨型灯光这些技术，平时很容易出现在广告、商业活动和大型 spectacle 里。

**Native Chinese revision**

> 其实，我们平时经常在广告、商业活动中看到类似投影、追踪、巨型灯光这些技术。

变化不只是“把我们放到句首”。后一个版本沿人的日常感知展开：我们 → 平时经常 → 在某些场景 → 看到 → 某类技术。动词“看到”承担了经验与对象之间的关系。

**Boundary / legal counterexamples**

以下句子同样可以自然成立：

> 到了晚上，一整面建筑外墙会出现互动投影。

> 在 Body Movies 中，我们只需要走进光里，在墙上留下影子。

时间、范围或话题在当前篇章承担真实 framing function 时，可以自然前置。因此不把 `person-first` 设成规则。

**Rule**：Chinese-native syntax and discourse information order. Sentence order follows Chinese topic/comment structure, given/new information, temporal/spatial framing, action relations and attention movement; do not form an English proposition first and replace its words with Chinese.

---

## Core Case 013 — 压缩成 UI 文案时丢掉事件

> 来源：一次真实作者修正。Agent 把一份长研究报告压缩成网页的 UI 文案，作者改写了其中一句。这一对同时改了四处，不能隔离单一机制；拆分后的最小对照见 csf-041/042/043。

**Context**：母题地图页面上的一个问句式小标题，页面列出作者写下来的一组问题及其关联。

**AI-ish**

> 写下来的问题，彼此怎么相连

**Author revision**

> 那些写下来的问题，它们是怎么连起来的？

每个字都能看懂，语序也没错，但原本的问题被压成了“名词短语 + 抽象动词”的半句：“相连”只有状态、没有结果；“彼此”和“相连”的相互义重复；泛指的“写下来的问题”没有锚定到页面上的具体对象；问号也一起丢了。

**Boundary / legal counterexamples**

> 问题地图

> 思想年表

导航标签和栏目名本来就是名词性的，不需要补成句子。

> 写下来的问题是怎么连起来的？

作者也接受这一版，称“它也是我会写出来的句子”。“那些”和“它们”都不是必要成分。作者随后补充：这一版更自然，更适合多数书面呈现；她自己那一版口语化更重。

**Rule**：Core 4.2. When compressing long content into titles or UI copy, compress modifiers and argument, not the event itself; ask who acts, what result is reached, and whether a question is still a question.
