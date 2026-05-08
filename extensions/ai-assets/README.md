# AI Assets Extension

This bundled extension adds `speckit.ai-assets.extract` and keeps a lightweight
`ai-assets/` knowledge layer alongside the normal Spec Kit workflow.

It is designed to:

- scan the repository for verifiable source files
- synthesize business-facing private knowledge from those sources
- make `speckit.plan` read business context before planning

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
- `ai-assets/extraction-report.md`

Every generated asset must separate:

- `核心解释`
- `实现锚点`
- `待确认问题`

Important rule: `ai-assets/` is an interpretation layer for AI assistance. It
does not replace code, configuration, contracts, or formal project documents as
the source of truth.
