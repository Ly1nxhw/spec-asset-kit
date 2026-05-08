# Spec Asset Kit 使用说明书

本文档是 `Spec Asset Kit` 的详细中文使用说明，面向两类读者：

- 第一次接触本项目的使用者
- 已经在团队或仓库中落地 SDD，希望系统理解工作流、目录结构、`ai-assets` 与扩展机制的维护者

如果你只想快速跑通一次，请先看 [quickstart.md](./quickstart.md)。  
如果你想完整理解本 fork 的设计与使用方式，请从本文开始。

## 1. 产品概览

### 1.1 它是什么

`Spec Asset Kit` 是基于 `spec-kit` fork 的增强版工具链，用来在 AI coding agent 场景下推进 Spec-Driven Development。

它保留上游核心主链：

1. `constitution`
2. `specify`
3. `plan`
4. `tasks`
5. `implement`

并在此基础上强化：

- 中文原生体验
- `ai-assets` 项目理解层
- brownfield 项目接入能力

### 1.2 它解决什么问题

在普通 SDD 流程中，AI 常见问题是：

- 只理解当前 feature，不理解整个项目
- 每次规划时重新猜目录结构与模块边界
- 项目术语、历史包袱、隐性约定很难稳定进入上下文
- 中文团队使用英文模板时，沟通成本偏高

这个 fork 的目标，就是把这些问题转化为稳定的工作流和项目资产，而不是靠每次 prompt 临时补充。

### 1.3 它不是什么

它不是：

- 一个完全重写的 `spec-kit`
- 一个新的流程哲学
- 一个替代源码和正式文档的知识库
- 一个已经完成全部知识治理能力的平台

## 2. 核心理念

### 2.1 SDD 主链不变

这个 fork 仍然坚持标准 SDD 主链：

`constitution -> specify -> plan -> tasks -> implement`

其中：

- `constitution` 定义长期原则和质量门槛
- `specify` 定义功能“做什么”和“为什么做”
- `plan` 定义技术规划和实现边界
- `tasks` 将规划拆为可执行任务
- `implement` 按任务推进实现

### 2.2 `ai-assets` 是项目理解层

`ai-assets` 的角色不是替代规范，而是帮助 AI 更稳定地回答这些问题：

- 这个项目是什么
- 这个仓库的结构是怎样的
- 这个团队有哪些术语与约定
- 哪些历史演进会影响当前规划

### 2.3 source of truth 规则

必须始终记住：

`ai-assets` 不是事实源本身。

当内容冲突时，优先级建议为：

1. 源码与运行行为
2. 正式契约与 schema
3. 配置与构建定义
4. `constitution`
5. `ai-assets`
6. `spec / plan / tasks` 中的推断性内容

## 3. 安装与初始化

### 3.1 安装方式

推荐使用 `uv`：

```bash
uv tool install specify-cli --from git+https://github.com/<your-org>/spec-asset-kit.git
```

安装完成后检查版本：

```bash
specify version
```

### 3.2 初始化项目

初始化一个新项目：

```bash
specify init <PROJECT_NAME> --integration codex --script sh
```

在当前目录初始化：

```bash
specify init --here --integration codex --script sh
```

### 3.3 常用参数

#### `--integration <name>`

指定 AI agent 集成，例如：

- `codex`
- `claude`
- `copilot`
- `generic`

#### `--script sh|ps`

指定脚本运行环境：

- `sh`：Bash / POSIX Shell
- `ps`：PowerShell

#### `--no-git`

跳过 git 初始化与 bundled git 扩展。

#### `--ignore-agent-tools`

跳过本地 agent CLI 可用性检查，适用于先初始化仓库、后补装工具。

### 3.4 初始化后会发生什么

`specify init` 完成后，通常会生成这些内容：

```text
.specify/
|- templates/
|- scripts/
|- memory/
|- integrations/
|- workflows/
|- extensions/
|  `- ai-assets/
|- extensions.yml
`- init-options.json

ai-assets/                  # 后续由 extractor 初始化/刷新

.agents/skills/ 或其他 agent 命令目录
```

其中最关键的是：

