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
|- project-overview.md
|- glossary.md
|- architecture.md
|- repo-map.md
|- conventions.md
|- evolution-log.md
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

- 先把项目结构、术语和约定抽出来
- 让后续 `plan` 和 `tasks` 阶段更稳定

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

- 用 `glossary.md` 稳定术语
- 用 `repo-map.md` 和 `architecture.md` 校正结构假设
- 用 `conventions.md` 补充项目隐性规定

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

### 6.1 `project-overview.md`

用途：

- 解释项目目标和仓库角色
- 说明系统在业务或组织中的定位

适合写入：

- 项目目标
- 核心能力
- 用户或维护者类型
- 仓库在整体系统中的角色

### 6.2 `glossary.md`

用途：

- 稳定项目术语
- 减少中英混用和词汇漂移

适合写入：

- 项目术语
- 缩写
- 中英映射
- 别名
- 过时术语

### 6.3 `architecture.md`

用途：

- 归纳主要模块、边界、调用关系

适合写入：

- 核心模块
- 分层关系
- 关键入口
- 数据流和调用流

### 6.4 `repo-map.md`

用途：

- 帮助 AI 快速理解仓库结构

适合写入：

- 顶层目录职责
- 关键源码路径
- 关键脚本
- 工作流与模板位置
- 构建、测试、运行入口

### 6.5 `conventions.md`

用途：

- 把隐性规则显性化

适合写入：

- 命名偏好
- 测试约定
- 代码组织习惯
- 文档风格
- 不鼓励的模式

### 6.6 `evolution-log.md`

用途：

- 记录仓库演进线索

适合写入：

- 历史迁移
- 大型重构
- 遗留包袱
- 当前演进方向

### 6.7 `extraction-report.md`

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
2. 模板命令再基于这些事实生成资产

这比“全靠模型盲读整个仓库”更稳定，也比重型静态分析器更轻。

### 7.3 默认扫描来源

优先关注：

- `README*`
- `AGENTS.md`
- `docs/**`
- `CHANGELOG*`
- `CONTRIBUTING*`
- 顶层配置文件
- 顶层目录结构
- 关键入口文件
- 关键脚本
- 工作流和模板文件

### 7.4 资产结构约束

除 `extraction-report.md` 外，每个核心资产都应区分：

```markdown
## Observed

## Inferred

## Open Questions
```

并建议使用置信度标签：

- `[high]`
- `[medium]`
- `[low]`

## 8. `plan` 如何消费 `ai-assets`

在这个 fork 里，`plan` 不是单独看 `spec.md` 就开始推导。

正确做法是：

1. 看 `spec.md`
2. 看 `constitution.md`
3. 看 `ai-assets/glossary.md`
4. 看 `ai-assets/repo-map.md`
5. 看 `ai-assets/architecture.md`
6. 看 `ai-assets/conventions.md`

这样做的好处：

- 术语不会乱
- 目录假设更稳
- 技术规划更贴近真实仓库
- 能显式记录项目约束

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
3. 检查 `ai-assets/` 初稿
4. `/speckit.constitution`
5. `/speckit.specify`
6. `/speckit.plan`
7. `/speckit.tasks`
8. `/speckit.implement`

这类项目里，最好先让 AI 理解项目，再让它写规划。

### 10.3 团队协作建议

建议把以下内容纳入团队约定：

- `constitution` 必须先建立
- `plan` 前必须确保 `ai-assets` 至少有一版可用
- `ai-assets` 只写总结，不替代源码和正式规范
- 如果项目出现明显漂移，后续再补 `assets.reconcile`

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

它更像“面向 AI 的总结性代码地图”，适合帮助 AI 在开始规划前快速理解项目，而不是替代 IDE、静态分析器或源码阅读本身。

### 11.4 为什么 `plan` 必须显式读 `ai-assets`？

因为如果不显式要求，AI 很容易只读当前 `spec.md`，然后在不了解真实项目结构的情况下生成脱离现实的规划。

### 11.5 当前版本还缺什么？

当前最明显的后续方向包括：

- `assets.reconcile`
- 更稳定的 drift 检测
- 更好的人工校对流程
- 更丰富的 brownfield 抽取策略

## 12. 故障排查

### 12.1 初始化后没有 `ai-assets` 扩展

检查：

- `.specify/extensions/ai-assets/` 是否存在
- `.specify/extensions.yml` 是否存在
- `specify init` 是否成功执行

### 12.2 `plan` 没有消费 `ai-assets`

检查：

- 生成的 `speckit.plan` 命令文件中是否包含 `ai-assets/glossary.md`
- `.specify/templates/plan-template.md` 是否包含 `AI Assets 输入` 章节
- 扩展模板覆盖是否被正确安装

### 12.3 `ai-assets` 内容看起来不准

这是正常现象之一。

当前 Phase 2 目标是：

- 先产出“可用初稿”
- 不追求一次性达到完美知识治理水平

建议做法：

- 先保留高价值结论
- 用 `Open Questions` 记录不确定项
- 不要把低置信度内容当事实源

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

### 13.2 优先稳定术语和结构

如果资源有限，最优先维护：

1. `glossary.md`
2. `repo-map.md`
3. `architecture.md`
4. `conventions.md`

因为这四类最直接影响后续规划和实施质量。

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
