# AI Assets 评测流程

本文定义 `Spec Asset Kit` 中 `ai-assets` 能力的完整测试与评估流程，用于回答一个核心问题：

> 在 brownfield 仓库中，引入 `ai-assets` 后，AI 生成的 `plan`、`tasks` 和后续实现是否更贴合真实项目。

评测重点不是证明 `ai-assets/` 能生成文件，而是证明它能降低规划幻觉、减少人工修正、提升任务可执行性。

## 落地边界

真正有说服力的 L2/L3/L4 量化验证应该在真实业务项目中执行，而不是只在 `spec-asset-kit` 自身执行。

推荐分工：

| 位置 | 职责 |
|---|---|
| `spec-asset-kit/evaluation/` | 维护评测方法、schema、rubric、聚合脚本、报告模板和 simulated smoke case |
| 真实业务项目 `.speckit-eval/` 或 `evaluation/` | 采集真实历史 feature replay 的 case、run、diff、judge 和 metrics |
| 回流材料 | 只回流脱敏后的 `results.csv`、`summary.json`、报告结论或可公开示例 |

因此，`spec-asset-kit` 中的 simulated case 只能证明流程可运行；是否存在稳定收益，必须由真实业务项目的历史 replay A/B 数据证明。

## 评测目标

### 北极星指标

历史真实 feature replay 中，AI 产出能否被判定为“可进入 PR review 并接近真实 feature 目标”。

可接受的提升目标：

- `plan/tasks` 一次通过率提升 20% 以上
- 幻觉路径、幻觉依赖、错误模块边界下降 30% 以上
- 人工必须修正问题数下降 30% 以上
- 任务可执行性评分提升 1 分以上，满分 5 分
- 实现阶段 review blocker、越界修改、人工修正时间低于 baseline

### 评测问题

本流程要回答：

1. `ai-assets.extract` 是否能从仓库事实中提炼出可追溯、可消费的项目理解资产。
2. `speckit.plan` 消费 `ai-assets` 后，是否更少误判目录、模块、技术栈、测试方式和项目术语。
3. `speckit.tasks` 是否能生成更贴近真实文件与实现路径的任务。
4. 后续实现阶段是否减少返工、越界修改和 review 问题。
5. 在真实历史 feature replay 中，B 组是否比 A 组更接近真实 feature 的行为意图与改动范围。

## 实验分组

至少保留 A/B 两组。若要排除中文模板影响，增加 C 组。

| 组别 | 配置 | 用途 |
|---|---|---|
| A: upstream baseline | 原生 `spec-kit`，不提供 `ai-assets` | 基线 |
| B: asset enhanced | `spec-asset-kit`，先运行 `speckit.ai-assets.extract`，再运行 `speckit.plan` | 验证 `ai-assets` 增益 |
| C: zh-only optional | 中文模板，但禁用 `ai-assets` | 区分中文化收益与资产收益 |

固定变量：

- 使用同一模型、同一模型版本、同一 temperature。
- 使用同一仓库快照、同一 feature 描述、同一 agent。
- 同一 case 至少重复 3 次，降低 LLM 随机性影响。
- 输出评审时隐藏组别，避免人工偏见。

核心防泄题规则：

- 执行开发的 agent 只能看到起始 commit、需求描述和常规项目上下文。
- 执行开发的 agent 不能看到真实 feature 分支 diff、最终代码或 gold notes。
- 真实 feature diff 只允许在裁判阶段使用。
- 裁判可以使用 gold reference，但必须允许“不同实现方式但业务正确”的结果。

## 评测层级

### L0: 工程回归测试

目标：保证工具链不坏。

已覆盖方向：

- bundled `ai-assets` 扩展可以安装
- `before_plan` hook 可以注册
- scanner 可以输出 JSON
- Bash 与 PowerShell scanner 输出一致
- `plan` 模板覆盖会优先选择 `ai-assets` 版本

建议继续作为 PR 必跑：

```bash
pytest tests/extensions/ai_assets/test_ai_assets_extension.py -v
pytest tests/integrations/test_integration_generic.py -v
pytest tests/integrations/test_integration_codex.py -v
```

