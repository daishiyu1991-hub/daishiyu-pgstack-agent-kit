# Product Strategy Template OS

面向同事 agent 的安装与运行入口。

只要 agent 读到这份 README，就应该能完成三件事：

1. 安装这个 skill。
2. 验证基础文件完整。
3. 按固定 OS 逻辑启动并运行一轮品类战略用研。
4. 在 skill 边界自动处理 GBrain 同步或 Hermes Admin 交接。

这不是一个普通市场分析 prompt。它是一套固定模板 OS：

```text
模板章节识别
-> 证据收集
-> Input / Processing / Output
-> 补证 review
-> red-team argue
-> 完整 HTML 报告
-> 人类判断停点
-> 状态与 GBrain 交接记录
```

## 1. Install

在同事机器上运行：

```bash
npx skills add https://github.com/daishiyu1991-hub/daishiyu-pgstack-agent-kit --skill product-strategy-template-os
```

安装后，skill 通常位于：

```bash
${CODEX_HOME:-$HOME/.codex}/skills/product-strategy-template-os
```

如果 agent 不确定安装位置，先搜索：

```bash
find "${CODEX_HOME:-$HOME/.codex}/skills" -maxdepth 2 -name SKILL.md -path '*product-strategy-template-os*'
```

## 2. Bootstrap Check

安装后必须先跑验收，不要直接开始分析：

```bash
SKILL_HOME="${CODEX_HOME:-$HOME/.codex}/skills/product-strategy-template-os"
python3 "$SKILL_HOME/scripts/bootstrap_check.py" --skill-root "$SKILL_HOME"
```

预期输出：

```text
OK_BOOTSTRAP
```

如果没有 `OK_BOOTSTRAP`，先修安装，不要继续跑 research。

## 3. Start A New Run

新建一个品类研究 run：

```bash
SKILL_HOME="${CODEX_HOME:-$HOME/.codex}/skills/product-strategy-template-os"
RUN_DIR="$PWD/runs/$(date +%F)-wake-up-light品类战略用研"

python3 "$SKILL_HOME/scripts/init_run.py" \
  --category "wake up light" \
  --marketplace US \
  --out "$RUN_DIR"
```

验证 run 骨架：

```bash
python3 "$SKILL_HOME/scripts/validate_run.py" "$RUN_DIR"
```

预期输出：

```text
OK_VALIDATE_RUN
```

也可以一步完成 bootstrap + 初始化：

```bash
SKILL_HOME="${CODEX_HOME:-$HOME/.codex}/skills/product-strategy-template-os"
RUN_DIR="$PWD/runs/$(date +%F)-wake-up-light品类战略用研"

python3 "$SKILL_HOME/scripts/bootstrap_check.py" \
  --skill-root "$SKILL_HOME" \
  --category "wake up light" \
  --marketplace US \
  --init-run "$RUN_DIR"
```

## 4. Files The Agent Must Read

每次启动这个 OS，agent 必须按顺序读取：

```text
README.md
SKILL.md
references/global-rules.md
references/pipeline-architecture.md
references/template-structure.zh.md
references/data-source-router.md
references/red-team-company-baseline.md
references/frontend-report-style.md
```

如果是发布、交接、同步 GBrain，还要读取：

```text
gbrain/HERMES_ADMIN_HANDOFF.md
gbrain/gbrain-handoff-packet-v1.json
gbrain/gbrain-sync-queue.jsonl
gbrain/gbrain-sync-status.json
```

## 5. Operating Logic

每次运行开始，agent 先执行：

```bash
python3 "$SKILL_HOME/scripts/gbrain_auto_sync.py" --skill-root "$SKILL_HOME" --phase start
```

每次运行结束，agent 再执行：

```bash
python3 "$SKILL_HOME/scripts/gbrain_auto_sync.py" --skill-root "$SKILL_HOME" --phase end
```

这一步不需要人类每次提需求。它是原生 GBrain 的 skill-boundary sync 模式：

```text
有 gstack-brain-sync -> 自动注册全局规则记录 -> drain / discover / once
没有 gstack-brain-sync -> 不伪造写入，明确进入 Hermes Admin handoff queue
```

原生 GBrain 可接收的全局规则会被压缩写入：

