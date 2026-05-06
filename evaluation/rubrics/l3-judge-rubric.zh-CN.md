# L3 Historical Replay Judge Rubric

L3 裁判只在 A/B 执行完成后使用 gold diff。执行 agent 不允许读取 `gold.diff`、`gold-files.txt`、真实最终实现或 `judge_only` 字段。

## 输入

- 原始需求 `input.md`
- A/B 的 `plan.md`、`tasks.md`
- A/B 的 `changes.diff`、`changed-files.txt`
- A/B 的测试命令和结果
- gold diff 和 gold key files
- case manifest 中的 gold behavior checklist

## 评分维度

| 维度 | 分值 | 评分要点 |
|---|---:|---|
| 业务正确性 | 25 | 是否满足真实 feature 的核心行为，允许不同实现方式 |
| 架构贴合度 | 20 | 是否沿用现有模块边界、分层和依赖方向 |
| 测试质量 | 15 | 是否覆盖 gold 行为、边界场景和回归风险 |
| gold diff 意图对齐 | 15 | 是否命中关键文件、关键行为和合理改动范围 |
| 改动范围控制 | 15 | 是否避免越界修改、重构漂移和无关文件 churn |
| 可维护性 | 10 | 命名、异常处理、兼容性和长期维护成本 |

总分 100。`acceptable_for_pr = false` 的样本必须记录 blocker，即使总分不低。

## 输出

每个 reviewer 输出 `evaluation/reviews/_template/reviewer-score.yml` 形状的结构化结果。最终 judge 输出：

```yaml
case_id: feature-replay-001
gold_reference:
  diff: evaluation/cases/feature-replay-001/gold.diff
  files: evaluation/cases/feature-replay-001/gold-files.txt
groups:
  A:
    acceptable_for_pr: false
    l2_plan_score: 70
    l3_total_score: 62
    scores:
      business_correctness: 15
      architecture_fit: 12
      test_quality: 8
      gold_diff_alignment: 8
      scope_control: 12
      maintainability: 7
    blockers:
      - "遗漏核心边界场景"
  B:
    acceptable_for_pr: true
    l2_plan_score: 86
    l3_total_score: 84
    scores:
      business_correctness: 22
      architecture_fit: 17
      test_quality: 12
      gold_diff_alignment: 13
      scope_control: 12
      maintainability: 8
    blockers: []
winner: B
summary: "B 更接近真实业务意图，且人工修正成本更低。"
```