这一层只判断功能正确性，不判断 AI 产出质量。

### L1: 资产质量评测

目标：评估 `ai-assets.extract` 生成的 7 个资产是否准确、可追溯、不过度编造。

评估对象：

- `ai-assets/project-overview.md`
- `ai-assets/glossary.md`
- `ai-assets/architecture.md`
- `ai-assets/repo-map.md`
- `ai-assets/conventions.md`
- `ai-assets/evolution-log.md`
- `ai-assets/extraction-report.md`

核心指标：

| 指标 | 定义 |
|---|---|
| `asset_file_completeness` | 7 个资产文件是否全部存在 |
| `section_completeness` | 6 个核心资产是否包含 `Observed / Inferred / Open Questions` |
| `grounded_rate` | 有明确来源路径的结论数 / 总结论数 |
| `unsupported_observed_count` | 写在 `Observed` 但找不到来源的结论数 |
| `wrong_fact_count` | 与源码、配置、正式文档冲突的结论数 |
| `useful_asset_score` | 人工评估资产对理解项目是否有帮助，1-5 分 |

最低通过标准：

- `asset_file_completeness = 100%`
- `section_completeness = 100%`
- `grounded_rate >= 80%`
- `unsupported_observed_count = 0`
- `wrong_fact_count = 0`

### L2: 离线规划质量 A/B

目标：只跑到 `plan + tasks`，先不写代码，以较低成本验证规划质量。

推荐第一版规模：

```text
10 个 case
x 2 组：A baseline / B asset enhanced
x 3 次重复
= 60 份 plan/tasks
```

评估对象：

- `specs/<feature>/plan.md`
- `specs/<feature>/tasks.md`
- 规划过程中生成的 `research.md`、`data-model.md`、`contracts/*`、`quickstart.md`

自动指标：

| 指标 | 定义 |
|---|---|
| `path_exists_rate` | 输出中提到的仓库路径真实存在比例 |
| `missing_path_count` | 输出中不存在的路径数量 |
| `unknown_command_count` | 输出中不存在或无法解释来源的命令数量 |
| `unknown_dependency_count` | 输出中不在配置或源码中出现的依赖数量 |
| `wrong_test_framework_count` | 测试框架识别错误次数 |
| `asset_reference_count` | B 组 plan 中明确引用资产结论的次数 |
| `conflict_recorded_count` | 发现资产与事实源冲突并记录的次数 |

人工盲评指标：

| 指标 | 分值 | 评分含义 |
|---|---:|---|
| 仓库事实准确性 | 25 | 路径、模块、技术栈、入口、脚本是否准确 |
| 架构与模块边界贴合 | 20 | 是否沿用现有分层、依赖方向和边界 |
| 术语一致性 | 15 | 是否使用项目既有术语，是否乱造名词 |
| 约定与测试策略符合度 | 15 | 是否遵守命名、测试、脚本、流程约定 |
| 任务可执行性 | 15 | tasks 是否能直接分配给工程师执行 |
| 幻觉与越界风险 | 10 | 是否提出不存在组件、过度重构或越界修改 |

总分 100 分。建议每份产物由 2 名 reviewer 独立评分，分歧超过 15 分时进行复核。

### L3: 历史 feature replay A/B

目标：用真实历史 feature 验证 `ai-assets` 是否真正减少实现返工，并让 AI 产出更接近真实业务改动。

这是本评测体系中最有说服力的一层。它不依赖人工编造需求，而是使用真实项目历史：

```text
master/main 起始 commit: M
真实 feature 最终 commit: F

gold reference: M -> F
A 组实验: M + upstream spec-kit + 同一需求
B 组实验: M + spec-asset-kit + 同一需求
```

`M -> F` 是参考答案，不是唯一正确答案。裁判要判断 AI 产出是否满足同一业务目标，而不是只追求 diff 完全相同。

流程：

