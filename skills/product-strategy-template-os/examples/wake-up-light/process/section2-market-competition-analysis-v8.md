# 第 2 章市场竞争分析 v8：模板节点循环分析包

> 本文件是分析层，不是展示层。HTML 只从这里提炼结论、图表和判断框。
> 本轮目标：按 Word 模板完整重做第 2 章，补上 Evidence Sufficiency Review 与 Red Team Argument，不再把第 3 章竞品拆解提前展开。

## 0. 本轮执行规则

固定循环：

```text
Template Node
-> Question
-> Input Contract
-> Evidence Acquisition
-> Processing
-> Output Draft
-> Evidence Sufficiency Review
-> Red Team Argument
-> Revised Conclusion
-> Review Gates
-> Human Decision Stop
```

数据原则：

- 所有事实必须来自 MCP/API、已固化文件、公开网页或用户输入。
- 没有来源写 `not_collected`。
- 无法比较写 `not_comparable`。
- 推断必须写 `inference`。
- 结论必须经过反方质疑后再输出。

本轮新增证据账本：`process/section2-market-competition-v8-evidence-ledger.json`

## 1. Chapter Preamble

当前章节：`2. 市场竞争分析`

允许范围：

- `2.1 市场大盘`
- `2.2 亚马逊渠道分析`
- `2.3 其他渠道市场机会`
- 本章最终输出：市场阶段、渠道优先级、第 3 章输入对象池

禁止展开：

- 第 3 章：头部品牌基因、品牌矩阵、竞品深拆。
- 第 4 章：用户画像、用户旅程、需求矩阵。
- 第 5 章：社媒传播、KOL、内容策略。
- 第 6 章：供应链、BOM、供应商、开模。
- 第 7 章：产品定义、listing 方案、SKU 规划。

## 1.1 基础行业阶段判断

第 2 章必须先回答“这个行业处于什么阶段”，否则后面的市场结构、竞品和渠道判断会没有锚点。

本轮结论：

| 层级 | 阶段判断 | 依据 | 策略含义 |
|---|---|---|---|
| Sleep Tech 上位市场 | 成长期 | 公开 sleep tech devices 市场报告显示宏观睡眠科技仍有增长预期 | 只能作为上位叙事，不能直接等同于 wake-up-light |
| Alarm Clock / 普通 Wake-up Light 底盘 | 成熟期中后段 | Amazon 相关关键词年度总量下降、竞品数量多、老品评论门槛高、低价供给充足 | 不能当蓝海，不能用低价闹钟打法进入 |
| Sunrise + Sound + Routine 融合分支 | 成熟市场里的再分化窗口 | Odokee / REACHER / BUFFBEE / Hatch 等代表样本证明融合形态仍能起量 | 第 3 章要验证哪种分化机制可复制，尤其是中价光效体验切口 |

最小可存活结论：

> 这个行业不是整体成长期，也不是完全衰退期，而是“成熟底盘里的结构再分化”。机会来自用户从传统闹钟、普通 wake-up-light 和声音机向更高价值感的睡眠唤醒体验迁移。

## 2.1 市场大盘

### 2.1.1 全球主要市场大盘

Template Node：全球主要市场大盘

Question：这个品类是否有足够大的外部需求背景，值得继续做深度研究？

Input Contract：

- 全球市场报告：需要。
- 行业报告：需要。
- 论坛协会数据：未收集。
- 供应链 B 端数据：未收集。
- 海关数据：未收集。

Evidence Acquisition：

- 已收集：公开 sleep tech devices 市场报告。2025 年约 USD 29.30B，2026 年约 USD 34.70B，2035 年约 USD 134.60B，CAGR 约 18.46%。
- 已收集：Hatch Restore 3 在 Hatch 官方、Target、Walmart、Best Buy、Macy's 等渠道的公开零售存在性。
- 未收集：精确 wake-up-light 全球 TAM。
- 未收集：供应链 B 端数据、海关数据。

Processing：

- 将 sleep tech devices 作为相邻宏观代理，而不是 wake up light 精确市场。
- 用 Hatch 跨渠道售价锚判断 premium routine 是否被多个零售渠道承认。
- 不把宏观 sleep tech 增长直接推断成 wake up light 增长。

