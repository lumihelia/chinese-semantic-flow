# 可重跑的诊断评估

此目录把仓库的语言判断转成可审查的实验材料。它不自动调用模型，不使用词表/正则判中文好坏，也不把仓库原来的 Better 当作人类金标。

当前入口：

- [数据契约](FORMAT.md)：case、provenance、packet、judgment 和统计定义；
- [六维 rubric](RUBRIC.md)：语义证据、关系、立场、任务、作用域和篇章；
- [failure taxonomy 与覆盖缺口](FAILURE-TAXONOMY.md)；
- [语义审查 v2](SEMANTIC-REVIEWS.md)：分开报告语义风险、风格变化和作者接受度；
- [34 个诊断案例](../benchmarks/data/cases.jsonl)、[固定版本来源摘录](../benchmarks/data/sources.json)。

公开数据集只包含 core 案例。依赖个人 extension 的案例、作者校准记录与历史 run 属于私有研究材料，不在本仓库。

需要 Python 3.10+ 和包含来源 commit 的 Git checkout，无第三方 Python 依赖。下载没有 Git 历史的 ZIP 不能验证固定来源，程序会明确报错；不可跳过来源检查后声称验证通过。

## 运行

在 repository 根目录：

```sh
python3 -m evaluation.harness validate
python3 -m unittest discover -s tests -v
python3 -m evaluation.harness packet --seed 17 --out /tmp/csf-new-run
```

`validate` 只验证结构和来源完整性。`packet` 写出盲评输入 `packet.json` 和私有映射 `manifest.json`；已有同名文件时拒绝覆盖。

让人类或独立 evaluator 只读取 packet，按其中 rubric 为每题写一行 `judgments.jsonl`。不要给 evaluator 看 dataset、manifest、原案例标签或暂定答案。两个换位题如在同一上下文中评估，仍可能被识别并记住，不能称为独立的两次盲测。更强实验应把两种顺序分配到隔离会话，并另存分配记录。

```sh
python3 -m evaluation.harness report \
  --run /tmp/csf-new-run \
  --judgments /tmp/csf-new-run/judgments.jsonl \
  --out /tmp/csf-new-run/report.json
```

漏题、重复题、错引用、输入过期、映射篡改或不合契约的判断会报错，不能把部分结果当完整运行。原文引用检查只证明引用存在，无法验证评语正确。全弃权不算成功，换位不一致不变成平局。合同题一致率与未决题弃权、覆盖率分别报告；所有键仍是暂定解释。

## 新增案例与修订

先固定来源和任务证据，再写假设与边界。真实语料缺失时标 synthetic / adaptation，不伪造作者批准。需要真实来源或 taste 的问题留 unresolved；`contract` 表示从明示请求与仓库规范暂定推导，不表示人类确认。家族内只改什么、保持什么必须写在 `provenance.changes`。

改键之前保存原 run、原数据和原判断，写明是哪项证据要求修订。不要为了提高 agreement 改键，也不要把重算当作新评估。把同一源材料及其变体放在同一 split；当前全是 development diagnostics，没有 held-out test。

## English reading note

This is a local, standard-library diagnostic harness, not an automatic language scorer. The dataset and rubric are primarily Chinese because the judged text is Chinese; [FORMAT.md](FORMAT.md) defines the machine contract in English. Sources are pinned repository excerpts. Keys are provisional, synthetic contexts remain identified, and hypothesis/abstention results are separated from contract agreement. The bilingual repository entrypoints link to the same canonical artifacts to avoid duplicate datasets drifting apart.