1. 选择 3-5 个已合并的真实历史 feature，记录当时的起始 commit `M` 和最终 commit `F`。
2. 从 `M` 创建两份干净工作区，分别安装 A 组和 B 组工具链。
3. 使用同一份需求输入，不暴露 `F` 的 diff 或最终实现。
4. A/B 两组都完整执行 `specify -> plan -> tasks -> implement`。
5. 固定时间上限，例如每个 case 每组最多 60-120 分钟。
6. 运行同一套测试、静态检查、构建命令。
7. 生成 A/B 两组相对 `M` 的 git diff。
8. 在裁判阶段引入 `M -> F` 的真实 diff，进行多 agent 综合评判。

指标：

| 指标 | 定义 |
|---|---|
| `test_pass_rate` | 生成实现后测试通过比例 |
| `review_blocker_count` | review 中阻塞合并的问题数量 |
| `rework_count` | 需要重新规划或返工的次数 |
| `expected_file_hit_rate` | AI 改到的 gold 关键文件数 / gold 关键文件数 |
| `changed_file_precision` | 实际修改文件中，属于 gold 关键范围或合理替代范围的比例 |
| `out_of_scope_file_count` | 越界修改文件数量 |
| `behavior_match_score` | 多 agent 判断业务行为与真实 feature 目标的匹配度，1-5 分 |
| `test_overlap_rate` | AI 覆盖到的 gold 测试场景数 / gold 测试场景数 |
| `gold_diff_alignment_score` | 与真实 diff 的意图和范围接近度，1-5 分 |
| `manual_fix_minutes` | 人工修正到可合并所需时间 |

通过标准：

- B 组 `review_blocker_count` 低于 A 组
- B 组 `out_of_scope_file_count` 低于 A 组
- B 组 `manual_fix_minutes` 低于 A 组
- B 组 `behavior_match_score` 和 `gold_diff_alignment_score` 高于 A 组
- B 组不能以显著增加实现时间为代价换取质量提升

### L3 裁判设计

历史 feature replay 推荐使用多 agent 分工裁判。每个裁判只负责一个维度，最后由 judge 汇总。

| 裁判 | 输入 | 职责 |
|---|---|---|
| 架构 reviewer | 仓库快照、A/B diff、gold diff | 判断模块边界、分层、依赖方向是否合理 |
| 业务 reviewer | 原始需求、A/B diff、gold diff | 判断是否满足真实 feature 的业务意图 |
| 测试 reviewer | A/B 测试改动、测试结果、gold 测试 | 判断测试覆盖、边界场景和回归风险 |
| diff reviewer | A/B diff、gold diff | 判断关键文件命中、遗漏、越界和替代实现是否可接受 |
| 质量 reviewer | A/B diff、仓库约定 | 判断可维护性、异常处理、兼容性、性能风险 |
| judge | 所有 reviewer 输出 | 汇总分数，给出可合并判断和主要原因 |

裁判输出必须结构化：

```yaml
case_id: feature-replay-001
group: B
scores:
  business_correctness: 4
  architecture_fit: 4
  test_quality: 3
  gold_diff_alignment: 4
  scope_control: 5
  maintainability: 4
blockers:
  - "缺少对空配置的边界测试"
acceptable_for_pr: true
summary: "实现覆盖了核心业务意图，改动范围比 gold 更小，但测试覆盖略弱。"
```

建议总分：

| 维度 | 分值 |
|---|---:|
| 业务正确性 | 25 |
| 架构贴合度 | 20 |
| 测试质量 | 15 |
| gold diff 意图对齐 | 15 |
| 改动范围控制 | 15 |
| 可维护性 | 10 |

总分 100 分。`acceptable_for_pr = false` 时，即使总分较高，也要记录为阻塞样本。

### L4: 团队真实 A/B

目标：在真实开发流程中验证价值。

建议先灰度 2 周：

- 选择 1-2 个维护者熟悉的 brownfield 仓库。
- 选择低风险需求，不选择紧急线上问题。
- 每个需求随机进入 baseline 或 asset enhanced 流程。
- 所有需求进入统一记录表。

真实指标：

- 需求从 spec 到 plan 的耗时
- plan review 轮次
- tasks review 轮次
- PR review 问题数
- 返工次数
- 合并后 bug 数
- 开发者主观满意度，1-5 分

## Case 数据集设计

每个 case 应该包含：