```text
${GSTACK_HOME:-$HOME/.gstack}/projects/product-strategy-template-os/learnings.jsonl
```

并通过：

```text
gstack-brain-enqueue
gstack-brain-sync --discover-new
gstack-brain-sync --once
```

进入正常的 GBrain 同步链路。

默认模板有七章：

```text
1. 品类本质小结
2. 市场竞争分析
3. 头部品牌竞争&竞品分析
4. 用户场景&需求分析
5. 营销分析&社媒传播
6. 供应链管理
7. 产品规划
```

每一章都必须执行同一个循环：

```text
1. Template Router
   识别当前章节、模板边界、禁止越界内容。

2. Chapter Preamble
   检查已有页面、已有结论、上一章人类判断、索引结构锁。

3. Evidence Contract
   写清楚本章需要哪些真实输入，哪些已经收集，哪些缺失。

4. Evidence Acquisition Router
   能用 MCP/API/浏览器/上传文件收集的，agent 自动收集。
   只有供应链、内部能力、线下报价等 AI 无法验证的信息才问人。

5. Processing Framework
   每个模板节点都写成 Input -> Processing -> Output。

6. 補證 Review
   输出结论前，先检查证据缺口。能补的继续补，不能补的标注原因。

7. Red-team Argue
   至少从数据怀疑者、消费者怀疑者、竞争怀疑者、公司适配怀疑者四个立场反驳结论。

8. Complete HTML Report
   生成一页完整报告。结论在前，过程在后，图表不能丢。

9. Human Decision Stop
   停下来等人类选择。没有明确选择，不得解锁下一章。

10. Artifact & Memory Ledger
   更新 process JSON、索引链接、GBrain 交接队列。
```

## 6. Zero-Hallucination Rules

所有数据必须真实可追溯。

禁止编造：

```text
ASIN
价格
销量
关键词搜索量
趋势增长
review quote
供应商报价
BOM
MOQ
工具/模具费
引用来源
```

缺数据必须写成：

```text
not_collected
manual_required
not_available_in_current_session
unknown
```

推断必须明确标注为推断。增长率必须写清楚比较周期，例如：

```text
latest vs previous period
latest vs same period one year earlier
first available period -> latest period
```

## 7. HTML Report Contract

每一章只有一个主报告，格式是：

```text
结论
关键图表
模板节点分析
证据充分性 review
red-team argue
人类判断框
来源与方法
```

HTML 是给人看和判断的，不是 process log。过程文件放在 `process/`。

## 8. Human Decision Contract

每章结束必须停在人类判断。标准选项：

```text
A. 通过，解锁下一章
B. 需要补证，暂不解锁
C. 暂停，等待人工输入
D. 否决或重做本章
```

人类选择必须写入：

```text
process/section{n}-human-decision-*.json
```

空白选择不能由 AI 补成通过。

## 9. GBrain Handoff

本 skill 不要求每个同事 agent 直接写云端 GBrain，但必须自动处理同步边界。

默认边界：

```text
本地 run folder = 原始过程与 HTML 源文件
gbrain/ queue = 可交给 Hermes Admin 的企业 GBrain 交接包
Hermes Admin / gbrain-remote = 原生企业 GBrain 写入与验证路径
```

写入 GBrain 的只应该是：

```text
章节摘要
人类判断
稳定 pipeline 规则
证据缺口
可复用分析模型
```

不要写入：

```text
原始账号 token
供应商敏感报价明细
未脱敏原始文件
每一个草稿 HTML
```

如果当前 agent 没有 GBrain 写权限，只需要更新：

```text
gbrain/gbrain-sync-queue.jsonl
process/gbrain-sync-queue.jsonl
```

并把任务交给 Hermes Admin。

不要把 GBrain 同步变成人类每次手动提需求。只有以下情况才问人：

```text
缺 credentials
缺权限
需要选择隐私同步级别
需要确认是否发布到 team/shared 层
```

## 10. Acceptance Checklist

同事的 agent 完成安装后，必须回报：

```text
OK_BOOTSTRAP
OK_VALIDATE_RUN
skill path
run path
current chapter
whether GBrain handoff is queued or synced
```

没有这些验收结果，就不能认为安装完成。
