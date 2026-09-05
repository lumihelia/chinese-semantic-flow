# Changelog

中文 · [English](./CHANGELOG.en.md)

## v0.2.0 — 2026-09-05

第一次规则架构整理。

### Changed

- 把“先确定真实命题 B”明确成生成前的默认起点，并补充“不要先生成 A 再删除”的实现原则；
- 将 core 收敛到 semantic / Chinese expression / interaction / editing 四类可迁移判断；
- 把 Helia 长文、系统视角、动态自我理解与 possibility → reality 从 core 移回 extension；
- 新增 `extensions/helia-language.md`，承载 `TA`、代词经济和直接称呼等 house-style 规则；
- 将 Merva 的 soothing policy、playfulness、舞台动作等 persona 规则完全留在 `extensions/merva-dialogue.md`；
- benchmark 新增合法 contrast、B-first generation、立场/不确定性保真与 pronoun economy 等边界案例；
- 增加 downstream integration 协议，区分 runtime composition 与 vendored profile；
- 标记 `video-to-chinese-essay` 为需要对齐的早期下游；
- `SKILL.md` frontmatter 对齐 portable Agent Skills 字段，并加入 MIT license metadata；
- 公开说明文档补齐中英双语版本。

## v0.1.0 — 2026-09-04

第一版公开规则系统。

### Added

- semantic-first generation 与 core-proposition rule；
- forward semantic progression；
- contrast-first gate；
- Chinese parataxis；
- evidence-bound specificity；
- retractable inference 与 emotion/motive restraint；
- agency-preserving dialogue；
- dynamic conversational density；
- contextual playfulness；
- personal essay movement；
- dynamic self-modeling 与 system-level analysis；
- authorial stance / voice preservation；
- unknown gender → `TA`；
- benchmark-driven iteration；
- Helia writing 与 Merva dialogue extensions；
- rule taxonomy 与 contribution workflow。
