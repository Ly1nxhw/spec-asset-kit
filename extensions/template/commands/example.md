---
description: "演示扩展功能的示例命令"
# 自定义：列出此命令使用的 MCP 工具
tools:
  - 'example-mcp-server/example_tool'
---

# 示例命令

<!-- 自定义：将整个文件替换为你的命令文档 -->

此示例命令用于演示如何为 Spec Kit 扩展创建命令。

## 用途

说明此命令执行什么操作，以及何时使用。

## 前置条件

列出使用此命令前需要满足的条件：

1. 前置条件 1，例如已配置 MCP server
2. 前置条件 2，例如配置文件已存在
3. 前置条件 3，例如 API 凭据有效

## 用户输入

$ARGUMENTS

## 步骤

### 步骤 1：加载配置

<!-- 自定义：替换为你的实际步骤 -->

从项目中加载扩展配置：

```bash
config_file=".specify/extensions/my-extension/my-extension-config.yml"

if [ ! -f "$config_file" ]; then
  echo "错误：未在 $config_file 找到配置"
  echo "运行 'specify extension add my-extension' 以安装并配置扩展"
  exit 1
fi

# 读取配置值

setting_value=$(yq eval '.settings.key' "$config_file")

# 应用环境变量覆盖

setting_value="${SPECKIT_MY_EXTENSION_KEY:-$setting_value}"

# 验证配置

if [ -z "$setting_value" ]; then
  echo "错误：配置值未设置"
  echo "编辑 $config_file 并设置 'settings.key'"
  exit 1
fi

echo "配置已加载：$setting_value"
```

### 步骤 2：执行主要动作

<!-- 自定义：替换为你的命令逻辑 -->

说明此步骤执行什么操作：

```markdown
使用 MCP 工具执行主要动作：

- 工具：example-mcp-server example_tool
- 参数：{ "key": "$setting_value" }

这会调用 MCP server 工具来执行操作。
```

### 步骤 3：处理结果

<!-- 自定义：按需添加更多步骤 -->

处理结果并提供输出：

```bash
echo ""
echo "命令已成功完成！"
echo ""
echo "结果："
echo "  - 项 1：值"
echo "  - 项 2：值"
echo ""
```

### 步骤 4：保存输出（可选）

如有需要，将结果保存到文件：

```bash
output_file=".specify/my-extension-output.json"

cat > "$output_file" <<EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "setting": "$setting_value",
  "results": []
}
EOF

echo "输出已保存到 $output_file"
```

## 配置参考

<!-- 自定义：记录配置选项 -->

此命令使用 `my-extension-config.yml` 中的以下配置：

- **settings.key**：说明此设置的作用
  - 类型：string
  - 必填：是
  - 示例：`"example-value"`

- **settings.another_key**：说明另一个设置
  - 类型：boolean
  - 必填：否
  - 默认值：`false`
  - 示例：`true`

## 环境变量

<!-- 自定义：记录环境变量覆盖项 -->

可使用环境变量覆盖配置：

- `SPECKIT_MY_EXTENSION_KEY`：覆盖 `settings.key`
- `SPECKIT_MY_EXTENSION_ANOTHER_KEY`：覆盖 `settings.another_key`

示例：

```bash
export SPECKIT_MY_EXTENSION_KEY="override-value"
```

## 故障排查

<!-- 自定义：添加常见问题和解决方案 -->

### “未找到配置”

**解决方案**：安装扩展并创建配置：

```bash
specify extension add my-extension
cp .specify/extensions/my-extension/config-template.yml \
   .specify/extensions/my-extension/my-extension-config.yml
```

### “MCP 工具不可用”

**解决方案**：确认已在 AI agent 设置中配置 MCP server。

### “权限被拒绝”

**解决方案**：检查外部服务中的凭据和权限。

## 备注

<!-- 自定义：添加有用说明和提示 -->

- 此命令需要可用的外部服务连接
- 结果会缓存以提升性能
- 重新运行命令可刷新数据

## 示例

<!-- 自定义：添加使用示例 -->

### 示例 1：基础用法

```bash
# 使用默认配置运行
> /speckit.my-extension.example
```

### 示例 2：使用环境变量覆盖

```bash
# 使用环境变量覆盖配置
export SPECKIT_MY_EXTENSION_KEY="custom-value"
> /speckit.my-extension.example
```

### 示例 3：在核心命令之后使用

```bash
# 作为工作流的一部分使用
> /speckit.tasks
> /speckit.my-extension.example
```

---

*更多信息请参阅扩展 README，或运行 `specify extension info my-extension`*
