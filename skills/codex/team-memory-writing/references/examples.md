# Team Memory Writing Examples

## Bad

```text
I checked the DB, then I queried the registration endpoint, then I looked at the viewer, and eventually confirmed that the approval had worked remotely but the local client was still stale...
```

Problem:

- too long
- too narrative
- hard to retrieve

## Also Bad

```text
I changed the model on my Mac to gpt-5.4-mini, restarted Hermes, and now it feels more stable for me.
```

Problem:

- personal preference
- host-specific
- not a team knowledge-base object
- belongs in local continuity, not in `team_shared`

## Better

```text
If Hub approval is already active but the local client still shows pending, compare Hub registration status with local `client_hub_connection`. When Hub is active but local `user_token` is empty, local token sync is stale. kb_domain: skills. Source of truth: install-memos-local-hermes-plugin skill.
```

Why it works:

- names the recurring condition
- gives the durable conclusion
- gives the next recovery move
- classifies the object
- links to the canonical source

## Another Good Pattern

```text
When a live Hub connection exists, MemTensor team-page cleanup has two layers: local `team_shared_chunks` and remote Hub memories. If the team page still looks dirty after local cleanup, query `/api/v1/hub/memories` and unshare the remote rows too. kb_domain: skills. Source of truth: pgstack cleanup policy.
```

## Good AI-Knowledge Pattern

```text
gstack is not just a prompt library; it encodes reusable expert workflows with roles, stages, artifacts, and gates. Treat it as an AI work operating system when adapting it to new domains. kb_domain: ai_knowledge. Source of truth: gstack atomic memory and local wiki.
```

## Reroute Instead Of Publish

```text
The container on one host exited twice with code 137 after a local restart sequence.
```

Better decision:

- useful for investigation
- not yet a clean `business`, `ai_knowledge`, or `skills` object
- keep local or stage as `team_candidate`
- do not publish directly to `team_shared`
