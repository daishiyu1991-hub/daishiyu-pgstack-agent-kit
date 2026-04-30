# Template OS 运行协议

## 总原则

每一章都是一个小循环，不是一次性大报告。先执行计划，再证据，再分析，再渲染，再人类选择。

## 章节生命周期

```text
locked
-> planned
-> evidence_ready
-> analysis_draft
-> reviewed
-> awaiting_human_decision
-> unlocked_next / paused / evidence_requested
```

## 1. Template Router

要做：

- 识别当前章节编号和章节名。
- 读取模板允许的子模块。
- 写清楚哪些内容只能作为后续输入，不能在本章展开。

禁止：

- 第 2 章写竞品品牌策略。
- 第 3 章写用户需求结论。
- 第 4 章写产品规划。
- 第 5 章写供应链成本。
- 第 6 章写最终 SKU 和 listing。

## 2. Chapter Preamble

检查：

- 当前 run 的索引页是否锁定。
- 前一章是否有明确人类选择。
- 是否已有本章旧页面，旧页面中哪些结构值得继承。
- 本章可用数据、缺失数据、权限阻塞、人工输入项。

## 3. Evidence Contract

每个字段必须列出：

```text
field
required_input
route
status
source_ref
not_collectable_reason
```

状态只能是：

- `collected_and_used`
- `collected_not_expanded`
- `missing_to_collect`
- `manual_required`
- `not_collectable_now`

## 4. Evidence Acquisition Router

先执行能执行的证据采集：

- MCP/API：批量市场、关键词、ASIN、评论、销量、价格。
- Browser：Amazon 前台、A+、视频、五点、coupon、官网、渠道页。
- File：Excel、CSV、docx、PDF、用户上传资料。
- Manual：BOM、供应商报价、MOQ、模具费、内部工艺边界。
- Web：行业报告、官方页面、公开渠道。

如果工具不可用，写 `not_available_in_current_session`，不要伪造已采集。

## 5. Processing Framework

每个模板节点都按：

```text
Input -> Processing -> Output
```

结论必须能追溯到输入或明确标为推断。

## 6. 補證 Review

在结论前问：

- 模板要求的关键输入有没有缺？
- 缺失是否会改变结论？
- 是否有可自动补的证据还没补？
- 是否有只能人工补的证据？
- 当前报告是完整报告、低置信假设，还是执行计划？

## 7. Red-team Argue

反方必须在结论前出现。默认四个立场：

- 数据怀疑者：证据是否足以支撑？
- 消费者怀疑者：用户第一眼是否会理解并购买？
- 竞争怀疑者：对手是否能快速复制？
- 公司适配怀疑者：是否适合公司的能力、白帽打法和成本结构？

最后输出“幸存结论”，不是直接 Go。

## 8. Complete HTML Report

完整报告包含：

- 结论先行。
- 核心图表或对比表。
- 模板节点 Input -> Processing -> Output。
- 证据充分性审查。
- red-team 争论。
- 人类判断选项。
- 来源在底部。

## 9. Human Decision Stop

必须停下，不能自动进入下一章。选择要写进：

```text
process/section{n}-human-decision-*.json
```

如果选择暂停：

- 保留执行计划和已有报告。
- 不解锁下一章。
- 写清 resume 条件。

## 10. Artifact & Memory

本地 run folder 是原始资料和 HTML 展示面。GBrain 只写稳定、压缩、可复用的结论。

不要写入：

- 原始供应商机密。
- 授权 token。
- 每个页面草稿。
- 未验证的临时猜测。
