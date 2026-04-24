# Source Strategy

The brief should behave like an analyst, not a scraper.

## Runtime Shape

For Hermes unattended runs, prefer this shape:

```text
deterministic source collector
-> candidate bundle
-> Hermes ranking + writing
-> Feishu digest + Obsidian deep report
```

The collector should favor stable official feeds and sitemaps before any open-ended web search.

## Expanded Source Model

The fuller operating picture for this brief is:

```text
social-radar
-> official-confirm
-> deterministic source collector
-> candidate bundle
-> Hermes ranking + writing
-> Feishu digest + Obsidian deep report
-> optional NotebookLM research brief
```

Only the deterministic collector is currently in the unattended production path. `social-radar` and `NotebookLM` are research sidecars around that core.

## Layer 0: Social Radar

Use social and community signals as a discovery layer only.

Good examples:

- official X posts
- official YouTube uploads
- official GitHub release activity
- major maintainer posts linked to a paper, repo, or product page

Rule:

- no social-only item should enter the final digest without official confirmation or a clearly labeled `二手源` fallback.

Current wired collector sources:

- OpenAI News RSS
- Google DeepMind News RSS
- Google AI Blog RSS
- Anthropic sitemap
- Mistral sitemap
- Hugging Face blog feed
- NVIDIA developer blog feed
- Qwen blog feed
- ERNIE English blog sitemap
- arXiv `cs.AI`
- arXiv `cs.CL`

## Priority Tiers

### Tier 1: Official And Primary Sources

Start here first. These sources define the day's backbone.

- Model labs and platform vendors:
  - OpenAI
  - Anthropic
  - Google
  - Meta
  - Microsoft
  - xAI
  - Mistral
  - NVIDIA
  - Hugging Face
- China high-signal players:
  - DeepSeek
  - Alibaba / Qwen
  - Baidu
  - ByteDance / Doubao
  - Moonshot AI / Kimi
  - MiniMax
  - Zhipu

Preferred source types:

- official news pages
- official blogs
- release notes
- model cards
- official GitHub release notes
- product or API announcements

Current collector-ready additions verified on `2026-04-24`:

- Google DeepMind news RSS: stable and directly ingestible
- ERNIE blog English sitemap: stable, but requires sitemap-relative URL resolution

Official but not yet wired into the deterministic collector:

- xAI: official sitemap exists in `robots.txt`, but direct crawling currently returns `403`
- Microsoft Research: official pages currently return `403` to unattended fetches
- MiniMax: official sitemap path is reachable, but the useful news structure needs a custom extractor
- DeepSeek API Docs: official sitemap is reachable, but current entries are doc-heavy and need better filtering for product/news updates
- Moonshot / Kimi: public web endpoints are not currently stable enough for deterministic unattended collection

### Tier 2: Research And Open Source

Use these to catch meaningful capability movement and notable releases.

- arXiv papers with real downstream impact or unusually important results
- Hugging Face blog or model releases
- major open-source model, agent, eval, or tooling releases
- important GitHub repo or release activity when it changes what practitioners can do

### Tier 3: Capital, Policy, And Regulation

Include only when the event materially changes the field.

- major financing rounds with strategic relevance
- acquisitions that shift platform power or distribution
- regulatory rulings, safety rules, export controls, or compliance changes with real operational effect

## Signal Criteria

Keep an item when at least one of these is true:

- it launches or materially upgrades a major model, product, API, or platform capability
- it changes developer economics, distribution, or access in a meaningful way
- it represents a real benchmark, reasoning, multimodal, agent, or infrastructure step-change
- it is a notable open-source release that changes what builders can realistically ship
- it creates meaningful policy, governance, market, or competitive implications

## Exclusions

Drop items that are mainly:

- rumor, leak, or inference without primary confirmation
- secondary repost without additional signal
- SEO content farm summaries
- generic "top AI news" aggregations
- small wrapper launches with no broader significance
- social-media heat without durable facts

## Deduping Rules

- treat one event with many writeups as one record
- keep the primary announcement as the anchor source
- attach one or two supporting links only when they add real context
- if the only accessible source is secondary, label it `二手源`

## Blocking And Fallback Rules

- if a primary site is blocked by anti-bot tooling, prefer an accessible official mirror, RSS feed, blog page, or release note page
- still try to link back to the primary announcement when recoverable
- if no primary page is accessible, use a high-credibility secondary source and mark it clearly

## Ranking Order

Rank candidates in this order:

1. platform and model moves
2. research or open-source advances with practical impact
3. distribution, pricing, or ecosystem moves
4. policy and capital shifts
5. everything else

## NotebookLM Position

NotebookLM is not a primary source collector in this system. It is a deeper synthesis layer for already confirmed topics.

Use it after the daily brief when:

- a topic deserves a second-pass explanation
- several sources need cross-reading
- the user wants a decision-oriented memo instead of a short daily item
