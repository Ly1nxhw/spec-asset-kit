# Decision Log

## 核心解释

| 决策/演进 | 原因 | 影响 | 来源 |
|---|---|---|---|
| 从单一写入 CLI 演进为支持安全预览的 CLI | 用户需要看到将要写入的内容，但不能实际写文件。 | 新实现必须保留普通写入，同时新增无副作用分支。 | `evaluation/cases/sim-cli-dry-run-001/input.md` |
| 不新增 commands 分层 | 当前业务能力集中在单文件 CLI，需求规模小。 | 避免把 dry-run 做成不存在的 `src/commands/` 模块。 | `evaluation/cases/sim-cli-dry-run-001/case.yml` |

## 实现锚点

- `sample_cli.py`: 保持小范围演进。
- `gold-files.txt`: 关键文件仅包含 CLI 和测试。

## 待确认问题

- 模拟 case 没有 changelog 或真实 PR 历史，决策来源只来自 case 输入和 gold notes。
