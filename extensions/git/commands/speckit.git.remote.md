---
description: "检测 Git 远程 URL 以供 GitHub 集成使用"
---

# 检测 Git 远程 URL

检测 Git 远程 URL，以便与 GitHub 服务集成，例如创建 issue。

## 前置条件

- 运行 `git rev-parse --is-inside-work-tree 2>/dev/null` 检查 Git 是否可用
- 如果 Git 不可用，输出警告并返回空结果：
  ```
  [specify] Warning: Git repository not detected; cannot determine remote URL
  ```

## 执行

运行以下命令获取远程 URL：

```bash
git config --get remote.origin.url
```

## 输出

解析远程 URL 并判断：

1. **仓库 owner**：从 URL 中提取，例如从 `https://github.com/Ly1nxhw/spec-asset-kit.git` 提取 `Ly1nxhw`
2. **仓库名称**：从 URL 中提取，例如从 `https://github.com/Ly1nxhw/spec-asset-kit.git` 提取 `spec-asset-kit`
3. **是否为 GitHub**：判断远程是否指向 GitHub 仓库

支持的 URL 格式：

- HTTPS：`https://github.com/<owner>/<repo>.git`
- SSH：`git@github.com:<owner>/<repo>.git`

> [!CAUTION]
> 只有当远程 URL 确实指向 github.com 时，才报告为 GitHub 仓库。
> 如果 URL 格式不匹配，不要假设远程是 GitHub。

## 优雅降级

如果未安装 Git、目录不是 Git 仓库，或没有配置远程：

- 返回空结果
- 不要报错，其他工作流应能在没有 Git 远程信息的情况下继续