- `.specify/templates/`：核心文档模板
- `.specify/scripts/`：流程脚本
- `.specify/memory/constitution.md`：项目宪章
- `.specify/extensions/ai-assets/`：bundled 扩展
- `.specify/extensions.yml`：扩展钩子注册

## 4. 目录与文件解释

### 4.1 `.specify/`

这是项目运行时的核心工作目录。

主要职责：

- 保存模板
- 保存自动化脚本
- 保存当前工作流
- 保存 agent 集成信息
- 保存扩展和钩子配置

### 4.2 `specs/`

每个 feature 的规格文档通常放在这里。

典型结构：

```text
specs/003-user-auth/
|- spec.md
|- plan.md
|- tasks.md
|- research.md
|- data-model.md
|- quickstart.md
`- contracts/
```

### 4.3 `ai-assets/`

这是本 fork 最关键的新增目录之一，用来存放长期项目理解资产。

默认包含：

```text
ai-assets/
|- business-context.md
|- domain-glossary.md
|- business-rules.md
|- user-journeys.md
|- external-systems.md
|- decision-log.md
|- open-questions.md
`- extraction-report.md
```

### 4.4 `AGENTS.md` 或其他上下文文件

不同集成会把“请阅读当前 plan”的提示写进不同上下文文件中。

例如：

- `AGENTS.md`
- `CLAUDE.md`
- 其他集成专用上下文文件

这个机制的目的是让 agent 自动知道：在继续执行之前，应该读取当前计划文件。

## 5. 标准工作流

### 5.1 第一步：建立宪章

命令：

```text
/speckit.constitution
```

目标：

- 定义项目原则
- 定义工程约束
- 定义测试和质量规则
- 定义哪些模式必须优先、哪些模式应该避免

建议内容包括：

- TDD/测试要求
- 架构边界
- 命名与分层偏好
- 性能、安全、可维护性约束

### 5.2 第二步：定义功能规格

命令：

```text
/speckit.specify
```

这里的核心原则是：

- 写“做什么”
- 写“为什么做”
- 不要过早写“怎么做”

建议输入：

- 用户是谁
- 要解决什么问题
- 成功结果是什么
- 哪些边界很重要

### 5.3 第三步：生成或刷新 `ai-assets`

命令：

```text
/speckit.ai-assets.extract
```

虽然 `plan` 前会自动触发，但建议在 brownfield 仓库中先主动运行一次。

原因：

- 先把业务私有知识、领域术语、业务规则和用户旅程整理成候选线索
- 让后续 `plan` 和 `tasks` 阶段先理解业务，再选择实现路径
- 避免 agent 只重新罗列技术栈、架构和目录结构
- 把无法从 repo 直接确认的私有知识写入 `open-questions.md`，等待人工补充

如果 `open-questions.md` 中已有需要人工确认的问题，先补充业务答案，再运行：

```text
/speckit.ai-assets.refine
```

`refine` 会把人的明确回答沉淀为 `confirmed` 知识；没有确认的内容继续保留为 `candidate`。

### 5.4 第四步：生成技术规划

命令：

```text
/speckit.plan
```

在本 fork 中，`plan` 与上游最大的区别是：

- 规划前会检查 `before_plan` 钩子
- bundled `ai-assets` 扩展会强制先执行 extractor
- 规划时显式读取 `ai-assets`

最小消费要求是：

- 用 `business-context.md` 理解业务域、角色和目标
- 用 `domain-glossary.md` 稳定业务私有术语
- 用 `business-rules.md` 和 `user-journeys.md` 约束行为、状态和流程
- 用 `external-systems.md`、`decision-log.md` 补充上下游语义和历史决策
- 用 `open-questions.md` 识别还没有被人工确认的业务私有知识
- 只把 `confirmed` 当作规划事实；`candidate` 必须进入风险、待确认项或先通过 `refine` 确认

### 5.5 第五步：拆任务

命令：

```text
/speckit.tasks
```

这里会把 `plan.md` 拆成可执行任务。

好的任务应该具备：

- 真实文件路径
- 明确动作
- 按依赖排序
- 能支持分阶段实施

### 5.6 第六步：实施

命令：

```text
/speckit.implement
```

