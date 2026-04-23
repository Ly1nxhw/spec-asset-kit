# Fork 改造实施方案 v0.1

## 1. 文档目的

本文定义基于 `spec-kit` fork 的增强版产品改造方案，用于指导后续在 fork 仓库中的实施、分工、验收与迭代。

本文目标是明确以下三件事：

1. 保留什么
2. 增强什么
3. 如何分阶段落地

## 2. 产品定位

### 2.1 定位陈述

该 fork 是一个基于 `spec-kit` 的增强版 SDD 工作流系统，面向中文开发环境、brownfield 项目接入和长期项目上下文治理场景。

### 2.2 产品核心价值

相对于原始 `spec-kit`，本 fork 强化三点：

- 中文原生体验
- `ai-assets` 项目理解层
- TDD 驱动的 QA 主线

### 2.3 非目标

本 fork 当前阶段不追求：

- 全量重写 `spec-kit`
- 自建全新流程哲学
- 覆盖所有 AI agent 集成
- 一次性构建完整生态系统
- 完整替代源码、接口文档、正式规范

## 3. 设计原则

### 3.1 保留 SDD 标准主链路

主工作流保持不变：

1. `constitution`
2. `spec`
3. `plan`
4. `tasks`
5. `implement`

### 3.2 中文原生优先

默认输出语言、模板语言、命令说明、交互提示优先采用中文。

### 3.3 ai-assets 一等公民

`ai-assets` 不是外挂说明，而是帮助 AI 理解项目的长期总结性资产层。

### 3.4 TDD 不是建议，而是主线 QA 约束

TDD 要在 `constitution / plan / tasks / implement` 中被显式制度化。

### 3.5 summary over copy

`ai-assets` 必须是提炼，不是全文搬运。

### 3.6 单一事实源优先

当 `ai-assets` 与代码、契约、配置冲突时，以正式事实源优先。

### 3.7 尽量最小侵入 fork

能通过模板、命令、扩展层完成的，不优先改 CLI 核心。

## 4. 核心产品模型

### 4.1 三层结构

系统拆分为三层：

- `Core Workflow Layer`
- `AI Assets Layer`
- `QA/TDD Enforcement Layer`

### 4.2 各层职责

| 层 | 职责 |
|---|---|
| Core Workflow Layer | 提供 `constitution -> spec -> plan -> tasks -> implement` 主流程 |
| AI Assets Layer | 提供项目长期理解：架构、术语、代码地图、约定、演进线索 |
| QA/TDD Enforcement Layer | 提供测试优先、回归验证、验收追踪、实现后对齐 |

### 4.3 核心关系

- `spec-kit` 负责“当前 feature 怎么推进”
- `ai-assets` 负责“这个项目是什么”
- `TDD/QA` 负责“结果怎么保证质量”

## 5. ai-assets 定义

### 5.1 定义

`ai-assets` 是从项目代码、文档、配置、历史记录中提炼出的项目级总结性资产，用于帮助 AI 在多个任务、多个阶段中稳定理解项目。

### 5.2 ai-assets 不是

- 不是源码副本
- 不是 ADR 全量替代
- 不是 feature 文档
- 不是正式 API 契约
- 不是最终事实源

### 5.3 ai-assets 必须满足

- 总结性
- 可追溯
- 可更新
- 低冗余
- 可按需加载

## 6. ai-assets 最小集合

建议第一版固定 6 类资产。

### 6.1 `ai-assets/project-overview.md`

内容包括：

- 项目目标
- 主要用户/贡献者
- 核心技术栈
- 系统运行形态
- 当前仓库在全系统中的角色
- 高层边界说明

### 6.2 `ai-assets/glossary.md`

内容包括：

- 项目术语
- 中英映射
- 别名
- 禁用词/弃用词
- 缩写解释
- canonical term

### 6.3 `ai-assets/architecture.md`

内容包括：

- 核心模块
- 边界关系
- 主要依赖方向
- 关键入口
- 主要数据流/调用流
- 观察与推断分层

### 6.4 `ai-assets/repo-map.md`

内容包括：

- 顶层目录职责
- 关键文件
- 关键脚本
- 关键配置
- 构建/运行/测试入口
- 重要生成物路径

### 6.5 `ai-assets/conventions.md`

内容包括：

