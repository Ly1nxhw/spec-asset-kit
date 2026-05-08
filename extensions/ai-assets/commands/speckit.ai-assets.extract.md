---
description: 从仓库线索中初始化或刷新 ai-assets 候选业务知识与待确认问题。
scripts:
  sh: .specify/extensions/ai-assets/scripts/bash/extract-ai-assets.sh --json
  ps: .specify/extensions/ai-assets/scripts/powershell/extract-ai-assets.ps1 -Json
---

## 用户输入

```text
$ARGUMENTS
```

如果用户输入非空，请把它当作本次提取的附加关注点，但不要偏离仓库事实。不要把用户未确认的业务解释写成已确认知识。

## 执行纲要

1. 在仓库根目录运行 `{SCRIPT}`，获取当前仓库的扫描 JSON。扫描结果只用于定位可读来源和业务线索，不要把扫描到的目录结构机械改写成资产正文。
2. 基于扫描结果，优先读取能暴露业务线索的来源文件，例如 `README*`、`AGENTS.md`、`docs/**`、`specs/**`、`CHANGELOG*`、`CONTRIBUTING*`、业务流程文档、产品说明、接口契约和领域相关测试。配置文件、工作流、模板文件只作为补充来源。
3. 先判断每条知识的状态：
   - `confirmed`：来源是正式业务文档、规格、契约、测试，或用户在本次输入中明确确认。
   - `candidate`：只从命名、目录、代码分支、注释或弱文档中推断出来，需要人工确认。
   - `deprecated`：来源显示这是旧术语、旧流程或不应继续使用的知识。
4. 在仓库根目录创建或刷新 `ai-assets/`，生成以下文件：
   - `ai-assets/business-context.md`
   - `ai-assets/domain-glossary.md`
   - `ai-assets/business-rules.md`
   - `ai-assets/user-journeys.md`
   - `ai-assets/external-systems.md`
   - `ai-assets/decision-log.md`
   - `ai-assets/open-questions.md`
   - `ai-assets/extraction-report.md`

## 写作规则

- 资产目标是沉淀业务私有知识，而不是重新生成一份架构说明、技术栈说明或目录说明。
- `extract` 阶段默认只能可靠地产出 repo 线索、候选知识和待确认问题；除非来源明确，否则不要把业务解释写成 `confirmed`。
- 所有结论优先来自业务文档、规格、接口契约、测试用例、README、宪章、AGENTS、领域代码命名和正式文档。
- `ai-assets/` 只能提炼和组织事实，不能替代源码、配置、契约或正式文档的 source of truth 地位。
- 不要把猜测写成事实。无法直接验证的内容必须标记为 `candidate`，并同步写入 `open-questions.md`。
- 不再使用 `[high]`、`[medium]`、`[low]` 平铺列表。改用清晰标题、表格、知识卡片和“来源”字段组织内容。
- 尽量引用具体文件路径，方便后续规划阶段回溯。
- 如果仓库事实不足，不要强行补完，直接记录缺口。
- 技术栈、目录结构、模块边界、运行命令只在“实现锚点”中简要列出，且必须服务于业务知识解释；不要展开成完整架构文档。

## 每个资产的固定结构

除 `open-questions.md` 与 `extraction-report.md` 外，每个资产文件都必须包含以下四个二级标题，且顺序固定：

```markdown
## 已确认知识

## 候选线索

## 实现锚点

## 待确认问题
```

建议使用如下知识卡片或表格格式：

```markdown
### 业务概念：<名称>

| 项 | 内容 |
|---|---|
| 含义 | <用业务语言解释，不写技术实现> |
| 触发场景 | <用户/运营/系统何时会遇到它> |
| 关键规则 | <限制、状态、权限、边界> |
| 状态 | confirmed / candidate / deprecated |
| 来源 | `docs/example.md`, `tests/example_test.py` |
| 实现锚点 | `src/example/...`（仅列路径，不展开架构） |
| 待确认 | <如果是 candidate，写清楚需要问人的问题> |
```

`open-questions.md` 使用如下格式：

```markdown
## 待人工确认

| ID | 问题 | 为什么重要 | 线索来源 | 影响资产 |
|---|---|---|---|---|
| AQ001 | <需要业务方回答的问题> | <影响 plan/tasks 的原因> | `path/to/source` | `business-rules.md` |

## 已回答待整理

## 本次无足够线索
```

## 各资产目标

### `business-context.md`

- 解释项目服务的业务域、目标用户、核心业务对象、业务价值和非技术背景
- 回答“这个系统为什么存在、帮谁解决什么问题”
- 不要展开技术架构、目录结构或依赖清单
- 如果只能从 repo 命名推断业务域，必须写入候选线索并进入 `open-questions.md`

### `domain-glossary.md`

- 收集业务专用名词、内部黑话、缩写、中英映射、过时说法和容易混淆的近义词
- 每个术语必须解释业务含义、使用场景、反例或混淆点
- 技术缩写只有在承载业务语义时才记录

### `business-rules.md`

- 归纳业务规则、状态流转、权限边界、数据约束、合规/运营规则和例外处理
- 优先从测试、接口契约、产品文档和代码条件分支中提炼
- 用表格表达“规则/适用场景/例外/来源/实现锚点”

### `user-journeys.md`

- 解释主要用户旅程、业务流程、系统间流转和失败/回滚场景
- 用步骤列表或流程表描述“参与者 -> 触发 -> 关键动作 -> 结果”
- 只在实现锚点中简要列出相关入口文件

### `external-systems.md`

- 解释上下游系统、外部服务、第三方平台、消息通道、人工运营环节和数据交互边界
- 重点记录业务职责、交互语义、失败影响和不可替代的私有上下文
- 不要变成接口清单；接口路径只作为来源或实现锚点

### `decision-log.md`

- 从 changelog、文档历史、注释、测试变化和规格中提炼业务决策与演进原因
- 重点回答“为什么现在这样做”“哪些历史包袱影响新需求”
- 无法确认原因时记录为待确认，不要杜撰

### `open-questions.md`

- 汇总所有需要人工确认的业务问题
- 每个问题都必须说明“为什么重要”和“影响哪些资产/规划决策”
- `speckit.ai-assets.refine` 会消费这里的问题和用户回答，把候选知识升级为已确认知识

### `extraction-report.md`

- 记录本次提取扫描了哪些来源
- 记录哪些资产来自业务事实，哪些仅有技术锚点
- 记录 confirmed/candidate/deprecated 的数量
- 记录尚未解决的缺口与建议人工补充点
- 记录没有写入完整资产的技术来源索引，供后续排查

## 完成标准

- `ai-assets/` 全部 8 个文件都已存在
- 6 类核心资产都包含 `已确认知识 / 候选线索 / 实现锚点 / 待确认问题`
- `open-questions.md` 汇总了所有 candidate 知识对应的人工确认问题
- `extraction-report.md` 说明了来源范围、主要结论和未决问题
- 输出结果明确提醒：后续 `speckit.plan` 只能把 `confirmed` 当事实；遇到 `candidate` 必须标记风险或先运行 `speckit.ai-assets.refine`
