# GitHub 发布说明

## 推荐仓库形态

最简单的发布方式：让仓库根目录就是本 skill 文件夹。

```text
product-strategy-template-os/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
  assets/
  examples/
```

安装：

```bash
npx skills add https://github.com/<owner>/product-strategy-template-os
```

如果放在 monorepo 子目录，安装器需要支持 `--skill product-strategy-template-os` 或对应子目录参数。

## 发布前检查

运行：

```bash
python3 scripts/sanitize_check.py .
python3 scripts/init_run.py --category "wake up light" --out /tmp/wake-up-light-run
```

确认：

- 没有 access token / app secret / Authorization header。
- 没有原始供应商机密报价。
- 示例案例是脱敏案例。
- `SKILL.md` 在仓库根目录或安装器可识别的位置。

## 可见性建议

如果示例包含公司能力、产品结论、案例数据，先建 private repo。要公开时，删掉公司专属内容或改成通用 red-team baseline。
