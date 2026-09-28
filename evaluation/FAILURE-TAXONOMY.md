# Failure taxonomy — provisional v1

本表是本轮从仓库规范提出的错误整理方式，供标注与覆盖检查使用。标签不表示九种互斥疾病，也不提供加权总分。一个具体语义损害可以关联多项规则；报告实例时先写最小损害，再加标签，避免重复计罚。

| Tag | 判定所需证据 | 主要维度 / 仓库来源 | 必须存活的负控 |
| --- | --- | --- | --- |
| unsupported_contrast | 被回应的 A 无给定或许可使用的来源 | grounding, relation；SKILL §§0/1/16 | 有明示 A 的纠正；单纯否定事实 |
| unsupported_detail | 候选新增一个无法溯源的事实、观察者、机制或事件 | grounding；§§5/6/7 | 已给具体资料；请求的虚构；明确可撤回且与资料相称的候选 |
| relation_drift | 可指认的因果、条件、并列、包含、先后或范围关系变化 | relation；§3 | 必要连接词；有证据的三项并列；真实张力 |
| stance_drift | 作者的确定程度、认识时间、经验范围、归属或立场改变 | stance；§§13/14 | 保留强判断；原有犹豫；原样 KEEP |
| interaction_overreach | 当前请求和材料不足以支持所补情绪、动机、分析或选择 | grounding, task_fit；§§7–11 | 明确情绪；明确分析或建议请求 |
| task_mismatch | 候选缺少本轮必要信息/动作，或违背具体要求 | task_fit；§§11/18/20–22 | 简短完成；要求的总结、术语、列表或较长分析 |
| scope_leak | 用了未加载的作者/persona 约定，或让 extension 覆盖保真 | scope；Part VII、taxonomy A–E | core-only 多种合法表达；已加载 profile 的局部规范 |
| template_overcorrection | 仅为避某种词形/模板删掉合法信息或功能 | 对应实际损害维度；§§4/4.1/15–19 | 合法被动、所有格、第二人称、术语、总结、否定、对象前置 |
| unresolved_naturalness | 只有语感差异，缺能分辨语域/上下文/作者偏好的证据 | discourse；§4.1、promotion gate | abstain；保真任务下两个足够好的版本可 tie |

`template_overcorrection` 是机制假设标签，不能仅凭输出断定生成者实际用了某条禁令。`unresolved_naturalness` 是知识状态，不能累计为候选失败。自动程序只检查标签合法与覆盖，不判断语义。

## 尚缺 coverage

现有数据覆盖单句改写、短对话、条件/因果/时间/并列/冲突/包含、有限 profile 切换与历史参考复核。尚未覆盖：

- 长篇话题链、段落重排与多轮关系连续；
- 同题跨作者、地区、语域及真实读者任务；
- 不同来源强度、来源相互冲突、引语归属、编辑授权逐步变化；
- 多 extension 同时加载和当地任务规则冲突；
- 作者文风 extension 的长文运动 taste、persona 安抚行为的明确请求边界；
- 真实 prompt 下有/无 core 的生成对照与成本、模型版本；
- 对信息顺序变量做语义控制后的盲选及复测；
- 独立人类标注、一致性分析、争议裁决和真正 held-out 题。

下一轮新增案例时按 family 和源材料整体切分。不要把本轮 development cases 的轻微改写当作未见过的测试集，也不要因合成覆盖表完整而声称获得自然分布覆盖。
