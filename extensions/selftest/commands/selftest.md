---
description: "验证扩展从目录到安装的生命周期"
---

# 扩展自检：`$ARGUMENTS`

此命令会驱动一次自检，模拟开发者使用 `$ARGUMENTS` 扩展的体验。

## 目标

验证扩展 `$ARGUMENTS` 的端到端生命周期，包括发现、安装和注册。
如果 `$ARGUMENTS` 为空，必须提示用户提供扩展名称，例如：`/speckit.selftest.extension linear`。

## 步骤

### 步骤 1：目录发现验证

检查该扩展是否存在于 Spec Kit 目录中。
执行以下命令，并确认命令成功完成且返回的扩展 ID 与 `$ARGUMENTS` 完全一致。如果命令失败或 ID 不匹配，则判定测试失败。

```bash
specify extension info "$ARGUMENTS"
```

### 步骤 2：模拟安装

首先尝试直接将扩展添加到当前工作区配置中。如果目录将该扩展标记为 `install_allowed: false`，即仅允许发现，则此步骤预期会失败。

```bash
specify extension add "$ARGUMENTS"
```

然后，通过目录中的下载 URL 模拟安装扩展；这种方式应绕过上述限制。
从目录元数据中获取扩展的 `download_url`，例如通过目录信息命令或界面获取，然后运行：

```bash
specify extension add "$ARGUMENTS" --from "<download_url>"
```

### 步骤 3：注册验证

`add` 命令完成后，通过检查项目配置来验证安装。
使用终端工具，例如 `cat`，确认以下文件包含 `$ARGUMENTS` 的记录。

```bash
cat .specify/extensions/.registry/$ARGUMENTS.json
```

### 步骤 4：验证报告

分析三个步骤的标准输出。
生成终端风格的测试输出，详细说明发现、安装和注册结果，并直接返回给用户。

示例输出格式：

```text
============================= test session starts ==============================
collected 3 items

test_selftest_discovery.py::test_catalog_search [PASS/FAIL]
  详情：[提供 specify extension search 的执行结果]

test_selftest_installation.py::test_extension_add [PASS/FAIL]
  详情：[提供 specify extension add 的执行结果]

test_selftest_registration.py::test_config_verification [PASS/FAIL]
  详情：[提供注册记录验证结果]

============================== [X] passed in ... ==============================
```