Output Draft：

- 宏观睡眠科技是增长市场，但 wake up light 不是等于 sleep tech。
- 第 2 章可以把宏观趋势作为背景，不可把它作为品类容量结论。
- 更有效的本章判断应落回 Amazon 站内需求、关键词结构和渠道证据。

Evidence Sufficiency Review：

- 通过项：相邻宏观市场与零售价格锚有证据。
- 不足项：缺精确 wake-up-light TAM、区域 split、渠道 split、B 端和海关数据。
- 对判断影响：不能得出“全球 wake up light 大盘高速增长”，只能得出“睡眠健康/睡眠科技为相邻上位叙事”。

Red Team Argument：

- 反方：如果宏观 sleep tech 增长主要来自穿戴、智能床垫、医疗检测，wake up light 不一定受益。
- 公司能力视角：我们是照明/灯具工艺相关公司，sleep tech 里最适合我们的不是穿戴或医疗监测，而是光效、卧室灯具、睡眠唤醒体验。这个范围与公司能力相邻。

Revised Conclusion：

> 宏观市场只能作为“睡眠健康叙事存在”的支撑，不能作为进入理由。真正要判断的是：Amazon 站内是否存在从传统闹钟向“光 + 声 + 睡眠例程”的结构迁移，以及这个迁移是否落在我们的照明能力边界内。

### 2.1.2 市场发展趋势

Template Node：市场发展趋势

Question：需求是在增长、稳定、下滑，还是周期性波动？

Input Contract：

- Google 趋势数据：未收集，SellerSprite `google_trend` 返回 `ERROR_UNAUTHORIZED`。
- Amazon 站内关键词趋势：已收集，Sorftime 24 个月搜索量序列。
- 关键词：`wake up light`、`sunrise alarm clock`、`sound machine alarm clock`、`alarm clock`。

Evidence Acquisition：

- Sorftime `keyword_trend` 原始数据：2024-04 到 2026-03。
- 年度窗口：上一完整 12 个月 2024-04 -> 2025-03；当前完整 12 个月 2025-04 -> 2026-03。

Processing：

- 年度总量变化 = 当前完整 12 个月搜索量总和 / 上一完整 12 个月搜索量总和 - 1。
- MoM = 本月 / 上月 - 1。
- YoY = 本月 / 去年同月 - 1。

Output Draft：

| 关键词 | 上一完整 12 个月 | 当前完整 12 个月 | 年度总量变化 |
|---|---:|---:|---:|
| wake up light | 103,506 | 78,494 | -24.2% |
| sunrise alarm clock | 2,164,156 | 1,945,375 | -10.1% |
| sound machine alarm clock | 202,838 | 186,186 | -8.2% |
| alarm clock | 7,077,961 | 6,225,123 | -12.0% |

Evidence Sufficiency Review：

- 通过项：Amazon 站内趋势足够支撑“不是整体年度增长”。
- 不足项：Google Trends 未采集，不能判断站外搜索兴趣是否同步下降。
- 对判断影响：本章结论要从“品类增长”改成“成熟底盘里的结构迁移/局部修复”。

Red Team Argument：

- 反方：如果四个词年度都下降，这个市场可能不是机会，而是衰退。
- 正方：`wake up light` 在 2026 Q1 YoY 转正，Odokee 等中价融合 ASIN 有起量，说明并非所有需求都死掉，而是老关键词和老形态承压。
- 公司能力视角：我们不适合去做纯低价成熟闹钟；如果进入，必须证明“光效体验 + 可靠品质 + 中价可感知价值”能抢结构迁移。

Revised Conclusion：

> Amazon 站内需求不支持“整体增长”。机会如果存在，不来自大盘自然上涨，而来自成熟市场中的结构迁移：传统闹钟/普通 wake-up-light 向“sunrise + sound machine + sleep routine”的融合形态分流。

### 2.1.3 市场生命周期

Template Node：市场生命周期

Question：品类在探索期、成长期、成熟期，还是衰退期？

Input Contract：

