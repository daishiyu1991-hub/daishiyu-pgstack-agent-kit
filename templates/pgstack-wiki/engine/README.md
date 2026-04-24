# PGBrain Engine

`pgbrain_engine.py` is the deterministic local engine for this starter node.

Commands:

```bash
python3 engine/pgbrain_engine.py status
python3 engine/pgbrain_engine.py doctor
python3 engine/pgbrain_engine.py query "AI Daily Brief Job"
python3 engine/pgbrain_engine.py related "AI Daily Brief Job"
python3 engine/pgbrain_engine.py maintenance
python3 engine/skillpack_check.py
```

The engine is filesystem-backed and intentionally small.

`skillpack_check.py` validates the canonical repo-level skill manifest, resolver
coverage, and required `skills/*/SKILL.md` files. `PGBrain Engine` validate and
doctor also call this check.
