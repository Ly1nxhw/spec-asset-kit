# Business Rules

## 核心解释

| 规则 | 适用场景 | 例外 | 来源 | 实现锚点 |
|---|---|---|---|---|
| 普通模式必须写文件 | 未提供 `--dry-run` 时 | 无 | `tests/test_sample_cli.py` | `write_message()` |
| dry-run 模式不得创建输出文件 | 提供 `--dry-run` 时 | 无 | `evaluation/cases/sim-cli-dry-run-001/input.md` | `main([...])`, `write_message()` |
| dry-run 仍需给出用户反馈 | 提供 `--dry-run` 时 | 文案未严格限定 | `evaluation/cases/sim-cli-dry-run-001/input.md` | `print(...)` |
| 原有 newline 行为必须保持 | 普通写入路径 | 无 | `sample_cli.py`, `tests/test_sample_cli.py` | `path.write_text(message + "\n")` |

## 实现锚点

- `sample_cli.py`: 写入副作用集中在 `write_message()`。
- `tests/test_sample_cli.py`: 需要新增 no-file dry-run 断言。

## 待确认问题

- dry-run preview 是否应返回不同退出码没有明确；现有成功路径返回 0，应保持。
