# 数据源路由

## 总规则

所有数据必须真实、可追溯。能自动采集的由 pipeline 自动采集；只有离线事实和动态质量判断才问人。

## 常见数据源

| 数据需求 | 默认路线 | 说明 |
|---|---|---|
| Amazon 销量、价格、评论、BSR、ASIN 池 | MCP/API，例如 Sorftime、SellerSprite、Gerp Ads、Jungle Scout | 批量数据优先走结构化工具 |
| 关键词趋势 | Sorftime/SellerSprite/Gerp Ads/Google Trends | 必须说明首尾、环比、同比、近 3 月 |
| ABA / SIF / 反查关键词 | SellerSprite/Gerp Ads/用户上传 Excel | 认证失败时写 `not_available_in_current_session` |
| Amazon 前台 | Browser | 主图、视频、A+、五点、coupon/deals 必须打开页面看 |
| 评论 / Q&A | MCP/API/导出 Excel/browser | 引用必须有来源，不编评论 |
| Walmart/Target/HomeDepot/Lowe's | MCP/API/browser | 判断其他渠道机会 |
| 独立站 / 官方页 | browser/web | 用于品牌叙事、站外承接、科学背书 |
| 社媒内容 | browser/web/上传截图 | TikTok/YouTube/Instagram/Reddit/论坛 |
| 1688 / 供应商线索 | MCP/browser/manual verification | 平台价格可能欺骗，必须人工复核 |
| BOM / MOQ / 模具费 / 交期 | manual_input_required | 必须来自供应商或内部工程 |
| 公司能力边界 | user_input / company baseline | 不可从外部网页推断 |

## 趋势报告格式

任何趋势结论必须写清比较周期：

```text
首尾：first available period -> latest period
环比：latest vs previous period
同比：latest vs same period last year
近3月：latest vs three periods earlier
```

没有热搜趋势数据时写 `无热搜趋势数据`，不要当作 0 需求。

## 证据状态

```text
collected_and_used
collected_not_expanded
missing_to_collect
manual_required
not_collectable_now
not_available_in_current_session
```

## Provenance Schema

```json
{
  "source_type": "MCP | API | file | web | user_input | offline_supplier | inference",
  "source_ref": "path, URL, tool name, ASIN, table id, or human note",
  "collected_at": "YYYY-MM-DD or unknown",
  "raw_available": "yes | no",
  "transformation": "none | normalized | summarized | translated | classified | calculated",
  "confidence": "high | medium | low"
}
```
