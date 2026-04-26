# Rewrite Examples

## Bad

```text
Hub approval already succeeded. I checked the DB, then the registration endpoint, then the token state, then the viewer, and eventually confirmed the issue was local token sync...
```

Why it is bad:

- too long
- mixes evidence collection with the durable rule
- hard to scan during retrieval

## Better

```text
If Hub approval is active but an agent still shows pending, compare Hub registration status with the agent's configured cloud memory route. When Hub is active but the agent has no usable route token, route setup is stale. kb_domain: skills. Source of truth: cloud MemTensor Hub setup runbook.
```

Why it is better:

- starts with the condition
- states the durable conclusion
- gives the recovery pointer
- classifies the memory
- points to a source of truth

## Replacement Pattern

Use this when swapping out a verbose shared memory:

```text
Old memory:
- long, narrative, mixed evidence and conclusion

New memory:
- one compact operating rule
- one recovery pointer
- one `kb_domain`
- one source-of-truth path

Cleanup action:
- share new compact memory
- unshare old verbose memory

## Reroute Example

```text
Old memory:
- detailed timeline of one host's container restart and debugging commands

Decision:
- useful locally
- not yet a clean business, AI, or skill knowledge object

Action:
- keep local or stage as `team_candidate`
- do not publish to `team_shared`
```
```
