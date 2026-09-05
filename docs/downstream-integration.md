# Downstream Integration

中文 · [English](./downstream-integration.en.md)

任务型 Skill 经常只需要 Chinese Semantic Flow 的一部分。下游集成有两种推荐方式。

## 方式 A：运行时组合

宿主同时加载：

1. `chinese-semantic-flow` core；
2. 任务 Skill；
3. 当前任务明确需要的 extensions。

优点：core 更新后可以直接获得新规则。

代价：宿主需要支持多 Skill 组合，而且下游行为会随 upstream 更新变化。

## 方式 B：Vendored profile

下游 Skill 在自己的 references 中保存一个任务范围内的规则子集。

适合希望独立分发、没有多 Skill 组合能力，或需要冻结行为的任务包。

Vendored profile 至少记录：

```yaml
upstream: chinese-semantic-flow@0.2.0
scope:
  - core-proposition
  - forward-progression
  - chinese-parataxis
  - evidence-bound-specificity
local-additions:
  - transcript-fidelity
  - publishable-essay-structure
```

同时说明：

- 哪些规则来自 upstream；
- 哪些是任务自己的局部规则；
- upstream 更新后什么时候需要 drift review；
- 哪些个人 extensions 没有被带入。

## 不推荐：无标记复制

复制几段规则后各自继续修改，会出现三类问题：

- 同一个概念在不同仓库逐渐拥有不同定义；
- 修复了 upstream 的边界问题，下游仍继续复现旧行为；
- 个人 taste 可能在复制过程中被误当成通用规则。

## Drift review 触发条件

出现以下变化时检查下游：

- core proposition / contrast gate 的含义变化；
- fact / inference / stance preservation 边界变化；
- 规则从 core 移到 extension，或反向移动；
- benchmark 新增了能改变旧实现的合法反例；
- 下游长期自行修补同一类中文问题。

## 当前已知下游

### `lumihelia/video-to-chinese-essay`

它的 `style-diagnostics.md` 比 Chinese Semantic Flow 更早形成，已经包含中文意合、连接词检查和 contrast-first 判断的早期版本。

方向一致，但当前缺少：

- B-first 作为生成起点的明确表达；
- core / task-specific rule 分层；
- upstream version marker；
- 合法 contrast 反例；
- drift review 约定。

因此在 `chinese-semantic-flow@0.2.0` 合并后，应回到该仓库做一次对齐。推荐保留它的独立任务 Skill 形态，同时把本地 style diagnostics 改成明确的 vendored profile，而不是让它产生运行时硬依赖。
