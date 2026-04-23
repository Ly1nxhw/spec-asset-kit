# Phase 1 实施规划与任务拆解

## 1. 文档目的

本文定义 fork 改造蓝图的 `Phase 1` 实施方案，目标是在不破坏 `spec-kit`
现有 SDD 主链路的前提下，完成第一阶段的中文原生化改造，并为后续
`ai-assets` 与 TDD 强化打下稳定基础。

本文回答四个问题：

1. Phase 1 要交付什么
2. Phase 1 改哪些文件
3. Phase 1 先做什么，后做什么
4. Phase 1 如何验收

## 2. Phase 1 目标

### 2.1 核心目标

Phase 1 只做一件大事：让现有 `constitution -> spec -> plan -> tasks -> implement`
主工作流具备中文原生使用能力。

### 2.2 本阶段必须达成

- 命令模板默认以中文表述
- 产出模板默认以中文表述
- 中文用户可以直接输入需求，不需要先翻译成英文
- 保留现有文件命名、slug、路径规则与大部分 CLI 兼容性
- 不在本阶段引入新的顶层 workflow 阶段

### 2.3 本阶段不做

- 不实现完整 `ai-assets` 提取器
- 不引入 `assets.extract` / `assets.reconcile`
- 不大改 `src/specify_cli/` 核心结构
- 不重做扩展系统
- 不处理完整多语言切换
- 不实现全量产品化文档站改造

## 3. 改造策略

### 3.1 原则

本阶段遵循“三改三不改”。

三改：

- 改命令提示模板
- 改文档产物模板
- 改中文帮助文档入口

三不改：

- 不改主 workflow 顺序
- 不改路径与文件命名约定
- 不改底层核心 CLI 架构

### 3.2 技术路径

优先通过模板层完成改造：

1. `templates/commands/*.md`
2. `templates/*.md`
3. 必要时补充 `docs/product/` 文档

只有当模板层无法表达需求时，才进入 `src/specify_cli/`。

## 4. Phase 1 交付物

本阶段最终交付以下内容：

### 4.1 中文命令模板

至少覆盖以下核心命令：

- `constitution`
- `specify`
- `plan`
- `tasks`
- `implement`
- `analyze`
- `clarify`

### 4.2 中文产物模板

至少覆盖以下模板：

- `constitution-template.md`
- `spec-template.md`
- `plan-template.md`
- `tasks-template.md`

### 4.3 配套产品文档

新增或维护以下文档：

- fork 改造蓝图
- Phase 1 实施规划
- 如有必要，补一份中文 quickstart 或 migration note

## 5. 文件改动范围

## 5.1 最高优先级文件

### 命令模板

- `templates/commands/constitution.md`
- `templates/commands/specify.md`
- `templates/commands/plan.md`
- `templates/commands/tasks.md`
- `templates/commands/implement.md`
- `templates/commands/analyze.md`
- `templates/commands/clarify.md`

### 产物模板

- `templates/constitution-template.md`
- `templates/spec-template.md`
- `templates/plan-template.md`
- `templates/tasks-template.md`

## 5.2 次优先级文件

- `docs/index.md`
- `docs/quickstart.md`
- `README.md`
- 与中文默认体验直接相关的引导文档

## 5.3 本阶段不碰的文件

- `src/specify_cli/agents.py`
- `src/specify_cli/extensions.py`
- 多 agent integration 实现目录
- 扩展 catalog 与 preset catalog
- 大部分 workflow engine 内核

## 6. 任务拆解

## Task Group A: 语言策略定稿

### A1. 明确中文化边界

输出结论：

- 正文中文
- 文件名不变
- slug 保持 ASCII
- 命令 id 保持兼容

验收标准：

- 团队对“内容中文，标识稳定”无歧义

### A2. 明确术语基线

需要统一以下术语中文表达：

- Constitution
- Feature Specification
- Implementation Plan
- Tasks
- Acceptance Scenarios
- Success Criteria
- Assumptions
- Edge Cases
- Clarifications
- Constitution Check

验收标准：

- 后续模板中同一术语不出现多种中文译法

## Task Group B: 产物模板中文化

### B1. 改造 `constitution-template.md`

目标：

- 把标题、说明、占位示例改成中文
- 保留版本、日期、治理结构
- 显式引入中文环境和 TDD/质量导向表达

重点检查：

- 占位符仍可被后续命令替换
- 版本信息格式不变

### B2. 改造 `spec-template.md`

目标：

- 保持结构不变
- 中文化用户故事、边界条件、需求、成功标准、假设
- 让中文产出自然，不带英语腔

重点检查：

- “独立可测试”表达清晰
- 验收场景中文表述稳定

### B3. 改造 `plan-template.md`

目标：

- 中文化技术上下文、项目结构、复杂度追踪
- 保留现有字段与 SDD 逻辑
- 为后续 `ai-assets` 接入预留表达空间

重点检查：

- 结构和字段名兼容现有命令逻辑
- 不在本阶段引入新的强依赖字段

### B4. 改造 `tasks-template.md`

目标：

- 中文化任务说明
- 保留严格 checklist 格式
- 把测试与验证描述写得更明确

重点检查：

- 任务格式不被中文化破坏
- `[US1]`、`[P]`、`T001` 等保持原样

## Task Group C: 命令模板中文化

### C1. 改造 `constitution` 命令模板

目标：

- 将说明、执行步骤、总结输出全部中文化
- 保留 hook 机制说明
- 保留模板替换与同步检查逻辑

### C2. 改造 `specify` 命令模板

目标：

- 支持中文需求输入作为默认场景
- 输出中文 spec
- 保留 branch/slug/path 规则

重点风险：