- 市场增长率：Amazon 关键词年度趋势已收集。
- 需求增长率：Amazon 关键词年度趋势已收集；Google 未收集。
- 产品品种：Sorftime/SellerSprite 商品池和节点证据已收集。
- 竞争者数量：关键词搜索结果竞品数量已收集。
- 进入壁垒：由评价门槛、品牌集中度、价格带、广告和 listing 成熟度推断。
- 技术变革：本章只判断光 + 声 + routine 融合，不进入产品技术细节。

Processing：

- 市场增长率：负。
- 需求结构：传统大词下滑，但融合产品仍有高销量代表。
- 竞争者数量：多。
- 评论门槛：高低分层，JALL/Philips/BUFFBEE 等老品评论深。
- 新品窗口：Odokee/REACHER 等中价融合产品证明仍有进入窗口。

Output Draft：

- 传统 wake up light / alarm clock：成熟期或成熟后期。
- `sunrise + sound + sleep routine` 融合分支：成熟底盘里的再分化窗口，不是完整成长期。

Evidence Sufficiency Review：

- 通过项：生命周期判断可由关键词下滑、竞品数量、评论门槛、新品起量共同支持。
- 不足项：缺完整新品上架分布和品类年销售额曲线。

Red Team Argument：

- 反方：成熟底盘意味着进入难、价格战、评价门槛高。
- 正方：如果融合分支能把“只是闹钟”升级成“睡眠唤醒体验”，就不是同一个价值锚。
- 公司能力视角：我们适合做光效体验和品质可靠性，但不适合做低价白牌；所以只能选择中价/中高价、前台价值清楚的切口。

Revised Conclusion：

> 生命周期判断是“成熟大盘 + 融合分支窗口”。这要求第 3 章不能只拆低价 wake-up-light，而要拆四个战场：premium routine、中价融合、低价声音机、传统光疗/闹钟。

## 2.2 亚马逊渠道分析

### 2.2.1 亚马逊关键词搜索趋势

Template Node：亚马逊关键词搜索趋势

Question：哪个关键词才是有效入口？关键词背后是否代表同一个市场？

Input Contract：

- Amazon 关键词月搜索趋势：已收集。
- 当前 keyword_detail：已收集。
- 年度销量曲线：全市场未收集，代表 ASIN 已有部分 SellerSprite 近 14 个月数据。

Evidence Acquisition：

- Sorftime 当前 keyword_detail：
  - `sunrise alarm clock`：月搜索量 128,138，竞品数 3,333，CPC 0.86。
  - `wake up light`：月搜索量 6,193，竞品数 121,153，CPC 0.96。
  - `sound machine alarm clock`：月搜索量 10,156，竞品数 5,792，CPC 1.50。
- Sorftime 年度趋势：四个词年度总量均下降。

Processing：

- 比较月搜索量：`sunrise alarm clock` 明显大于其他两个垂直词。
- 比较竞品数：`wake up light` 竞品数异常高，且 top product 混入 book light / night light，说明语义污染严重。
- 比较 top products：`sunrise alarm clock` 混入 Echo Spot、DreamSky、Hatch、Sharp；`sound machine alarm clock` 混入 Magicteam、BrownNoise、Hatch、DreamSky，说明真实战场不是单关键词。

Output Draft：

- `sunrise alarm clock` 是更干净的 Amazon 入口词。
- `wake up light` 不能作为单独边界。
- `sound machine alarm clock` 是必须纳入的相邻战场，不是可选补充。

Evidence Sufficiency Review：

- 通过项：关键词入口判断有当前月、年度趋势、Top 产品结构支持。
- 不足项：ABA 转化词和购买份额未收集。

Red Team Argument：

- 反方：如果主入口是 `sunrise alarm clock`，它可能只是传统闹钟/低价市场，不适合我们。
- 正方：Top 产品里 Hatch 和 Odokee 证明中高价和中价融合都在这个入口里存在。
- 公司能力视角：我们的机会不是抢泛闹钟，而是在 `sunrise alarm clock` 入口里做“更像灯具/睡眠体验”的价值表达。

Revised Conclusion：

> 第 2 章的关键词边界应改为：核心入口 `sunrise alarm clock`，辅助验证 `sound machine alarm clock`，污染词 `wake up light` 只保留为 seed，不作为市场边界。

### 2.2.2 亚马逊市场容量&趋势

