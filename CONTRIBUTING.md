# Contributing

中文 · [English](./CONTRIBUTING.en.md)

Chinese Semantic Flow 从具体语言失败和具体纠正中生长。

最有价值的贡献单位是一个 **judgment case**，而不是一条新的禁令。

## 提交一个 case

尽量包含：

1. **Context / prompt** — 当时在写什么、讨论什么；
2. **Original output** — 哪一句让人觉得不对；
3. **Why it fails** — 精确描述语义、证据、互动或 scope 问题；
4. **Better version** — 一个或多个更好的版本；
5. **Candidate judgment function** — 生成前哪个判断需要改变；
6. **Boundary conditions** — 原来的表达什么时候其实成立；
7. **Scope** — core semantic、Chinese expression、interaction、scenario 或 house style；
8. **Benchmark value** — 是否值得做 regression case。

推荐路径：

> taste reaction → articulation → candidate rule → boundary → benchmark → repeated validation → revision

## 贡献原则

- 不把“不喜欢这个词”直接变成普遍禁令；
- 优先写 conditional gate，而不是词表 blacklist；
- 保留证据边界，不为了例子鲜活而补事实；
- 区分个人声音偏好与可迁移的中文生成失败；
- 保留作者立场、不确定性与 agency；
- 容易误伤合法表达的规则必须提供反例；
- 规则可以升级，也可以降级或迁移到 extension。

## 修改 core 时

Core 变化需要回答：

1. 哪个可复现 failure 促成了修改？
2. 它是否跨作者/跨场景成立？
3. 新规则会误伤什么？
4. 是否新增或更新 benchmark？
5. 哪些下游 vendored profile 需要 drift review？

## 修改 extension 时

说明它属于哪个作者、persona 或场景。Extension 可以很有个性，不需要假装通用。

## Versioning

- Patch：例子、benchmark、边界澄清、窄修复；
- Minor：兼容总体 philosophy 的规则模块新增或重构；
- Major：底层生成 philosophy 或 rule architecture 改变。