- 隐性编码约定
- 文档约定
- 命名偏好
- 分层偏好
- 不鼓励的模式
- 项目特有“默认做法”

### 6.6 `ai-assets/evolution-log.md`

内容包括：

- 重要演进节点
- 历史重构线索
- 迁移路径
- 已知遗留包袱
- 当前演进方向

## 7. source of truth 规则

必须显式定义冲突优先级。

### 7.1 优先级顺序

1. 源码与运行行为
2. 正式契约与 schema
3. 配置文件与构建定义
4. constitution
5. ai-assets
6. spec / plan / tasks 中的推断性内容

### 7.2 使用规则

- `ai-assets` 负责解释，不负责替代正式定义
- 出现冲突时，必须记录到 `reconcile` 流程中
- 不允许 silently 覆盖事实源

## 8. 中文原生设计方案

### 8.1 语言策略

采用“内容中文，标识稳定”策略。

### 8.2 中文化范围

中文化范围包括：

- 命令说明
- 模板正文
- 交互提示
- 产出总结
- 质量检查说明
- 文档帮助信息

### 8.3 保持兼容的内容

以下内容尽量保持稳定和兼容：

- 文件名：`constitution.md`, `spec.md`, `plan.md`, `tasks.md`
- 分支名
- feature slug
- 路径名
- 代码标识符
- CLI 内部关键参数

### 8.4 双语桥接位置

双语桥接主要放在：

- `glossary.md`
- `project-overview.md`
- `architecture.md`

## 9. 工作流改造策略

### 9.1 保留主流程

主流程不增加新的顶层阶段。

### 9.2 ai-assets 的嵌入方式

`ai-assets` 作为贯穿式依赖进入每个阶段，而不是新增成 `phase 0`。

### 9.3 各阶段责任变化

#### `constitution`

输入：

- `project-overview`
- `conventions`
- `evolution-log`

目标：

- 提炼长期原则
- 把项目级隐性约束制度化
- 引入中文环境和 TDD 质量原则

#### `spec`

输入：

- `project-overview`
- `glossary`
- `repo-map`

目标：

- 让需求描述与项目语义对齐
- 避免术语漂移
- 避免 feature 定义脱离现有系统边界

#### `plan`

输入：

- `spec`
- `architecture`
- `repo-map`
- `conventions`

目标：

- 在真实结构上做技术规划
- 显式考虑兼容性、迁移影响、项目边界

#### `tasks`

输入：

- `plan`
- `repo-map`
- `architecture`

目标：

- 任务必须落到真实路径
- 测试任务必须前置
- 确保每个故事都可验证

#### `implement`

输入：

- `tasks`
- `conventions`
- `architecture`

目标：

- 先测后写
- 完成后回写 `ai-assets`
- 做 drift 对齐

## 10. TDD / QA 改造方案

### 10.1 总体要求

TDD 作为本 fork 的默认 QA 主线。

### 10.2 制度化落点

#### 在 `constitution`

加入强约束：

- 行为改动必须有验证方案
- 优先自动化测试
- 回归验证不可省略
- 测试不能长期滞后于实现

#### 在 `spec`

要求：

- 每个用户故事都要有可独立验证场景
- 验收条件必须可测试
- 不接受纯口号式成功标准

#### 在 `plan`

要求：

- 必须有测试策略字段
- 必须说明测试层次：单测、集成、回归、人工验证
- 必须说明不能自动化时的理由

#### 在 `tasks`

要求：

- 默认先列测试任务
- 每个用户故事阶段必须有验证任务
- 不再把测试标记为“可选”

#### 在 `implement`

要求：

- 先红后绿
- 变更后执行相关回归
- 最终生成验证结果摘要

### 10.3 分层 QA 模型

建议形成以下 QA 层级：

- `spec QA`
- `plan QA`
- `task QA`
- `implementation QA`
- `asset reconcile QA`

## 11. 命令与能力规划

### 11.1 保留命令

保留原始核心命令概念：

- `constitution`
- `specify`
- `plan`
- `tasks`
- `implement`
- `analyze`
- `clarify`
- `checklist`

### 11.2 新增命令

MVP 建议新增 2 个命令：

- `assets.extract`
- `assets.reconcile`

### 11.3 命令职责

#### `assets.extract`

职责：