Template Node：亚马逊市场容量&趋势

Question：Amazon 渠道是否有足够容量？这个容量是否能规划销售目标？

Input Contract：

- 类目数据：部分已收集。
- 销量/销售额：代表 ASIN 和关键词 Top100 样本已收集，完整品类年度曲线未收集。
- 客单价：代表 ASIN 已收集。
- 价格段：代表 ASIN 已收集，完整 Top50 价格分布未收集。
- 上架时间：部分新品证据已收集，完整 launch-date distribution 未收集。

Evidence Acquisition：

- SellerSprite v4 冻结证据：
  - Hatch：13,258 units，$169.99。
  - Odokee：8,667 units，$53.99。
  - REACHER：4,362 units，$32.99。
  - JALL：2,894 units，$32.88。
  - Philips：3,070 units，$108.99。
- Sorftime current keyword_detail top products：
  - `sunrise alarm clock` top products include Echo Spot 17,225 units, DreamSky 15,014, Hatch 14,125 / 12,421, Sharp 13,016.
  - `sound machine alarm clock` top products include Magicteam 24,336, Echo Spot 17,225, BrownNoise 16,627, DreamSky 15,014, Hatch 14,125.

Processing：

- 用代表 ASIN 不同价格带判断战场层级。
- 不用关键词搜索量直接替代销量。
- 用 Top 产品月销量证明 Amazon 渠道有成交容量，但不推算全市场总额。

Output Draft：

- Amazon 渠道有足够容量继续分析。
- 价格带并非只有低价，$53.99 Odokee 和 $169.99 Hatch 都有销量。
- 但完整 Amazon 品类规模和年度销售曲线仍是 `not_collected`。

Evidence Sufficiency Review：

- 通过项：足以判断“有容量、有中价/高价锚、有成交”。
- 不足项：不足以规划精确销售目标、市场份额目标和年销售额。

Red Team Argument：

- 反方：Top ASIN 销量不等于我们能拿到销量，尤其 Hatch 有品牌势能。
- 正方：Odokee/REACHER 证明非 Hatch 品牌也能在中价/中低价起量。
- 公司能力视角：我们不应复制 Hatch 的订阅生态，也不应卷 $20 低价声波机；更适合用灯具体验和品质做中价可感知价值。

Revised Conclusion：

> Amazon 容量足够进入第 3 章，但不能直接给销售目标。下一章必须回答：哪些销量来自品牌势能，哪些来自产品定义，哪些来自价格/广告。

### 2.2.3 品牌集中度

Template Node：品牌集中度

Question：这个市场是头部垄断，还是仍有新品牌进入空间？

Input Contract：

- 亚马逊品类品牌数据：部分已收集。
- 其他渠道品牌数据：部分公开页面已收集。
- 全量品牌数量：not_collected。
- N/A 品牌归因清洗：not_collected。

Evidence Acquisition：

- Sorftime `sunrise alarm clock` Top5 brand sample share：
  - N/A 18.42%，DreamSky 12.74%，Odokee 7.67%，Amazon 7.48%，Dreamegg 5.87%。
- Sorftime `sound machine alarm clock` Top5 brand sample share：
  - N/A 11.76%，Magicteam 7.81%，Odokee 5.72%，Amazon 5.12%，BrownNoise 4.94%。
- Sorftime `wake up light` Top5 brand sample share：
  - N/A 10.80%，Glocusent 5.46%，MediAcous 4.20%，Dreamegg 3.96%，Odokee 3.92%。

Processing：

- 计算 Top5 sample share。
- 对 N/A 做风险标注，因为里面可能包含 Hatch/Sharp 等未识别品牌。
- 区分“品牌集中度”与“卖家/亚马逊自营集中度”。

Output Draft：

- `sunrise alarm clock` 样本 Top5 集中度约 52.18%，但 N/A 过高，需要清洗。
- `sound machine alarm clock` 样本 Top5 集中度约 35.35%，更分散。
- 这不是绝对垄断市场，但部分入口有强品牌/强卖家存在。

Evidence Sufficiency Review：

- 通过项：足以判断“不是单一品牌垄断”。
- 不足项：N/A 未清洗，不能给精确品牌垄断系数。

Red Team Argument：