```text
case-id
repo-name
repo-commit
base-branch
base-commit
feature-branch
feature-final-commit
feature-input
expected-entrypoints
expected-modules
expected-test-entrypoints
forbidden-areas
domain-terms
known-conventions
gold-notes
```

推荐 case 类型：

| 类型 | 示例 |
|---|---|
| 小型配置改动 | 给已有 CLI 增加一个选项 |
| API 扩展 | 给已有 OpenAPI 增加一个字段 |
| 管理后台改动 | 新增筛选条件或列表字段 |
| 测试补齐 | 给已有模块补单元测试 |
| 模块内小功能 | 沿用现有 service/repository 分层加逻辑 |
| 文档/模板改动 | 增加一个命令模板或扩展说明 |
| 跨模块轻集成 | 在已有 hook 或 workflow 中接入一步 |
| 约定敏感任务 | 必须遵守命名、目录、脚本或 TDD 约定 |

不建议第一版包含：

- 大型重构
- 多服务联调
- 依赖外部私有系统才能验证的需求
- 需要大量产品判断的开放式需求

### 历史 feature replay case 选择标准

优先选择：

- 已经合并、线上或测试环境验证过的 feature。
- 起始 commit `M` 和最终 commit `F` 清晰可追溯。
- 原始需求描述可以找回，例如 Jira、飞书、PR 描述、需求文档。
- 改动规模小到中等，建议 gold diff 小于 30 个文件。
- 可以在本地或 CI 中运行基本测试。
- 业务判断相对明确，不需要大量外部系统状态。

避免选择：

- 只做代码格式化或依赖升级的分支。
- 大型重构和迁移。
- 多个无关需求混在一起的分支。
- 线上紧急修复但上下文缺失的分支。
- 真实实现本身质量有明显争议的分支。

每个 replay case 至少记录：

```text
base commit M
gold commit F
原始需求输入
真实 PR 链接或历史记录
真实测试命令
gold 关键文件列表
gold 关键业务场景
不可泄露给执行 agent 的裁判材料
```

## 数据记录格式

### case manifest

建议使用 `evaluation/cases/<case-id>/case.yml`：

```yaml
id: cli-option-001
repo: sample-cli
base_branch: main
base_commit: abc1234
feature_branch: feature/dry-run
feature_final_commit: def5678
feature_input: "为已有 CLI 增加 --dry-run 参数，只打印将要执行的动作，不实际写文件。"
expected_entrypoints:
  - src/specify_cli/__init__.py
expected_modules:
  - src/specify_cli
expected_test_entrypoints:
  - tests/
forbidden_areas:
  - src/specify_cli/integrations/
domain_terms:
  - dry-run
  - CLI
known_conventions:
  - "新增 CLI 行为必须有 pytest 覆盖"
gold_notes:
  - "应沿用现有 argparse/click/typer 入口，具体以仓库事实为准"
gold_reference:
  diff_range: "abc1234..def5678"
  key_files:
    - src/specify_cli/__init__.py
    - tests/test_cli_dry_run.py
  key_behaviors:
    - "--dry-run 不写文件"
    - "--dry-run 输出即将执行的动作"
judge_only:
  pr_url: "https://example.com/pr/123"
  notes:
    - "gold_reference 和 judge_only 不允许暴露给执行 agent"
```

### run record

建议使用 `evaluation/runs/<run-id>/run.yml`：

```yaml
run_id: 2026-05-05-cli-option-001-b-01
case_id: cli-option-001
group: B
model: gpt-5
temperature: 0
agent: codex
base_commit: abc1234
feature_final_commit: def5678
started_at: "2026-05-05T10:00:00+08:00"
outputs:
  plan: specs/001-cli-option/plan.md
  tasks: specs/001-cli-option/tasks.md
  diff: evaluation/runs/2026-05-05-cli-option-001-b-01/changes.diff
metrics:
  path_exists_rate: 0.95
  missing_path_count: 1
  unknown_dependency_count: 0
  wrong_test_framework_count: 0
  expected_file_hit_rate: 0.80
  out_of_scope_file_count: 2
  behavior_match_score: 4
review:
  reviewer_1_score: 84
  reviewer_2_score: 80
  blocker_count: 2
  correction_count: 5
```

