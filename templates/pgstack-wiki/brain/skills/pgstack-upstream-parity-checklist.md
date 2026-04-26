---
title: PGStack Upstream Parity Checklist
type: skill
created: 2026-04-26
updated: 2026-04-26
status: active
confidence: high
scope: local_pgstack
source_of_truth:
  - pgstack-gbrain-compatibility-layer.md
  - gbrain-operating-logic-compatibility-matrix.md
---

# PGStack Upstream Parity Checklist

## Compiled Truth

Any claim that PGStack has aligned, merged, replicated, covered, or finished
original `gstack + gbrain` must check the full upstream surface.

Do not answer from a feature-level impression. A tool-shaped shadow of a layer
is not the same as a merged operating protocol.

## Mandatory Parity Dimensions

Classify every dimension as:

```text
native-copied
adapted
substituted
partial
deferred
not-applicable
unknown
```

| Dimension | Current Default |
|---|---|
| Operating wrapper | adapted |
| Skills | adapted |
| Agents | partial |
| Jobs / minions | partial |
| Brain repo | adapted |
| Retrieval / memory | substituted |
| MCP / tools | adapted |
| Browser / verification | partial |
| Sync / packaging | adapted |
| Governance / maintenance | adapted |

## Agent Layer Gate

The agent layer is not merged until these are defined and tested:

- agent hosts
- specialist agent roles
- routing rules
- stop conditions
- artifact contracts
- review or verification gates
- memory write-back
- minion/job handoff
- MultiCA / ACP ownership
- Agent Kit packaging
- one real end-to-end chain

Until then, report:

```text
Agent layer: partial
```

Do not upgrade it just because Codex, Hermes, MultiCA, or MCP tools exist.

## Required Answer Format

For upstream parity questions, answer with:

```text
Short verdict:
Dimension table:
Biggest missing layer:
What is native-copied:
What is adapted:
What is substituted:
What is deferred:
Next merge gate:
```

## Typed Edges

- depends_on: [[pgstack-gbrain-compatibility-layer|PGStack GBrain Compatibility Layer]]
- depends_on: [[gbrain-operating-logic-compatibility-matrix|GBrain Operating Logic Compatibility Matrix]]
- implements: [[../../skills/brain-ops/SKILL|PGStack Brain Ops]]
- validated_by: [[pgbrain-engine-v1|PGBrain Engine v1]]

---

## Timeline

- 2026-04-26: Added to prevent installed PGStack Nodes from treating agent
  tooling as equivalent to a merged agent operating layer.