- 反方：如果 N/A 里主要是 Hatch、Sharp、Amazon，自然集中度可能被低估。
- 正方：Odokee、Dreamegg、Magicteam、DreamSky 等仍有可见份额，说明白牌/新品牌并非完全无路。
- 公司能力视角：我们不适合进入最低价分散市场；更适合找头部品牌没有覆盖好、但低价白牌又做不好的体验切口。

Revised Conclusion：

> 品牌集中度不是最大阻塞，最大阻塞是“我们要用什么前台价值从成熟低价和 premium 品牌中间切出位置”。

### 2.2.4 市场新品趋势

Template Node：市场新品趋势

Question：新品是否还有机会？机会来自低价、功能融合还是品牌打法？

Input Contract：

- 新 ASIN 列表：部分收集。
- 上线时间：部分收集。
- 类目排名：部分收集。
- 销量占比：代表 ASIN 部分收集。
- 广告/关键词投放线索：部分 traffic/ranking 收集。
- 产品定义差异：本章只做归类，不深拆详情。

Evidence Acquisition：

- Odokee B0DGXD6WVW：SellerSprite v4 月销量 8,667，$53.99；Sorftime ranking 在 `sunrise alarm clock` 多次 page 1。
- REACHER B0BZW7WY5M：月销量 4,362，$32.99。
- BUFFBEE B0B2ZTZZ3F：月销量 4,860，$21.99；在 `sound machine alarm clock` page 1 较稳定。
- Hatch B0F7C6XJ3P：在 `sound machine alarm clock` 有曝光，但更波动。

Processing：

- 将新品/增长样本分成中价融合、低价声音机、premium routine。
- 排除“只要新品就能起量”的误判。
- 用排名趋势判断是否真实出现在核心词/相邻词前台。

Output Draft：

- 新品窗口存在，但不是空白窗口。
- 中价融合型比纯低价或纯 premium 更适合后续重点拆。
- 新品是否可复制，必须到第 3 章拆流量、页面、评论、品牌和定位。

Evidence Sufficiency Review：

- 通过项：有代表样本。
- 不足项：缺全量 launch-date distribution 和最近 12 个月新品表。

Red Team Argument：

- 反方：Odokee 的增长可能来自广告/价格/评论，不一定来自产品定义。
- 正方：即便如此，它也证明中价融合不是完全无效。
- 公司能力视角：如果中价融合靠低价堆功能，我们不适合；如果靠光效体验、设计、可靠品质、清晰卖点，我们适合。

Revised Conclusion：

> 第 3 章要重点拆 Odokee/REACHER/BUFFBEE/Hatch，不是为了选一个竞品，而是判断哪一种新品进入机制可复制且适合公司能力。

## 2.3 其他渠道市场机会

Template Node：其他渠道市场机会

Question：除了 Amazon，这个品类在其他渠道是否有验证和布局价值？

Input Contract：

- Walmart 数据：Sorftime live 已收集。
- Target 页面：公开网页已收集。
- HomeDepot/Lowe's 结构化数据：not_collected。
- 其他渠道 Top1000：not_collected。

Evidence Acquisition：

- Walmart `sunrise alarm clock`：SearchVolume 32,829，ProductCount 443，首页均价 $44.58，平均评价 389.75，平均星级 4.30。
- Walmart `wake up light`：live call 返回暂无相关数据。
- Target Hatch Restore 3：$169.99，4.0 stars，2262 reviews。
- Walmart Hatch page：Hatch Restore 2 $169.99，同时有 refurbished/discount variants。
- Best Buy / Macy's：Hatch Restore 3 $169.99。

Processing：

- 判断 Walmart 是否支持渠道验证。
- 判断 Target/Best Buy/Macy's 是否支持 premium retail anchor。
- 不把 HomeDepot/Lowe's 作为事实依据，因为没有结构化数据。

Output Draft：

- Walmart 对 `sunrise alarm clock` 有有效搜索和产品池。
- Hatch 的跨渠道零售存在证明 premium routine 不是 Amazon 孤例。
- 对公司而言，线下/零售渠道可能重要，但本章不能规划渠道策略，只能作为第 3/5/7 章输入。

Evidence Sufficiency Review：

