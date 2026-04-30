# HTML 报告样式

## 阅读顺序

1. 结论先行。
2. 一眼可判断的图表/矩阵。
3. 模板节点 Input -> Processing -> Output。
4. 证据充分性 review。
5. red-team 争论。
6. 人类判断选项。
7. 来源与过程文件放到底部。

## 视觉原则

- 低饱和色，不要高噪音颜色。
- 卡片留白充足，避免密密麻麻。
- 中文正文易读，标题可以用宋体类。
- 用横向对比矩阵、趋势图、条形图、漏斗图、关系图帮助判断。
- 不要把所有证据堆到主阅读路径，细节放下方。
- HTML 不弹决策框；默认在 Codex 里让用户选。

## Index 页

Index 是路线图，不是结论页。锁定后只允许：

- 更新章节状态。
- 增加/修正链接。
- 更新简短章节摘要。
- 修坏链接或事实错误。

不要：

- 重排章节。
- 改模板结构。
- 放 AI 自己的最终决策。
- 把 process/runtime 页面当产品结论页。

## 报告页最低结构

```html
<nav>返回索引 + 章节名</nav>
<header>章节结论与当前人类选择记录</header>
<section>本章最小幸存结论</section>
<section>核心图表/矩阵</section>
<section>模板节点 Input -> Processing -> Output</section>
<section>补证 Review</section>
<section>Red-team Argue</section>
<section>Human Decision Stop</section>
<section>Sources</section>
```
