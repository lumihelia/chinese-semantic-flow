# Writing an extension

中文 · 本仓库只发布 core。作者文风、persona 或特定场景的规则写成 extension，由使用者自己维护。

## 什么时候写 extension

一条规则只对某位作者、某个品牌、某个对话 persona 或某类场景成立时，写进 extension，不放进 core（见 [`rule-taxonomy.md`](./rule-taxonomy.md) 的 Layer D / E）。例如：

- 性别未知时的代词约定；
- 某位作者的长文运动方式，比如从个人经验走向公共判断；
- 某个 persona 的语气、playfulness 与安抚边界；
- 某类产品文案的固定语体。

## 结构

一个 extension 是一份 markdown，建议包含：

1. **适用范围**：属于谁、在什么场景加载，什么时候不加载；
2. **规则**：每条都写判断标准，不写词表禁令；
3. **正例、反例与合法反例**：合法反例说明原来的表达什么时候其实成立；
4. **来源状态**：作者明确确认、一次观察，还是 Agent 推断；推断保持 candidate；
5. **与 core 的关系**：改变了 core 的哪条默认，哪些 core 规则仍然优先（证据边界、用户当前指令始终优先）。

## 加载

宿主同时加载 core 与当前任务明确需要的 extension。多个 extension 同时适用、互相冲突时，按 `rule-taxonomy.md` 的冲突优先级裁决。

## 隐私

extension 常常引用作者的真实文字与校准记录。公开发布前，确认引用的原稿、对话与校准记录都已获得作者同意；否则只发布规则本身，把证据留在私有位置。
