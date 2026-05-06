# Evaluation Toolkit

本目录是 `ai-assets` 增强 spec-kit 的可迁移评测工具包。

这里不应该沉淀大量真实业务项目源码或未脱敏 feature diff。真正有说服力的量化验证应在真实业务项目中执行；本目录负责提供统一结构、schema、rubric、聚合脚本和一个 simulated smoke case，保证不同项目采集出来的数据可以横向比较。

## 职责边界

| 位置 | 职责 |
|---|---|
| `spec-asset-kit/evaluation/` | 维护评测方法、数据结构、裁判规则、聚合脚本、示例 case |
| 真实业务项目 `.speckit-eval/` 或 `evaluation/` | 采集真实历史 feature replay 的 cases、runs、metrics、reports |
| 脱敏结果回流 | 只回流 `metrics.yml`、`summary.json`、`results.csv`、结论报告或已脱敏示例 |

核心判断不是“能否出报告”，而是能否稳定产出可重复聚合的数据：

- B 组相对 A 组的胜率
- PR 可接受率提升
- hallucinated path / wrong dependency 降低率
- review blocker 降低率
- gold diff alignment 提升
- manual repair cost 降低

## 推荐目录

在真实项目中复制或对齐以下结构：

```text
.speckit-eval/
|- cases/
|  `- <case-id>/
|     |- case.yml
|     |- input.md
|     |- gold.diff
|     `- gold-files.txt
|- runs/
|  |- <case-id>-a-01/
|  |  |- run.yml
|  |  |- metrics.yml
|  |  |- plan.md
|  |  |- tasks.md
|  |  |- changes.diff
|  |  `- changed-files.txt
|  |- <case-id>-b-01/
|  |  `- ...
|  `- <case-id>-judge/
|     `- judge-summary.yml
|- metrics/
|  |- results.csv
|  |- summary.json
|  `- quantitative-summary.md
`- reports/
```

## 数据文件

- `schemas/case.schema.yml`：历史 replay case 字段说明。
- `schemas/run.schema.yml`：单次 A/B run 字段说明。
- `schemas/metrics.schema.yml`：正向/负向指标、目标门槛和聚合口径。
- `rubrics/l3-judge-rubric.zh-CN.md`：L3 多 reviewer 裁判规则。
- `cases/_template/`：新 case 模板。
- `runs/_template/`：新 run 模板。
- `reviews/_template/`：单 reviewer 评分模板。

`sim-cli-dry-run-001` 是 simulated smoke case，只用于验证流程和聚合脚本，不作为真实收益证据。

## 标准实验形状

每个真实历史 feature replay 使用：

```text
base commit M
gold commit F
A: M + upstream spec-kit + 原始需求
B: M + spec-asset-kit + ai-assets + 原始需求
judge: A/B 输出 + gold diff
```

执行 agent 不能看到 `gold.diff`、`gold-files.txt`、`feature_final_commit` 的最终实现或 `judge_only` 信息。gold 材料只允许在 judge 阶段使用。

建议最小规模：

- 至少 8 个真实历史 replay case
- A/B 每组每个 case 至少重复 3 次
- 使用同一 agent、模型、temperature、时间上限和测试命令
- 输出独立结构化评分，再做总 judge 汇总

## 聚合数据

在本仓库或真实项目评测目录下运行：

```bash
python evaluation/scripts/aggregate_results.py
```

如果真实项目使用 `.speckit-eval/`：

```bash
python /path/to/spec-asset-kit/evaluation/scripts/aggregate_results.py \
  --evaluation-root .speckit-eval
```

输出：

- `metrics/results.csv`：每个 A/B run 一行，便于导入表格或 BI。
- `metrics/summary.json`：机器可读聚合结果。
- `metrics/quantitative-summary.md`：面向人阅读的量化摘要。

聚合脚本优先读取每个 run 目录下的 `metrics.yml`；如果不存在，则回退读取 `run.yml` 中的 `metrics` 字段。

## 通过门槛

第一阶段建议用以下门槛判断是否值得继续增强 spec-kit：

- B 组 `acceptable_for_pr` 胜率高于 A 组 20% 以上。
- B 组 `missing_path_count`、`unknown_dependency_count` 或同类幻觉指标平均下降 30% 以上。
- B 组 `review_blocker_count` 平均下降 25% 以上。
- B 组 `gold_diff_alignment_score` 平均提升 15% 以上。
- B 组不能显著增加 `out_of_scope_file_count` 和 `manual_fix_minutes`。
- L0 工程回归持续通过。

如果只在 simulated case 中成立，结论只能写成“流程可运行”；只有真实业务项目 replay 数据达到门槛，才可以写成“增强 spec-kit 有稳定量化收益”。
