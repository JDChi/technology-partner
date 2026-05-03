# Knowledge Index

This file is the entry point for the technology partner knowledge base.

## How To Maintain This Index
- Update this file whenever a durable document is added, merged, renamed, or retired.
- Prefer linking to stable documents instead of temporary notes.
- Group entries by topic so recurring problems are easy to rediscover.

## Sections

### Architecture
- `architecture/README.md`: how to record system understanding and architecture findings

### Decisions
- `decisions/README.md`: how to record decisions, tradeoffs, and superseded choices

### Patterns
- `patterns/README.md`: reusable engineering patterns, conventions, and heuristics
- `patterns/local-media-artifact-pipeline.md`: 本地媒体工件提取方案，含库选型、适用场景与风险边界
- `patterns/video-understanding-preprocessing-pipeline.md`: 视频理解前处理流水线，强调最小工件化、可选增强和 manifest 边界
- `patterns/agent-oriented-cli-tooling.md`: 面向 agent 的 CLI 工具设计模式，含 JSON 契约、doctor、错误模型和 CLI/SDK/service 选择边界

### Scenarios
- `scenarios/README.md`: scenario-based guidance for common problem types
- `scenarios/when-to-use-mlx-whisper.md`: 何时把 `mlx-whisper` 作为本地 ASR 默认选项，以及它的真实能力边界与环境限制

### Workflows
- `workflows/README.md`: repeatable execution playbooks
- `workflows/repo-to-generalized-guidance.md`: 如何从具体项目抽象出通用方案、流程和长期知识
- `workflows/build-agent-cli-from-sample-repo.md`: 如何从样本 repo 抽象出 agent 工具型 CLI 的通用方法

## Current Seed Knowledge
- `evolution-log.md`: changes to the knowledge system itself

## Open Areas To Grow
- repo analysis playbooks
- architecture comparison guides
- stack selection heuristics
- deployment and operations workflows
- code review checklists
- migration strategies