目标是按任务清单逐步落地，而不是一次性“把整个功能做完”。

推荐做法：

- 先完成最小闭环
- 每个阶段都做验证
- 完成后再补下一层能力

## 6. `ai-assets` 详解

### 6.1 `business-context.md`

用途：

- 解释业务域、目标用户、核心业务对象和系统存在的原因
- 说明系统在业务或组织中的定位，不展开技术架构

适合写入：

- 业务目标
- 用户/运营/维护者角色
- 核心业务对象
- 业务价值和非技术背景

### 6.2 `domain-glossary.md`

用途：

- 稳定业务私有术语
- 减少中英混用和词汇漂移

适合写入：

- 业务术语
- 缩写
- 中英映射
- 别名
- 过时术语
- 容易混淆的近义词和反例

### 6.3 `business-rules.md`

用途：

- 解释业务规则、状态流转、权限边界和例外处理

适合写入：

- 规则描述
- 适用场景
- 例外和边界
- 来源文件
- 简短实现锚点

### 6.4 `user-journeys.md`

用途：

- 帮助 AI 理解主要用户旅程和业务流程

适合写入：

- 参与者
- 触发条件
- 关键步骤
- 成功结果
- 异常/回滚路径
- 相关实现锚点

### 6.5 `external-systems.md`

用途：

- 解释上下游系统、外部平台、第三方服务、消息通道和人工运营环节

适合写入：

- 系统职责
- 交互语义
- 失败影响
- 数据边界
- 接口或配置来源

### 6.6 `decision-log.md`

用途：

- 记录业务决策、历史包袱和演进原因

适合写入：

- 历史决策
- 需求变化
- 产品/运营约束变化
- 仍影响新需求的历史包袱

### 6.7 `open-questions.md`

用途：

- 汇总所有需要人工确认的业务问题
- 说明每个问题为什么会影响后续规划、任务拆解或实现判断
- 作为 `/speckit.ai-assets.refine` 的主要输入队列

适合写入：

- 从 repo 命名、代码分支、注释或弱文档推断出来但无法确认的业务含义
- 需要产品、运营、业务研发或系统 owner 回答的问题
- 已回答但还没有完全整理进核心资产的知识

### 6.8 `extraction-report.md`

用途：

- 说明本次 extractor 看了什么
- 哪些结论可靠
- 哪些地方仍然不足

## 7. `ai-assets.extract` 的工作方式

### 7.1 命令

主命令：

```text
/speckit.ai-assets.extract
```

兼容别名：

```text
/speckit.assets.extract
```

### 7.2 抽取方式

当前采用混合式：

1. 轻量扫描脚本先提取仓库事实
2. 模板命令再基于这些事实生成候选资产和待确认问题

这比“全靠模型盲读整个仓库”更稳定，也比重型静态分析器更轻。

### 7.3 默认扫描来源

优先关注：

- `README*`
- `AGENTS.md`
- `docs/**`
- `specs/**`
- `CHANGELOG*`
- `CONTRIBUTING*`
- 接口契约、领域测试、产品说明和业务流程文档
- 顶层配置文件、入口文件、脚本、工作流只作为实现锚点补充

### 7.4 资产结构约束

除 `extraction-report.md` 外，每个核心资产都应区分：

```markdown
## 已确认知识

## 候选线索

## 实现锚点

## 待确认问题
```

不再建议使用 `[high]`、`[medium]`、`[low]` 平铺列表。更推荐使用 `confirmed`、`candidate`、`deprecated` 状态、知识卡片、表格和明确标题，把“含义、规则、场景、来源、实现锚点、待确认问题”分开写清楚。

状态含义：

- `confirmed`：来自正式文档、契约、测试，或人的明确确认
- `candidate`：来自 repo 线索的推断，仍需要人工确认
- `deprecated`：旧术语、旧流程或不应继续驱动新需求的历史知识

### 7.5 人工确认流程

`ai-assets.extract` 不应该假装能从 repo 里读出所有业务私有知识。更健康的流程是：

