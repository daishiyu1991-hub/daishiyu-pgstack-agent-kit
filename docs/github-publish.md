# GitHub Publish Checklist

Before pushing this kit:

1. Run `./scripts/smoke_test.sh`.
2. Run `./scripts/sanitize_check.sh`.
3. Confirm `config/hermes-cron.example.json` has placeholders only.
4. Confirm no local Obsidian pages contain private notes.
5. Create a GitHub repository.
6. Push:

```bash
git init
git add .
git commit -m "Initial PGStack Agent Kit"
git branch -M main
git remote add origin git@github.com:daishiyu1991-hub/daishiyu-pgstack-agent-kit.git
git push -u origin main
```

If using HTTPS or a GitHub connector, use the equivalent publish flow.
