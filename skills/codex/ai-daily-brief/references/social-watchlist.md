# Social Watchlist

This is the first practical watchlist for the `social-radar` sidecar.

It is intentionally small and biased toward official sources that are easy to confirm.

## Operating Rule

Use this watchlist to detect candidate stories early.

Do not promote a watched signal into the final daily brief until it has been confirmed by:

- an official announcement page
- official docs or release notes
- an official repo or release
- a model card, paper page, or first-party product page

## Current Structured Config

Runtime-oriented watchlist file:

```text
$HERMES_HOME/skills/research/ai-daily-brief/scripts/social_watchlist.json
```

## Automation Support

Current rule for Hermes:

- `GitHub` channels are enabled as a first `beta` automation slice through public Atom feeds
- inside GitHub, `repo release feeds` are preferred over `org activity feeds` because they are closer to an official artifact and much less noisy
- `X` channels remain `manual` observation only
- `YouTube` channels remain `manual` observation only until a cleaner feed strategy is defined

This means the current Hermes social-radar sidecar is intentionally narrow:

```text
watchlist
-> GitHub beta automation
-> social-radar sidecar JSON
```

It is useful as a discovery layer, but it does not yet replace human review for X or YouTube.

## Tier A: Core Frontier Labs

- OpenAI
  - X: `https://x.com/OpenAI`
  - YouTube: `https://www.youtube.com/@OpenAI`
  - GitHub: `https://github.com/openai`
- Anthropic
  - X: `https://x.com/AnthropicAI`
  - GitHub: `https://github.com/anthropics`
- Google DeepMind
  - X: `https://x.com/GoogleDeepMind`
  - YouTube: `https://www.youtube.com/@GoogleDeepMind`
  - GitHub: `https://github.com/google-deepmind`
- Mistral
  - X: `https://x.com/MistralAI`
  - GitHub: `https://github.com/mistralai`

## Tier B: Open Source And Infra

- Hugging Face
  - X: `https://x.com/huggingface`
  - YouTube: `https://www.youtube.com/@huggingface`
  - GitHub: `https://github.com/huggingface`
- NVIDIA Developer
  - YouTube: `https://www.youtube.com/@NVIDIADeveloper`

## Tier C: China High-Signal Builders

- Qwen
  - GitHub: `https://github.com/QwenLM`
- DeepSeek
  - X: `https://x.com/deepseek_ai`
  - GitHub: `https://github.com/deepseek-ai`

## Current Repo Release Feeds

The first repo-level feeds now wired for Hermes are:

- OpenAI
  - `openai/openai-python`
  - `openai/openai-node`
  - `openai/openai-agents-python`
- Anthropic
  - `anthropics/claude-code`
  - `anthropics/anthropic-sdk-python`
- Mistral
  - `mistralai/mistral-common`
- Hugging Face
  - `huggingface/transformers`
- Qwen
  - `QwenLM/Qwen-Agent`

These were chosen because their release feeds are publicly reachable and the emitted events are much closer to digest-worthy product or SDK changes than generic org activity.

## Why These First

These channels satisfy at least one of:

- they often surface launches before all official blog surfaces update
- they point directly to repos, demos, docs, or model pages
- they are likely to generate meaningful same-day social signal
- they are stable enough to watch manually or semi-automatically

## Current Hermes Reality

What Hermes can currently do reliably:

- fetch selected GitHub repo release Atom feeds
- fetch GitHub org Atom feeds as a lower-signal fallback
- apply simple low-signal filtering to org activity events
- write a structured `latest_social_radar.json` sidecar

What Hermes is **not** yet doing in production:

- scraping X posts into structured candidates
- parsing YouTube channel activity into a stable feed
- promoting social-radar items directly into the final digest

## Not Included Yet

Deferred until a cleaner collector exists:

- Reddit feeds
- Hacker News feeds
- LinkedIn
- WeChat official accounts
- broader X scraping beyond this small official list

Those sources are useful, but they are noisier and more likely to blur the confirmation boundary.