1. `/speckit.ai-assets.extract` 生成候选线索和 `open-questions.md`
2. 人补充业务答案、术语解释、规则边界或废弃说明
3. `/speckit.ai-assets.refine` 把明确回答升级为 `confirmed`
4. `/speckit.plan` 只把 `confirmed` 当事实，遇到 `candidate` 继续记录风险

### 7.6 漂移检查与实现后对齐

实现完成后，建议运行：

```text
/speckit.ai-assets.check
```

该命令严格只读，用于检查：

- 必需资产是否缺失
- 核心资产章节是否完整
- 实现锚点路径是否过期
- `confirmed` 条目是否缺少来源或锚点
- `candidate` 条目是否同步进入 `open-questions.md`
- plan 是否疑似把 `candidate` 当事实使用
- tasks 是否引用不存在路径

如果检查发现资产需要更新，或者本次实现改变了业务规则、术语、用户旅程、外部系统、历史决策或实现锚点，再运行：

```text
/speckit.ai-assets.reconcile
```

`reconcile` 只允许更新 `ai-assets/` 下的资产报告和待确认问题。它不得静默改写 `confirmed` 业务含义，也不得在没有人工确认、正式文档、契约或测试依据时把 `candidate` 升级为 `confirmed`。

## 8. `plan` 如何消费 `ai-assets`

在这个 fork 里，`plan` 不是单独看 `spec.md` 就开始推导。

正确做法是：

1. 看 `spec.md`
2. 看 `constitution.md`
3. 看 `ai-assets/business-context.md`
4. 看 `ai-assets/domain-glossary.md`
5. 看 `ai-assets/business-rules.md`
6. 看 `ai-assets/user-journeys.md`
7. 看 `ai-assets/open-questions.md`
8. 必要时看 `ai-assets/external-systems.md` 和 `ai-assets/decision-log.md`

这样做的好处：

- 业务术语不会乱
- 业务规则、状态流转和用户旅程更稳
- 技术规划不只围绕目录结构展开
- 能显式记录上下游约束和待确认业务问题
- 能避免把 `candidate` 推断内容误当成已确认事实

## 9. 扩展机制

### 9.1 什么是扩展

扩展用于给 Spec Kit 增加：

- 新命令
- 预处理/后处理钩子
- 模板覆盖
- 配置与集成行为

### 9.2 `ai-assets` 扩展做了什么

这个扩展当前提供：

- `speckit.ai-assets.extract`
- `speckit.assets.extract`
- `speckit.ai-assets.refine`
- `speckit.assets.refine`
- `speckit.ai-assets.check`
- `speckit.assets.check`
- `speckit.ai-assets.reconcile`
- `speckit.assets.reconcile`
- `before_plan` 强制钩子
- `plan` 命令模板覆盖
- `plan-template` 文档模板覆盖

### 9.3 为什么要用扩展而不是硬改主链

因为这样可以：

- 减少对核心 CLI 的侵入
- 保留与上游同步的可能性
- 让新增能力边界更清楚

## 10. 推荐使用方式

### 10.1 Greenfield 项目

建议顺序：

1. `specify init`
2. `/speckit.constitution`
3. `/speckit.specify`
4. `/speckit.plan`
5. `/speckit.tasks`
6. `/speckit.implement`

如果项目是新项目，`ai-assets` 的初始价值可能没有 brownfield 那么大，但依然有助于沉淀术语和结构。

### 10.2 Brownfield 项目

建议顺序：

1. `specify init --here`
2. `/speckit.ai-assets.extract`
3. 检查 `ai-assets/open-questions.md`
4. 补充业务答案后运行 `/speckit.ai-assets.refine`
5. `/speckit.constitution`
6. `/speckit.specify`
7. `/speckit.plan`
8. `/speckit.tasks`
9. `/speckit.implement`

这类项目里，最好先让 AI 理解项目，再让它写规划。

### 10.3 团队协作建议

建议把以下内容纳入团队约定：

- `constitution` 必须先建立
- `plan` 前必须确保 `ai-assets` 至少有一版可用
- `ai-assets` 只写业务知识沉淀和实现锚点，不替代源码和正式规范
- repo 推断只能作为 `candidate`，关键业务规则必须经过人工确认
- 如果项目出现明显漂移，后续再补资产冲突 reconcile 流程

