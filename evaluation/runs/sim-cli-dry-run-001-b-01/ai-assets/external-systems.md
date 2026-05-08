# External Systems

## 核心解释

当前模拟 case 没有真实外部系统。唯一外部边界是本地文件系统：

| 边界 | 业务语义 | 失败影响 | 来源 |
|---|---|---|---|
| output file | 用户指定的写入目标。 | dry-run 如果误写文件，会破坏“安全预览”承诺。 | `sample_cli.py`, `evaluation/cases/sim-cli-dry-run-001/input.md` |

## 实现锚点

- `Path.write_text(...)`: 普通模式的文件系统写入点。

## 待确认问题

- 没有涉及远程服务、数据库、队列或人工运营系统。