- 扫描仓库
- 抽取项目理解信息
- 初始化或刷新 `ai-assets`
- 生成提取报告

#### `assets.reconcile`

职责：

- 在实现或规划后检查 `ai-assets` 是否过期
- 回写新增术语、结构变化、约定变化、演进节点
- 产出 reconcile 报告

### 11.4 命令嵌入建议

推荐嵌入方式：

- `specify` 前检查 `ai-assets` 是否存在
- `plan` 时强依赖 `ai-assets`
- `implement` 后建议运行 `assets.reconcile`

## 12. ai-asset-extractor 设计要求

### 12.1 定位

`ai-asset-extractor` 是 `ai-assets` 的初始化和刷新能力，不是完整知识治理系统。

### 12.2 输入源优先级

优先读取：

- `README*`
- `AGENTS.md`
- `docs/**`
- `CHANGELOG*`
- `CONTRIBUTING*`
- 顶层配置文件
- 顶层目录结构
- 关键源码入口
- 关键脚本
- workflow/模板资产

### 12.3 输出内容

输出：

- 6 类 `ai-assets`
- `ai-assets/extraction-report.md`

### 12.4 置信度机制

每条重要结论建议带置信度：

- `high`
- `medium`
- `low`

### 12.5 观察与推断分离

所有资产中必须区分：

- `Observed`
- `Inferred`
- `Open Questions`

## 13. fork 仓库结构改造建议

### 13.1 目标结构

建议在 fork 中逐步形成以下结构：

```text
spec-kit-fork/
|-- templates/
|-- src/specify_cli/
|-- extensions/
|   `-- ai-assets/
|       |-- commands/
|       |-- scripts/
|       `-- templates/
|-- docs/
|   |-- zh/
|   `-- product/
`-- presets/
```

### 13.2 用户项目生成结构

用户项目建议形成：

```text
.specify/
ai-assets/
specs/
```

### 13.3 为什么 `ai-assets` 不放进 `.specify/`

原因：

- 它是项目长期资产，不只是 workflow 中间产物
- 它可能被多个流程与多个 agent 共享
- 它更像项目级知识层，而不是单一命令输出

## 14. 实施边界

### 14.1 第一阶段允许改动

优先改这些位置：

- `templates/commands/`
- `templates/*.md`
- `extensions/` 下新增 ai-assets 能力
- `docs/` 中文说明
- 少量 CLI 装配逻辑

### 14.2 第一阶段尽量不改

暂不优先改：

- 多 agent 集成底层结构
- 核心 CLI 架构
- 完整 extension 系统机制
- 所有 preset 体系
- 全生态兼容层

### 14.3 第二阶段再考虑

第二阶段再考虑：

- localized preset
- 默认中文 init 选项
- CLI 参数国际化
- 更强的资产 drift 检测
- 资产质量评分系统

## 15. 分阶段改造路线图

## Phase 1: 中文模板与命令层

目标：

- 主流程中文可用
- 保持 SDD 链路不变
- 先跑通基础体验

交付物：

- 中文版命令模板
- 中文版 spec/plan/tasks 模板
- 中文版 constitution 模板
- 中文帮助文档

验收标准：

- 中文需求输入可以自然生成中文 spec
- 中文 plan / tasks 输出可读且稳定
- 分支名/slug 仍可正常工作

## Phase 2: ai-assets MVP

目标：

- 建立 `ai-assets` 体系
- 接入 `assets.extract`

交付物：

- `ai-assets` 目录规范
- extractor 命令
- 6 个资产模板
- extraction report 模板

验收标准：

- 对 brownfield 仓库能生成可用的资产初稿
- plan 阶段可消费这些资产
- 术语与 repo-map 对规划有效

## Phase 3: TDD / QA 主线强化

目标：

- 让 TDD 真正进入默认工作流

交付物：

- TDD 强化后的 constitution 规则
- 强制测试优先的 tasks 模板
- implement 的验证输出
- analyze 的 QA 规则增强

验收标准：

- tasks 中默认前置测试任务
- 实现后必须有验证结论
- analyze 能识别缺失的测试覆盖与 drift

## Phase 4: 资产回写与闭环

目标：

- 完成 `assets.reconcile`
- 形成知识闭环

交付物：

- reconcile 命令
- drift 检测规则
- 资产回写模板

