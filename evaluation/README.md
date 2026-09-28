# 可重跑的诊断评估

这个目录把仓库的语言判断变成可以审查的实验材料。它不调用模型，不靠词表或正则表达式判断中文好坏，也不把仓库原来的 Better 当作人工认定的标准答案。

当前入口：

- [数据格式](FORMAT.md)：案例、来源、盲评数据包、判断结果和统计口径的定义（英文）；
- [评分细则](RUBRIC.md)：证据、关系、立场、任务、适用范围、篇章六个维度；
- [错误分类与覆盖缺口](FAILURE-TAXONOMY.md)；
- [语义审查 v2](SEMANTIC-REVIEWS.md)：分开报告语义风险、风格变化和作者接受度；
- [34 个诊断案例](../benchmarks/data/cases.jsonl)、[固定版本来源摘录](../benchmarks/data/sources.json)。

公开数据集只包含 core 案例。依赖个人 extension 的案例、作者校准记录和历史运行记录属于私有研究材料，不在本仓库。

需要 Python 3.10 以上，以及包含来源提交的 Git 仓库副本，不依赖第三方 Python 包。直接下载的 ZIP 没有 Git 历史，无法核对固定的来源，程序会明确报错；不能跳过来源检查，再声称验证通过。

## 运行

在仓库根目录运行：

```sh
python3 -m evaluation.harness validate
python3 -m unittest discover -s tests -v
python3 -m evaluation.harness packet --seed 17 --out /tmp/csf-new-run
```

`validate` 只检查结构和来源是否完整。`packet` 生成给评审看的 `packet.json`，以及不给评审看的对应表 `manifest.json`；同名文件已经存在时，拒绝覆盖。

评审（人或独立的 Agent）只读 `packet.json`，按里面的评分细则，每题在 `judgments.jsonl` 里写一行。不要让评审看到数据集、对应表、原案例标签或暂定答案。同一题的两种顺序如果在同一段对话里评，评审仍可能认出来、记住，不能算两次独立盲测。更严格的做法，是把两种顺序分到彼此隔离的会话里，并另外记下分配情况。

```sh
python3 -m evaluation.harness report \
  --run /tmp/csf-new-run \
  --judgments /tmp/csf-new-run/judgments.jsonl \
  --out /tmp/csf-new-run/report.json
```

漏题、重复题、引错原文、输入过期、对应表被改动，或者判断不符合格式，都会报错；不能把部分结果当作完整的一轮。引文检查只证明引文确实存在，证明不了评语是对的。全部弃权不算成功；同一题换了顺序结论不同，不会被算成平局。有暂定答案的题的一致率、未决题的弃权率和覆盖率，分开报告；所有答案都还只是暂定的解释。

## 新增案例与修订

先固定来源和任务证据，再写假设与边界。没有真实语料时，标成 synthetic（合成）或 adaptation（改编），不伪造作者的认可。需要真实来源或作者偏好才能判断的题，标为 unresolved；`contract` 只表示根据明确的请求和仓库规范暂时推出的答案，不代表有人确认过。同一题族里改了什么、保留了什么，都要写进 `provenance.changes`。

修改答案之前，先保存原来的运行记录、数据和判断，写明是哪条证据要求修改。不要为了提高一致率去改答案，也不要把重算当成新的评估。同一份源材料和它的变体，放在同一个切分里；目前全部是开发用的诊断题，还没有留出来的测试题。

## English reading note

This is a local, standard-library diagnostic harness, not an automatic language scorer. The dataset and rubric are primarily Chinese because the judged text is Chinese; [FORMAT.md](FORMAT.md) defines the machine contract in English. Sources are pinned repository excerpts. Keys are provisional, synthetic contexts remain identified, and hypothesis/abstention results are separated from contract agreement. The bilingual repository entrypoints link to the same canonical artifacts to avoid duplicate datasets drifting apart.
