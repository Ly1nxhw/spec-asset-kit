# AI Assets Extension

This bundled extension adds `speckit.ai-assets.extract` and
`speckit.ai-assets.refine` to keep a lightweight `ai-assets/` knowledge layer
alongside the normal Spec Kit workflow.

It is designed to:

- scan the repository for verifiable source files and candidate business signals
- synthesize business-facing private knowledge without treating weak repo
  inference as confirmed fact
- collect human confirmation questions in `open-questions.md`
- promote human-confirmed answers through `speckit.ai-assets.refine`
- make `speckit.plan` read confirmed business context before planning

It is not intended to regenerate a full architecture document, tech-stack
inventory, or repository map. Technical facts should appear only as short
implementation anchors that help trace a business concept back to code.

Generated project assets:

- `ai-assets/business-context.md`
- `ai-assets/domain-glossary.md`
- `ai-assets/business-rules.md`
- `ai-assets/user-journeys.md`
- `ai-assets/external-systems.md`
- `ai-assets/decision-log.md`
- `ai-assets/open-questions.md`
- `ai-assets/extraction-report.md`

Core generated assets must separate:

- `已确认知识`
- `候选线索`
- `实现锚点`
- `待确认问题`

Knowledge status values:

- `confirmed`: formal docs/contracts/tests or explicit human confirmation
- `candidate`: repo-derived signal that still needs a human answer
- `deprecated`: old term, old workflow, or knowledge that should not drive new work

Important rule: `ai-assets/` is an interpretation layer for AI assistance. It
does not replace code, configuration, contracts, or formal project documents as
the source of truth.
