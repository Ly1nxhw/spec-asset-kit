# Open Questions

## 待人工确认

| ID | 问题 | 为什么重要 | 线索来源 | 影响资产 |
|---|---|---|---|---|
| AQ001 | preview 是否必须包含目标文件路径？ | 影响 CLI 输出契约和测试断言粒度。 | `evaluation/cases/sim-cli-dry-run-001/input.md` | `domain-glossary.md`, `business-rules.md` |
| AQ002 | output 父目录不存在时，dry-run 是否仍应成功？ | 影响 dry-run 是否完全绕过文件系统校验。 | `sample_cli.py` | `user-journeys.md`, `business-rules.md` |

## 已回答待整理

- 无。

## 本次无足够线索

- 无真实外部系统、人工运营流程或历史 PR 决策链路。
