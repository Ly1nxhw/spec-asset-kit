---
description: "Spec Kit 命令完成后自动提交变更"
---

# 自动提交变更

在 Spec Kit 命令完成后，自动暂存并提交所有变更。

## 行为

此命令会作为核心命令前后触发的钩子调用。它会：

1. 从钩子上下文判断事件名称，例如 `after_specify` 钩子对应事件 `after_specify`，`before_plan` 对应事件 `before_plan`
2. 读取 `.specify/extensions/git/git-config.yml` 中的 `auto_commit` 配置
3. 查找具体事件键，判断是否启用自动提交
4. 如果没有事件级配置，则回退到 `auto_commit.default`
5. 如果配置了事件级 `message`，使用该提交消息；否则使用默认消息
6. 如果已启用且存在未提交变更，运行 `git add .` 和 `git commit`

## 执行

根据触发此命令的钩子确定事件名称，然后运行脚本：

- **Bash**：`.specify/extensions/git/scripts/bash/auto-commit.sh <event_name>`
- **PowerShell**：`.specify/extensions/git/scripts/powershell/auto-commit.ps1 <event_name>`

将 `<event_name>` 替换为实际钩子事件，例如 `after_specify`、`before_plan`、`after_implement`。

## 配置

在 `.specify/extensions/git/git-config.yml` 中：

```yaml
auto_commit:
  default: false          # 全局开关，设为 true 可对所有命令启用
  after_specify:
    enabled: true          # 按命令覆盖
    message: "[Spec Kit] Add specification"
  after_plan:
    enabled: false
    message: "[Spec Kit] Add implementation plan"
```

## 优雅降级

- 如果 Git 不可用，或当前目录不是仓库：显示警告并跳过
- 如果配置文件不存在：跳过，默认禁用
- 如果没有可提交变更：显示消息并跳过