## 11. 常见问题

### 11.1 为什么要这么多 Markdown 文档？

因为这里的 Markdown 不是“装饰性文档”，而是 AI 工作流中的结构化上下文层。

它们各自承担不同角色：

- `constitution`：长期原则
- `spec`：当前 feature 目标
- `plan`：技术设计与实现路径
- `tasks`：可执行任务
- `ai-assets`：项目级理解资产

关键不在“文档数量少”，而在“每类文档职责清晰、边界明确、彼此不互相污染”。

### 11.2 会不会造成上下文腐化？

会不会腐化，主要取决于两点：

1. 文档是否职责清楚
2. AI 是否有稳定的读取顺序

这个 fork 就是在解决这两个问题。

### 11.3 `ai-assets` 是否替代代码地图工具？

不能完全替代。

它更像“面向 AI 的业务知识工作台”，适合把领域术语、业务规则、用户旅程、上下游语义和待确认问题沉淀下来。代码路径只作为实现锚点存在，不替代 IDE、静态分析器或源码阅读本身。

### 11.4 为什么 `plan` 必须显式读 `ai-assets`？

因为如果不显式要求，AI 很容易只读当前 `spec.md`，然后在不了解真实项目结构的情况下生成脱离现实的规划。

### 11.5 当前版本还缺什么？

当前最明显的后续方向包括：

- 更完整的资产冲突 reconcile 流程
- 更稳定的 drift 检测
- 更好的人工校对 UI 或工作台
- 更丰富的 brownfield 抽取策略

## 12. 故障排查

### 12.1 初始化后没有 `ai-assets` 扩展

检查：

- `.specify/extensions/ai-assets/` 是否存在
- `.specify/extensions.yml` 是否存在
- `specify init` 是否成功执行

### 12.2 `plan` 没有消费 `ai-assets`

检查：

- 生成的 `speckit.plan` 命令文件中是否包含 `ai-assets/business-context.md`
- `.specify/templates/plan-template.md` 是否包含 `AI Assets 输入` 章节
- 扩展模板覆盖是否被正确安装

### 12.3 `ai-assets` 内容看起来不准

这是正常现象之一。

当前 Phase 2 目标是：

- 先产出“可用初稿”
- 不追求一次性达到完美知识治理水平

建议做法：

- 先保留高价值结论
- 用 `candidate` 和 `open-questions.md` 记录不确定项
- 用 `/speckit.ai-assets.refine` 消费人的明确回答
- 不要把推断内容当事实源

### 12.4 中文环境下会不会影响效果

相较于英文上游模板，这个 fork 默认中文化后通常更适合中文团队协作。  
真正决定效果的，仍然是：

- 模型能力
- 模板设计
- 资产质量
- 工作流约束是否稳定

## 13. 实践建议

### 13.1 不要追求一次性完美

尤其在 brownfield 项目里，`ai-assets` 第一版的目标是“先有可用初稿”，而不是一次完成全部知识治理。

### 13.2 优先稳定业务知识

如果资源有限，最优先维护：

1. `business-context.md`
2. `domain-glossary.md`
3. `business-rules.md`
4. `user-journeys.md`

因为这四类最直接影响后续规划是否理解业务意图，而不是只猜技术实现。

### 13.3 文档越像索引越有价值

对 AI 来说，最有用的文档通常不是最长的文档，而是：

- 有结构
- 可追溯
- 低冗余
- 能指回事实源

### 13.4 把 `ai-assets` 当作 harness engineering 的一部分

这个 fork 本质上是对模型能力的 harness engineering。

它不是在替模型思考，而是在：

- 给模型更稳定的输入
- 给模型更清晰的任务边界
- 给模型更少漂移、更高一致性的上下文

## 14. 后续文档入口

- 项目首页：[index.md](./index.md)
- 快速开始：[quickstart.md](./quickstart.md)
- 扩展参考：[reference/extensions.md](./reference/extensions.md)
- fork 改造蓝图：[../enhance/fork-enhancement-blueprint.zh-CN.md](../enhance/fork-enhancement-blueprint.zh-CN.md)
