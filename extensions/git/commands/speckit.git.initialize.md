---
description: "初始化 Git 仓库并创建初始提交"
---

# 初始化 Git 仓库

如果当前项目目录还不是 Git 仓库，则初始化一个 Git 仓库。

## 执行

从项目根目录运行对应脚本：

- **Bash**：`.specify/extensions/git/scripts/bash/initialize-repo.sh`
- **PowerShell**：`.specify/extensions/git/scripts/powershell/initialize-repo.ps1`

如果找不到扩展脚本，回退到：

- **Bash**：`git init && git add . && git commit -m "Initial commit from Specify template"`
- **PowerShell**：`git init; git add .; git commit -m "Initial commit from Specify template"`

脚本内部会处理全部检查：

- Git 不可用时跳过
- 已位于 Git 仓库内时跳过
- 运行 `git init`、`git add .` 和 `git commit`，并使用初始提交消息

## 自定义

可替换脚本以加入项目专用的 Git 初始化步骤：

- 自定义 `.gitignore` 模板
- 默认分支命名，例如 `git config init.defaultBranch`
- Git LFS 设置
- Git hooks 安装
- 提交签名配置
- Git Flow 初始化

## 输出

成功时：

- `Git repository initialized`

## 优雅降级

如果未安装 Git：

- 警告用户
- 跳过仓库初始化
- 项目仍可在没有 Git 的情况下工作，规格仍可创建在 `specs/` 下

如果已安装 Git，但 `git init`、`git add .` 或 `git commit` 失败：

- 向用户展示错误
- 停止此命令，避免继续使用部分初始化的仓库
