---
description: "使用顺序号或时间戳创建功能分支"
---

# 创建功能分支

为给定规格创建并切换到新的 Git 功能分支。此命令只负责创建分支，规格目录和文件由核心 `/speckit.specify` 工作流创建。

## 用户输入

```text
$ARGUMENTS
```

如果用户输入非空，你必须在继续前考虑这些输入。

## 环境变量覆盖

如果用户明确提供了 `GIT_BRANCH_NAME`，例如通过环境变量、参数或请求文本提供，请在调用脚本前设置 `GIT_BRANCH_NAME` 环境变量并传递给脚本。设置 `GIT_BRANCH_NAME` 后：

- 脚本直接使用该值作为分支名，跳过全部前缀和后缀生成逻辑
- 忽略 `--short-name`、`--number` 和 `--timestamp` 标志
- 如果名称以数字前缀开头，从名称中提取 `FEATURE_NUM`；否则将完整分支名作为 `FEATURE_NUM`

## 前置条件

- 运行 `git rev-parse --is-inside-work-tree 2>/dev/null` 检查 Git 是否可用
- 如果 Git 不可用，警告用户并跳过分支创建

## 分支编号模式

按以下顺序判断分支编号策略：

1. 检查 `.specify/extensions/git/git-config.yml` 中的 `branch_numbering` 值
2. 检查 `.specify/init-options.json` 中的 `branch_numbering` 值，以保持向后兼容
3. 如果两处都不存在，默认使用 `sequential`

## 执行

为分支生成简短名称，长度为 2 到 4 个词：

- 分析功能描述，提取最有意义的关键词
- 尽量使用动作加名词格式，例如 `add-user-auth`、`fix-payment-bug`
- 保留技术术语和缩写，例如 OAuth2、API、JWT

根据当前平台运行对应脚本：

- **Bash**：`.specify/extensions/git/scripts/bash/create-new-feature.sh --json --short-name "<short-name>" "<feature description>"`
- **Bash（时间戳）**：`.specify/extensions/git/scripts/bash/create-new-feature.sh --json --timestamp --short-name "<short-name>" "<feature description>"`
- **PowerShell**：`.specify/extensions/git/scripts/powershell/create-new-feature.ps1 -Json -ShortName "<short-name>" "<feature description>"`
- **PowerShell（时间戳）**：`.specify/extensions/git/scripts/powershell/create-new-feature.ps1 -Json -Timestamp -ShortName "<short-name>" "<feature description>"`

**重要**：

- 不要传入 `--number`，脚本会自动判断下一个正确编号
- 始终包含 JSON 标志，Bash 使用 `--json`，PowerShell 使用 `-Json`，以便可靠解析输出
- 每个功能只能运行此脚本一次
- JSON 输出会包含 `BRANCH_NAME` 和 `FEATURE_NUM`

## 优雅降级

如果未安装 Git，或当前目录不是 Git 仓库：

- 跳过分支创建并警告：`[specify] Warning: Git repository not detected; skipped branch creation`
- 脚本仍输出 `BRANCH_NAME` 和 `FEATURE_NUM`，便于调用方引用

## 输出

脚本输出包含以下字段的 JSON：

- `BRANCH_NAME`：分支名，例如 `003-user-auth` 或 `20260319-143022-user-auth`
- `FEATURE_NUM`：使用的数字或时间戳前缀
