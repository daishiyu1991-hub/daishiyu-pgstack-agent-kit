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

## 0. Single Source Of Truth

这套 OS 只能有一个可更新源头：

```text
GitHub source:
https://github.com/daishiyu1991-hub/daishiyu-pgstack-agent-kit

skill:
product-strategy-template-os
```

同事安装、更新、复现案例时，都必须从这个源头安装。不要从旧 zip、旧本地 `skill-packages/`、聊天记录里的半成品 HTML、或某次 run folder 直接复制成 skill。

如果机器上存在多个同名 skill，agent 必须先报告实际读取的 `SKILL_HOME`，并以通过 `bootstrap_check.py` 和 `validate_run.py` 的那一份为准。旧 7 章版本必须视为无效版本。

## 1. Install

在同事机器上运行：

```bash
npx skills add https://github.com/daishiyu1991-hub/daishiyu-pgstack-agent-kit --skill product-strategy-template-os --yes --global
```

## 1.1 Update

同事后续只需要对 agent 说：

```text
/update product-os
```

agent 必须把它理解成“从 GitHub 重新安装并验证 Product Strategy Template OS”，然后运行：

```bash
SKILL_HOME="${AGENTS_HOME:-$HOME/.agents}/skills/product-strategy-template-os"
python3 "$SKILL_HOME/scripts/update_product_os.py"
```

如果 skill 是通过 `npx skills add --global` 安装，默认位置通常是：

```bash
SKILL_HOME="${AGENTS_HOME:-$HOME/.agents}/skills/product-strategy-template-os"
```

如果本地安装的是旧版本，还没有 `update_product_os.py`，使用 fallback：

```bash
npx skills add https://github.com/daishiyu1991-hub/daishiyu-pgstack-agent-kit --skill product-strategy-template-os --yes --global
SKILL_HOME="${AGENTS_HOME:-$HOME/.agents}/skills/product-strategy-template-os"
python3 "$SKILL_HOME/scripts/bootstrap_check.py" --skill-root "$SKILL_HOME"
```

预期更新验收：

```text
OK_UPDATE_PRODUCT_OS
OK_BOOTSTRAP
```

安装后，skill 通常位于：

```bash
${AGENTS_HOME:-$HOME/.agents}/skills/product-strategy-template-os
```

如果 agent 不确定安装位置，先搜索：

```bash
find "${CODEX_HOME:-$HOME/.codex}/skills" -maxdepth 2 -name SKILL.md -path '*product-strategy-template-os*'
find "${AGENTS_HOME:-$HOME/.agents}/skills" -maxdepth 2 -name SKILL.md -path '*product-strategy-template-os*'
```

## 2. Bootstrap Check

安装后必须先跑验收，不要直接开始分析：

```bash
SKILL_HOME="${AGENTS_HOME:-$HOME/.agents}/skills/product-strategy-template-os"
python3 "$SKILL_HOME/scripts/bootstrap_check.py" --skill-root "$SKILL_HOME"
```

预期输出：

```text
OK_BOOTSTRAP
```

如果没有 `OK_BOOTSTRAP`，先修安装，不要继续跑 research。

## 2.1 Run Validation Gate

任何 run 要交给同事、放进索引主报告、或作为案例沉淀前，必须跑：

```bash
python3 "$SKILL_HOME/scripts/validate_run.py" "$RUN_DIR"
```

只有看到下面结果，才算通过：

```text
OK_VALIDATE_RUN
```

这个校验会拦住最常见的跑偏：

- 旧 7 章顺序：`6. 供应链管理 / 7. 产品规划`；
- 顶层状态和章节状态不一致；
- 锁定章节已经生成页面；
- 评论数量、提及次数等数字没有 raw/tag/effective review ledger；
- 产品规划 / USP 页面没有区分 `评论提及频次` 与 `USP 战略权重`。

如果校验失败，该页面只能算过程稿，不能当主报告。

## 2.2 Strict Mode: How To Run 100% By The Skill

不能靠“让 agent 自觉按模板写”来保证一致性。必须把 skill 当成可执行协议来跑：读取同一套文件、用同一套脚本初始化、用同一套 validator 拦截不合格输出。

严格模式流程：

```text
1. Resolve Skill
   找到唯一 SKILL_HOME，并回报路径。

2. Bootstrap
   python3 "$SKILL_HOME/scripts/bootstrap_check.py" --skill-root "$SKILL_HOME"
   必须得到 OK_BOOTSTRAP。

3. Read Contract
   按 README 第 4 节读取 SKILL.md 与 references/*.md。

4. Init Or Resume Run
   新 run 必须用 scripts/init_run.py 创建。
   旧 run 必须先读取 process/pipeline-run-state-v1.json。

5. Chapter Loop
   每章都必须跑：
   Template Router -> Preamble -> Evidence Contract -> Evidence Acquisition
   -> Input/Processing/Output -> Evidence Review -> Red-team
   -> Complete HTML Report -> Human Decision Stop -> Decision Record。

6. Raw Evidence Ledger
   任何 review 数字、关键词数字、趋势数字，都必须有 process/ 下的可复算 ledger。
   没有 ledger，就只能写 not_collected / not_recomputable / inference。

7. Validate Before Accept
   python3 "$SKILL_HOME/scripts/validate_run.py" "$RUN_DIR"
   不通过就修，不允许把失败页面放进主索引当成结论。

8. Sync Boundary
   章节结束运行 gbrain_auto_sync.py；未验证成功不能声称已同步。
```

这个流程能保证“被接受的产出”100%遵守 skill。它不能保证每个中间草稿都完美，但任何不合规草稿都会被 validator 拦下来，不能进入主报告和案例包。

如果同事跑出的结果不同，优先检查四件事：

- 读到的是否是同一个 `SKILL_HOME`；
- 是否还是旧 7 章顺序；
- 是否缺 raw/tag/effective evidence ledger；
- 是否把 `评论提及频次` 当成了 `USP 战略权重`。

## 3. Start A New Run

新建一个品类研究 run：

```bash
SKILL_HOME="${AGENTS_HOME:-$HOME/.agents}/skills/product-strategy-template-os"
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
references/explosive-usp-framework.md
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

默认模板有八章：

```text
1. 品类本质小结
2. 市场竞争分析
3. 头部品牌竞争&竞品分析
4. 用户场景&需求分析
5. 营销分析&社媒传播
6. 产品规划
7. 供应链实现
8. 项目计划
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

## 5.1 Chapter 6 Explosive USP Rule

第 6 章产品规划必须先运行 `references/explosive-usp-framework.md`。

不能只按“最稳妥、最容易落地、最符合现有能力”的评分选主赛道。若用户认为主赛道太平凡，agent 必须重新生成爆发力 USP，而不是在原结论上润色。

默认推导：

```text
评论证据 / 竞品购买理由
-> 用户真实任务
-> 一眼有画面的场景事件
-> 爆发力 USP 候选
-> 可控能力成长边界
-> Red-team argue
-> 技术拓扑：用户任务效果 -> 功能条件 -> 关键元器件
-> Human Decision Stop
```

能力边界默认三层：

```text
核心能力：必须利用
相邻能力：可以为了强 USP 有控制地成长
难能力：暂时不跳进去
```

示例：wake up light 的稳妥方向是“像灯具一样的日出光效”，但爆发力 USP 应该进一步压缩成“先叫醒房间，再叫醒你 / 一盏把卧室调成早晨的睡醒灯”。

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