## 历史 replay 执行流程

每个历史 feature 建议建立如下目录：

```text
evaluation/
|- cases/
|  `- cli-option-001/
|     |- case.yml
|     `- input.md
`- runs/
   |- cli-option-001-a-01/
   |- cli-option-001-b-01/
   `- cli-option-001-judge/
```

### 1. 准备 gold reference

维护者执行：

```bash
git checkout main
git checkout -b eval/base-cli-option-001 <base_commit>
git diff <base_commit>..<feature_final_commit> > evaluation/cases/cli-option-001/gold.diff
git diff --name-only <base_commit>..<feature_final_commit> > evaluation/cases/cli-option-001/gold-files.txt
```

`gold.diff` 和 `gold-files.txt` 只给裁判阶段使用，不给执行开发的 agent。

### 2. 准备 A/B 工作区

推荐使用独立 worktree：

```bash
git worktree add ../eval-cli-option-001-a <base_commit>
git worktree add ../eval-cli-option-001-b <base_commit>
```

A 组安装或复制 upstream `spec-kit` 配置。B 组安装或复制 `spec-asset-kit` 配置。

### 3. 执行同一需求

两组使用同一个 `input.md`，只包含原始需求和允许公开的背景：

```text
请基于当前仓库实现以下需求：

[原始需求内容]

约束：
- 不要读取任何 gold diff 或历史 feature 最终实现。
- 按当前工具链执行 specify/plan/tasks/implement。
- 完成后运行项目测试并报告结果。
```

执行阶段记录：

- 开始时间
- 结束时间
- 使用模型
- 使用 agent
- 执行命令
- 测试命令和结果
- agent 最终总结

### 4. 生成实验 diff

每组完成后：

```bash
git diff <base_commit> > evaluation/runs/cli-option-001-b-01/changes.diff
git diff --name-only <base_commit> > evaluation/runs/cli-option-001-b-01/changed-files.txt
```

### 5. 多 agent 裁判

裁判阶段输入：

- 原始需求
- base commit 仓库快照
- gold diff
- A 组 diff
- B 组 diff
- A/B 测试结果
- A/B `plan/tasks`

裁判阶段输出：

- 每个 reviewer 的结构化评分
- judge 汇总评分
- A/B 对比结论
- 是否接受 B 组优于 A 组
- 高频失败原因

## 自动检查建议

第一版自动检查不需要复杂 NLP，优先做确定性规则：

1. 从 `plan.md`、`tasks.md` 中提取反引号包裹的路径。
2. 判断路径是否存在，或是否在任务中明确表示为“待创建”。
3. 从输出中提取命令片段，判断命令是否来自 `scripts/`、`pyproject.toml`、`package.json`、`Makefile` 或文档。
4. 提取依赖名，判断是否来自配置文件或源码 import。
5. 检查是否提到错误测试框架，例如 Python 项目却规划 `go test`。
6. 检查 B 组 `plan.md` 是否填写 `AI Assets 输入`，并引用具体资产文件。

这些检查可以先作为脚本输出 JSON，不直接阻塞人工评审。

## 人工评审规则

L2 离线规划评审只评 `plan/tasks`，采用盲评。L3 历史 replay 裁判可以使用 gold diff，但只能在执行开发完成之后使用。

评审者只看：

- feature 输入
- 仓库快照
- 生成的 `plan/tasks`
- case 的 gold checklist

评审者不看：

- 分组信息
- 是否使用 `ai-assets`
- 另一组输出

L3 裁判额外可以看：

- A/B 实验 diff
- gold diff
- A/B 测试结果
- A/B 运行日志

L3 裁判仍不应知道哪个输出来自 A 组或 B 组，直到独立评分完成。

必须记录：

- 必须修正问题
- 可接受但建议优化问题
- 幻觉项
- 越界项
- 评分
- review 用时

示例问题分类：

| 类型 | 说明 |
|---|---|
| `wrong-path` | 引用了不存在或错误目录 |
| `wrong-boundary` | 模块边界判断错误 |
| `wrong-stack` | 技术栈、测试框架、构建方式错误 |
| `hallucinated-api` | 编造 API、命令、配置或依赖 |
| `missing-convention` | 忽略仓库已有约定 |
| `not-actionable` | 任务不可执行或过于抽象 |
| `over-engineering` | 明显过度设计 |
| `scope-creep` | 超出 feature 范围 |