验收标准：

- feature 实现后能更新术语、架构、代码地图变化
- ai-assets 不再长期过期

## Phase 5: CLI 与产品化收口

目标：

- 把增强体验做成默认产品行为

交付物：

- fork 版产品说明
- init 默认选项
- 文档入口与用户引导
- 示例项目

验收标准：

- 新用户能从文档直接进入完整流程
- 中文环境体验完整闭环

## 16. MVP 验收标准

### 16.1 必须达成

- 中文需求可直接进入完整 SDD 流程
- 主工作流仍是 `constitution -> spec -> plan -> tasks -> implement`
- `plan` 和 `tasks` 显式利用 `ai-assets`
- TDD 作为默认 QA 主线
- `ai-assets` 可初始化、可读、可追溯

### 16.2 体验成功标准

- 中文用户不需要先把需求翻译成英语
- AI 对项目术语误解明显减少
- brownfield 项目规划更少脱离现实目录结构
- 任务更容易落到真实文件路径
- 实现后能回写项目理解

## 17. 主要风险与对策

### 17.1 风险：fork 漂移过大

对策：

- 优先模板层改动
- 控制 CLI 核心改动面
- 明确自有改动边界

### 17.2 风险：ai-assets 变成第二套事实源

对策：

- 明确 source of truth 规则
- 每个资产写来源
- 引入 reconcile 而不是强行覆盖

### 17.3 风险：中文化破坏兼容性

对策：

- 内容中文，标识稳定
- 文件名与 slug 尽量兼容 upstream
- 双语桥接放在 glossary，不放在路径规则里

### 17.4 风险：系统过重

对策：

- MVP 只做 6 个资产
- 只新增 2 个命令
- 不引入额外顶层阶段

### 17.5 风险：TDD 口号化

对策：

- 把 TDD 写入模板、规则、任务和实现输出
- 不把测试标记为“可选”

## 18. 版本策略建议

### 18.1 fork 产品版本

建议独立版本体系，例如：

- `0.1.0` 中文模板可用
- `0.2.0` ai-assets MVP
- `0.3.0` TDD/QA 主线强化
- `0.4.0` reconcile 闭环
- `1.0.0` 中文原生 AI 资产增强版稳定发布

### 18.2 与 upstream 的关系

建议保留对 upstream 的追踪说明：

- 继承自哪个 upstream tag
- 本 fork 改动面有哪些
- 哪些目录有意偏离 upstream

## 19. 推荐的第一轮实施顺序

建议先做以下顺序：

1. 中文化 `templates/commands/*.md`
2. 中文化 `templates/spec-template.md`
3. 中文化 `templates/plan-template.md`
4. 中文化 `templates/tasks-template.md`
5. 补 `constitution-template.md` 的 TDD 与 ai-assets 表达
6. 设计 `ai-assets/` 模板
7. 实现 `assets.extract`
8. 修改 `plan` 使其消费 `ai-assets`
9. 修改 `tasks` 使其消费 `repo-map / architecture`
10. 实现 `assets.reconcile`

## 20. 实施前需要确认的决策

在切换到 fork 仓库后，建议先确认以下事项：

1. fork 的正式名称是什么
2. 命令前缀是否继续使用 `speckit`
3. `ai-assets/` 是否放仓库根目录
4. 中文是默认唯一输出，还是支持中英切换
5. 第一版是否保留 upstream 原模板作为兼容副本
6. `assets.extract` 是做成 extension 还是直接并入核心命令集
7. 第一阶段是否只支持 Codex skill 模式

## 21. 结论

本 fork 的改造方向明确且可落地：

- 保留 `spec-kit` 的 SDD 标准骨架
- 强化中文原生体验
- 引入 `ai-assets` 作为项目长期理解层
- 以 TDD 作为默认 QA 主线
- 通过最小侵入的 fork 策略逐步增强，而不是全量推翻 upstream

下一步进入 fork 仓库后，建议直接开始做两件事：

1. 确定目录与命令边界
2. 拆解第一阶段实施任务

切换到 fork 仓库后，可以继续产出下一份文档：

**《Phase 1 实施规划与任务拆解》**

它会具体到：

- 先改哪些文件
- 每个文件改什么
- 哪些先不碰
- 第一周如何落地 MVP
