# User Journeys

## 已确认知识

### Journey: 普通写入

| 步骤 | 行为 |
|---|---|
| 1 | 用户传入 `--message` 和 `--output`。 |
| 2 | CLI 解析参数。 |
| 3 | CLI 把 message 写入 output 文件。 |
| 4 | CLI 输出写入完成反馈。 |

### Journey: dry-run 预览

| 步骤 | 行为 |
|---|---|
| 1 | 用户传入 `--message`、`--output` 和 `--dry-run`。 |
| 2 | CLI 解析参数，与普通写入使用同一输入语义。 |
| 3 | CLI 输出 preview 信息。 |
| 4 | CLI 不创建、不修改 output 文件。 |

## 候选线索

- 如果 output 的父目录不存在，dry-run 是否仍应成功只输出预览没有明确来源。

## 实现锚点

- `build_parser()`: 增加 dry-run 参数。
- `main([...])`: 连接参数、业务分支和用户反馈。
- `tests/test_sample_cli.py`: 覆盖普通写入与 dry-run 预览。

## 待确认问题

- 如果 output 的父目录不存在，dry-run 是否也应跳过目录校验没有明确；当前需求只约束不写文件。