- 通过项：Walmart 和 premium retail anchor 有证据。
- 不足项：HomeDepot/Lowe's/Target 全量结构化价格评论表未收集。

Red Team Argument：

- 反方：Walmart 的均价 $44.58 更接近中低价，说明线下/平台未必接受中高价新品牌。
- 正方：Hatch 在多渠道 $169.99 存在，说明高价不是不可能，但需要品牌/体验/内容支撑。
- 公司能力视角：我们更适合先证明 Amazon 前台价值，再考虑零售渠道；若走零售，品质和供应稳定性会成为优势。

Revised Conclusion：

> 其他渠道验证了两件事：`sunrise alarm clock` 是比 `wake up light` 更有效的渠道入口；premium price anchor 存在，但不是普通新品牌可以直接复制。

## 3. 本章总 Red Team Argument

### 反方立场

1. Amazon 站内四个相关词年度总量都下降，不能证明需求增长。
2. Google Trends 未采集，站外趋势未知。
3. Wake up light 精确全球 TAM 未采集，宏观 sleep tech 只是代理。
4. Hatch 的高价成功可能来自品牌、内容、订阅和零售，不是产品形态本身。
5. Odokee/REACHER/BUFFBEE 起量可能来自价格、广告或短期流量，不一定能复制。
6. 我们不具备最低成本优势，如果切入低价成熟闹钟，很容易被打穿。

### 正方立场

1. Amazon 站内大盘下降不等于所有分支都没有机会；成熟底盘里仍有结构迁移。
2. `sunrise alarm clock` 仍有月搜索量 128,138，是有效入口词。
3. `sound machine alarm clock` 虽然月搜索量只有 10,156，但 Top 产品销量很高，说明它代表的是融合战场而不是小词。
4. Odokee 等中价融合产品证明非 Hatch 品牌也有进入窗口。
5. Hatch 的跨渠道存在说明用户愿意为“睡眠例程系统”支付高价，但新品牌不能直接复制 Hatch 生态。
6. Wake up light 与灯具、光效、卧室体验相邻，落在公司能力边界附近。

### 企业资源过滤后的中立结论

这个市场不是“因为增长所以做”，而是“如果能找到适合公司能力的结构迁移切口，才值得继续”。

适合继续分析的切口不是：

- 更便宜的低价闹钟；
- 普通白牌 wake-up-light；
- 复制 Hatch 的订阅生态；
- 只靠 coupon 或灰帽打法起量。

更适合进入第 3 章验证的切口是：

> 中价到中高价、围绕光效/卧室氛围/睡眠唤醒体验的融合产品。它必须让消费者第一眼看懂比传统闹钟更有价值，同时不落入 Hatch 式高品牌门槛和低价白牌价格战。

## 4. Review Gates

| Gate | 结果 | 说明 |
|---|---|---|
| 模板一致性 | pass | 已覆盖 2.1 / 2.2 / 2.3 和最终输出，没有展开第 3 章细节 |
| 数据真实性 | pass_with_gaps | 已标注 Google Trends、精确 TAM、全量销售曲线等缺口 |
| 章节越界 | pass | 竞品只作为第 3 章输入池，不做品牌深拆 |
| 补证 review | pass_with_gaps | 可调用 Sorftime 已补；SellerSprite/GBrain 不可用项明确标注 |
| Red Team | pass | 已加入公司能力、白帽、工艺边界过滤 |
| 阅读可用性 | pending_html | HTML 需要结论前置、图表完整、来源后置 |

## 5. Human Decision Stop

本章不自动进入第 3 章。建议在 Codex 中选择：

- A. 通过，并以“结构迁移切口”进入第 3 章品牌/竞品拆解。
- B. 补证后再判断，优先补 Google Trends / ABA / Top50 ASIN launch-date / Target-Walmart结构化表。
- C. 退回重定义市场边界，重新选择 seed keyword 和 ASIN 池。

当前 AI 建议：`A 或 B` 都合理。

- 如果目标是继续探索产品机会：选 A，进入第 3 章拆“哪些增长机制可复制且适合我们”。
- 如果目标是严格投资前判断：选 B，先补 Google Trends、ABA 和 Top50 ASIN 表。