- 英文示例中的 “2-4 words short name” 规则需要重写成对中文输入友好的 slug 生成描述

### C3. 改造 `plan` 命令模板

目标：

- 中文化 Phase 0/1 的说明
- 明确产物是中文
- 保持路径、脚本、artifact 规则不变

### C4. 改造 `tasks` 命令模板

目标：

- 中文化任务生成说明
- 保留严格格式检查
- 让中文描述仍然能映射到真实路径与任务动作

### C5. 改造 `implement` 命令模板

目标：

- 中文化执行说明
- 为后续 TDD 强化留接口
- 当前阶段不重写实现逻辑，只改表述和验证要求

### C6. 改造 `analyze` 与 `clarify`

目标：

- 中文化分析报告结构
- 中文化澄清问题逻辑
- 保留对缺失、冲突、模糊项的严格检查

## Task Group D: 文档入口整理

### D1. 在 `docs/product/` 下维护产品文档

至少包括：

- `fork-enhancement-blueprint.zh-CN.md`
- `phase-1-implementation-plan.zh-CN.md`

### D2. 评估是否补中文 quickstart

本任务不是立即重写 `docs/quickstart.md`，而是做判断：

- 是否需要单独新增中文 quickstart
- 是否在 Phase 1 末尾补一版最小中文入口文档

## 7. 推荐实施顺序

建议严格按以下顺序执行。

### Step 1

统一中文术语表与语言策略。

### Step 2

先改 `templates/*.md`，把产物模板跑顺。

顺序建议：

1. `spec-template.md`
2. `plan-template.md`
3. `tasks-template.md`
4. `constitution-template.md`

原因：

- `spec/plan/tasks` 是主路径高频产物
- `constitution` 虽重要，但使用频次低于前三者

### Step 3

再改 `templates/commands/*.md`。

顺序建议：

1. `specify.md`
2. `plan.md`
3. `tasks.md`
4. `implement.md`
5. `constitution.md`
6. `clarify.md`
7. `analyze.md`

### Step 4

补 `docs/product/` 文档与必要说明。

### Step 5

做一次端到端人工验证：

- 中文 constitution
- 中文 spec
- 中文 plan
- 中文 tasks

确认整个主链路可读、可用、不中断。

## 8. 依赖关系

### 8.1 模板依赖

- `specify.md` 依赖 `spec-template.md`
- `plan.md` 依赖 `plan-template.md`
- `tasks.md` 依赖 `tasks-template.md`
- `constitution.md` 依赖 `constitution-template.md`

因此，产物模板必须先于命令模板定稿。

### 8.2 文档依赖

- `docs/product/` 文档依赖 Phase 1 方案收敛
- quickstart 是否改造依赖主链路中文化验证结果

## 9. 验收方案

## 9.1 功能验收

使用中文输入完成以下链路验证：

1. 运行 `constitution`
2. 运行 `specify`
3. 运行 `plan`
4. 运行 `tasks`

预期结果：

- 产物主体为中文
- 文件名与路径仍兼容
- 任务格式未损坏

## 9.2 质量验收

检查以下点：

- 是否仍有大量英文说明残留在主路径模板中
- 中文是否自然，而不是英文句式直译
- task checklist 格式是否仍严格可执行
- slug、branch、feature directory 规则是否还能正常工作

## 9.3 兼容性验收

检查以下点：

- 路径名不因中文化失效
- 命令引用模板路径不变
- JSON / script / hook 说明未被中文化误伤

## 10. 风险与缓解

### 10.1 风险：中文化只改表面，不改默认行为

表现：

- 模板中文了，但生成内容仍大量偏英文

缓解：

- 命令模板明确要求默认中文输出
- 示例全部改成中文场景

### 10.2 风险：任务格式被自然语言改坏

表现：

- 中文化后 `T001 / [P] / [US1]` 格式漂移

缓解：

- 在 `tasks.md` 命令与模板中反复强调格式不变
- 在验收时做专门格式检查

### 10.3 风险：路径和 slug 规则被中文语义污染

表现：

- 中文 feature name 直接进入目录名或 branch

缓解：

- 明确保留 ASCII slug 规则
- 中文仅用于内容，不用于底层路径键值

### 10.4 风险：过早触碰 CLI 核心

表现：

- Phase 1 规模失控

缓解：

- 未证明模板层不够前，不进入 `src/specify_cli/`

## 11. Done 定义

Phase 1 完成的标准：

- 核心四类模板已中文化
- 核心七类命令模板已中文化
- `docs/product/` 下已有蓝图与实施文档
- 端到端主链路可以以中文场景运行
- 未引入新的顶层 workflow 阶段
- 未对 CLI 内核做不必要重构

## 12. Phase 1 完成后的下一步

Phase 1 完成后，立刻进入 `Phase 2: ai-assets MVP`。

届时重点将转向：

- `ai-assets/` 目录规范
- `assets.extract`
- `project-overview / glossary / architecture / repo-map` 初始模板
- `plan` 对 `ai-assets` 的显式消费

## 13. 建议的第一周执行切片

如果按一周切片推进，建议：

### Day 1

- 定稿语言策略
- 定稿术语表

### Day 2

- 改 `spec-template.md`
- 改 `plan-template.md`

### Day 3

- 改 `tasks-template.md`
- 改 `constitution-template.md`

### Day 4

- 改 `specify.md`
- 改 `plan.md`
- 改 `tasks.md`

### Day 5

- 改 `implement.md`
- 改 `clarify.md`
- 改 `analyze.md`

### Day 6

- 端到端手工验证
- 修正术语不一致与格式问题

### Day 7

- 收口文档
- 准备 Phase 2 设计输入
