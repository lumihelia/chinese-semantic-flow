# 下游集成

中文 · [English](./downstream-integration.en.md)

任务型 Skill 常常只需要 Chinese Semantic Flow 的一部分规则。推荐两种接法。

## 方式 A：运行时组合

宿主同时加载：

1. `chinese-semantic-flow` core；
2. 任务 Skill；
3. 当前任务明确需要的 extensions。

好处：core 一更新，下游直接用上新规则。

代价：宿主要能同时加载多个 Skill，下游的行为也会跟着上游变。

## 方式 B：内嵌规则子集（vendored profile）

下游 Skill 在自己的 references 里保存一份任务需要的规则子集。

适合要独立分发、宿主不能同时加载多个 Skill，或者需要固定行为的任务包。

内嵌子集至少记录：

```yaml
upstream: chinese-semantic-flow@0.4.1
scope:
  - core-proposition
  - forward-progression
  - chinese-parataxis
  - chinese-native-information-order
  - evidence-bound-specificity
local-additions:
  - transcript-fidelity
  - publishable-essay-structure
```

同时说明：

- 哪些规则来自上游；
- 哪些是任务自己的规则；
- 上游更新后，什么时候需要做漂移检查；
- 哪些个人 extension 没有带进来。

## 不推荐：复制了不做标记

复制几段规则以后各改各的，会出现三类问题：

- 同一个概念在不同仓库里慢慢有了不同的定义；
- 上游修好了一个边界问题，下游还在重复旧的错误；
- 个人偏好在复制过程中被误当成通用规则。

## 什么时候做漂移检查

出现以下变化时，检查下游：

- 核心命题或对照检查的含义变了；
- 事实、推断与立场保持的边界变了；
- 中文原生句法与信息顺序的定义或反例变了；
- 翻译腔的检查从词汇层扩展到了句法层或篇章层；
- 规则从 core 移到 extension，或者反过来；
- benchmark 新增了成立的反例，足以改变旧的做法；
- 下游一直在自己修补同一类中文问题。

## 公开与私有

extension 与校准记录常常包含作者的真实文字。下游要公开分发时，只内嵌任务真正需要的通用规则；个人 extension 和它引用的原稿、对话留在私有的地方，不因为上游公开就跟着公开。

示例优先用不带个人信息的案例，或者已经明确可以公开的案例。
