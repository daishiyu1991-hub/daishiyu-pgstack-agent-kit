# 第 2 章旧产物复盘 v1

目的：在生成“完整报告版”前，复盘旧页面哪些结构应该被继承，防止因为重做证据版而丢掉有效的判断体验。

## 1. 旧产物列表

| 文件 | 定位 | 处理 |
|---|---|---|
| `quality-review-template-ch2-market-competition-v1.html` | 视觉判断版雏形 | 继承其阅读节奏和图表结构 |
| `quality-review-template-ch2-market-competition-v8.html` | 证据审计版 | 继承其数据口径、补证 review、red-team 和缺口 |
| `quality-review-template-ch2-decision-pass-v1.html` | 决策记录 | 继承通过状态和下一章解锁问题 |

## 2. v1 值得继承的部分

- “先看结论”的阅读顺序。
- “图表先看”的结构，不让用户先读大量文字。
- 赛道地图，把市场拆成不同战场而不是均值市场。
- 价格 × 销量的横向判断。
- 关键词入口的解释，不把关键词当 SEO 列表。
- A/B/C/D 选择和复制判断入口。

## 3. v1 不能直接继承的部分

- v1 标注 SellerSprite Google Trends 已采集，但当前 v8 重新调用时返回 `ERROR_UNAUTHORIZED`，完整报告不能把 Google Trends 作为已采集事实。
- v1 其他渠道写 `not collected`，但 v8 已补到 Walmart live 数据和 Hatch 多渠道公开价格锚，需要更新。
- v1 还没有完整的补证 review 和公司能力 red-team，需要接入 v8。

## 4. v8 值得继承的部分

- Amazon 站内完整年度趋势口径。
- Sorftime 当前 keyword_detail 和 Walmart keyword_detail。
- 证据缺口显式标注。
- 公司能力过滤器。
- 第 3 章对象池。
- 通过状态和下一章问题。

## 5. 完整报告版生成规则

完整报告不是新增一个旁路页面，而是当前章节的主报告。

结构必须合并：

```text
结论先行
-> 视觉赛道地图
-> 核心图表
-> 模板节点 2.1 / 2.2 / 2.3
-> 补证 review
-> red-team argue
-> 人类决策记录
-> 下一章输入
-> 来源和过程文件
```

索引页主入口应指向完整报告，而不是只把旧页补成一个参考链接。

## 6. 以后全局规则

每次章节重做前都要先做 `previous_artifact_review`。

不允许：

- 用新证据页替代掉旧的有效判断结构；
- 只在索引里补一个旧链接就算修复；
- 让完整报告变成证据页、判断页、决策页三个分散页面。

必须：

- 生成一页完整报告作为主入口；
- 把有效旧结构合并进主报告；
- 把历史版本放在来源/过程区，而不是让人自己拼。
