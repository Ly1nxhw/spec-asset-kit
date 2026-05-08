# Domain Glossary

## 核心解释

| 术语 | 业务含义 | 易混淆点 | 来源 |
|---|---|---|---|
| message | 用户希望写入文件的文本内容。 | 不是日志消息，也不是状态输出。 | `sample_cli.py` |
| output | 用户指定的目标文件路径。 | dry-run 时不应创建该文件。 | `sample_cli.py`, `tests/test_sample_cli.py` |
| dry-run | 预览将要发生的写入动作，但不执行实际写文件。 | 不是空跑整个程序；仍应解析参数并输出 preview 信息。 | `evaluation/cases/sim-cli-dry-run-001/input.md` |
| preview | 面向用户的终端反馈，说明写入会被跳过。 | 不要求与最终写入文件内容完全同格式。 | `evaluation/cases/sim-cli-dry-run-001/input.md` |

## 实现锚点

- `sample_cli.py`: `--message` 与 `--output` 参数定义位置。
- `tests/test_sample_cli.py`: `output` 文件是否存在的行为断言。

## 待确认问题

- preview 是否需要包含目标文件路径没有在需求中明确。
