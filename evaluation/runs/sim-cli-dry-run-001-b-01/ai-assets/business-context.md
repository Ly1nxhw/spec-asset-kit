# Business Context

## 核心解释

### 业务场景：安全预览文件写入

| 项 | 内容 |
|---|---|
| 含义 | 用户通过 CLI 把 `message` 写入 `output` 文件；新增 dry-run 后，用户可以先预览将要写入的内容。 |
| 价值 | 在不产生文件副作用的前提下确认输入是否正确。 |
| 参与者 | CLI 使用者。 |
| 来源 | `evaluation/cases/sim-cli-dry-run-001/input.md`, `sample_cli.py`, `tests/test_sample_cli.py` |

## 实现锚点

- `sample_cli.py`: CLI 参数解析和文件写入入口。
- `tests/test_sample_cli.py`: 现有写入行为测试。

## 待确认问题

- 预览文本的精确格式没有业务强约束，只需清楚表达不会写文件。