## 统计与判定

每个指标同时看：

- 平均值
- 中位数
- 最差 case
- 标准差或离散程度
- B 组相对 A 组提升比例

提升计算：

```text
正向指标提升 = (B - A) / A
负向指标下降 = (A - B) / A
```

建议结论分级：

| 结论 | 标准 |
|---|---|
| 强收益 | B 组核心指标提升 30% 以上，且无明显成本增加 |
| 中等收益 | B 组核心指标提升 10%-30%，部分 case 明显有效 |
| 弱收益 | B 组提升低于 10%，或只在个别 case 有效 |
| 无收益 | B 组与 A 组接近，或引入更多错误 |
| 负收益 | B 组耗时、错误、返工明显增加 |

## 推荐执行节奏

### 第 1 周：建立评测集

- 选 5 个小型 brownfield case，其中至少 2 个来自真实历史 feature replay
- 为每个 case 写 `case.yml`
- 写 gold checklist
- 跑通 A/B 各 1 次
- 调整评分表和自动检查规则

### 第 2 周：离线 A/B

- 扩展到 10 个 case
- A/B 各重复 3 次
- 做人工盲评
- 输出第一版评测报告

### 第 3 周：历史 feature replay A/B

- 选择 3-5 个真实历史 feature 跑到 `implement`
- 生成 A/B diff，并与 gold diff 做多 agent 综合评判
- 统计测试、review blocker、返工、越界修改、gold 关键文件命中
- 修正 `ai-assets.extract` 和 `plan` 模板中的高频问题

### 第 4 周：团队灰度

- 在真实仓库灰度 2 周
- 每个真实需求记录组别和结果
- 根据真实指标决定是否默认启用或继续优化

## 评测报告模板

每轮评测输出一份报告：

```markdown
# AI Assets Evaluation Report

## Summary

- Date:
- Evaluator:
- Model:
- Cases:
- Groups:

## Main Result

| Metric | A Baseline | B Asset | Delta |
|---|---:|---:|---:|
| Plan score | | | |
| Missing path count | | | |
| Hallucination count | | | |
| Review blocker count | | | |
| Task actionability | | | |
| Expected file hit rate | | | |
| Out-of-scope file count | | | |
| Behavior match score | | | |
| Gold diff alignment score | | | |

## Historical Replay Result

| Case | A Acceptable | B Acceptable | A Score | B Score | Winner | Reason |
|---|---|---|---:|---:|---|---|
| | | | | | | |

## Findings

## Failure Cases

## Judge Notes

## Template Changes Suggested

## Extractor Changes Suggested

## Decision

- [ ] Continue
- [ ] Roll back default enablement
- [ ] Ship with limitations
- [ ] Expand to real team A/B
```

## 迭代闭环

评测结果应该反向驱动三类改动：

1. `ai-assets.extract` 命令：如果资产缺事实、来源不足、术语遗漏，就优化提取提示词与 scanner。
2. `plan` 模板：如果资产存在但未被使用，就强化 `AI Assets 输入` 的填写要求和冲突记录要求。
3. `tasks` 模板：如果 plan 已准确但 tasks 不可执行，就增加路径、测试、验收约束。

不要只根据单个 case 调模板。至少出现 3 次以上的同类问题，才进入模板级修正。

## 最小可行版本

如果时间有限，先做这个最小闭环：

1. 准备 5 个 case。
2. 其中 3 个只跑到 `plan/tasks`，2 个使用历史 feature replay 跑到 `implement`。
3. A/B 各跑 3 次。
4. L2 记录 `missing_path_count`、`hallucination_count`、`review_correction_count`、`task_actionability_score`。
5. L3 记录 `expected_file_hit_rate`、`out_of_scope_file_count`、`behavior_match_score`、`gold_diff_alignment_score`。
6. 输出一份报告。

这个版本已经足够判断 `ai-assets` 是否值得继续投入。
