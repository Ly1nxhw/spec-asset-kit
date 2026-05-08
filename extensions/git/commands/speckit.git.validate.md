---
description: "验证当前分支是否符合功能分支命名约定"
---

# 验证功能分支

验证当前 Git 分支是否符合预期的功能分支命名约定。

## 前置条件

- 运行 `git rev-parse --is-inside-work-tree 2>/dev/null` 检查 Git 是否可用
- 如果 Git 不可用，输出警告并跳过验证：
  ```
  [specify] Warning: Git repository not detected; skipped branch validation
  ```

## 验证规则

获取当前分支名：

```bash
git rev-parse --abbrev-ref HEAD
```

分支名必须匹配以下任一模式：

1. **顺序号**：`^[0-9]{3,}-`，例如 `001-feature-name`、`042-fix-bug`、`1000-big-feature`
2. **时间戳**：`^[0-9]{8}-[0-9]{6}-`，例如 `20260319-143022-feature-name`

## 执行

如果当前位于功能分支，即匹配任一模式：

- 输出：`On feature branch: <branch-name>`
- 检查 `specs/` 下是否存在对应的规格目录：
  - 对顺序号分支，查找 `specs/<prefix>-*`，其中 prefix 匹配数字部分
  - 对时间戳分支，查找 `specs/<prefix>-*`，其中 prefix 匹配 `YYYYMMDD-HHMMSS` 部分
- 如果规格目录存在：`Spec directory found: <path>`
- 如果规格目录缺失：`No spec directory found for prefix <prefix>`

如果当前不在功能分支：

- 输出：`Not on a feature branch. Current branch: <branch-name>`
- 输出：`Feature branches should be named like: 001-feature-name or 20260319-143022-feature-name`

## 优雅降级

如果未安装 Git，或目录不是 Git 仓库：

- 检查 `SPECIFY_FEATURE` 环境变量作为回退
- 如果已设置，则按命名模式验证该值
- 如果未设置，则显示警告并跳过验证
