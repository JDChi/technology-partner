# Agent Workspace Design Order

## Summary
- 设计长期协作型 agent 项目时，默认顺序不应是 `runtime -> orchestration -> unified entrypoint`，而应是 `behavior model -> skill boundaries -> memory model -> runtime`。先回答“agent 应该怎样工作”，再决定“代码是否需要出现”。否则项目很容易过早产品化，把还没稳定的思考方式误做成半成品后端。

## Context
- 很多 agent 项目一开始都会自然滑向“小系统”思路：补 runtime、补流程入口、补 helper、补自动路由。
- 这种路径的问题不在于它一定错，而在于它常常过早回答了实现问题，却还没回答更根本的问题：
  - agent 的价值单元是什么
  - 不同输入应该触发什么能力
  - 什么信息需要成为长期记忆
  - 哪些规则应是全局边界，哪些应是场景流程
- 对长期协作型项目来说，这些问题通常比代码骨架更先决定项目形态。

## Recommendation
- 默认按以下顺序设计 agent 项目：
  - `behavior model`
  - `skill boundaries`
  - `memory model`
  - `runtime`
- 逐层含义：
  - `behavior model`：先定义 agent 的角色、回答原则、边界、信息来源区分和长期协作方式。
  - `skill boundaries`：再定义遇到不同输入或场景时，应激活哪些能力模块。
  - `memory model`：再定义哪些内容值得写回、以什么 record 类型保存、检索顺序是什么。
  - `runtime`：只有在前面三层已经稳定、且纯文档/skill/records 不够支撑时，才引入 helper、store、orchestration 或 CLI。
- 设计判断上，优先把项目理解成“agent 工作空间”而不是“带 agent 的应用骨架”。

## Applicable Scenarios
- 个人长期协作型 agent。
- 以知识、决策、原则、画像、记忆检索为核心的 agent 项目。
- 需要把同一套思考方式复用到不同输入场景，而不是先做一个通用程序入口。
- 还在探索 agent 能力边界，尚未稳定到值得固化为较重代码层。

## Non-Applicable Scenarios
- 明确要做高频调用、批量任务、并发调度、服务接口的系统。
- 已经验证清楚 skill 和 memory contract，当前瓶颈就是性能、复用或程序化编排。
- 项目核心价值在外部产品能力，而不是 agent 内部协作方式。

## Tradeoffs And Risks
- 好处：
  - 能避免把不成熟的 SOP 过早写死进代码。
  - 能让能力边界、记忆边界、全局规则更早稳定。
  - 更容易看出项目真正的最小核心是什么。
- 代价：
  - 早期很多约束会先停留在 `AGENTS.md`、skills、records 和测试里，而不是可复用程序抽象。
  - 如果项目很快需要批处理、复杂检索或跨环境复用，后面仍可能补回 runtime。
  - 团队如果只擅长“程序结构思考”，会觉得这种做法一开始“不像在做工程”。

## Implementation Notes
- 推荐的最小分层：
  - `AGENTS.md`：人格、总原则、全局边界、共享回答规则。
  - `skills/` 或项目级 `.agents/skills/`：场景触发、输入分类、具体流程。
  - `records/` 或其他 memory store：长期状态与写回结果。
  - `schemas/` 或 contracts：结构约束与最小字段模型。
  - `tests/`：守住项目边界，防止旧假设回流。
- 何时说明已经准备好引入 runtime：
  - 多个 skill 之间开始反复共享同一段读写/校验逻辑。
  - 纯文本流程已经不足以可靠完成批量摄取、检索排序、冲突处理。
  - 团队开始需要跨项目复用同一记忆后端或执行链。
- 三个常见的“过早产品化”信号：
  - 还没稳定能力边界，就先补 orchestration。
  - 还没稳定记忆模型，就先补 runtime helper 或 store abstraction。
  - 还没明确输入类型，就先设计统一入口函数。

## Open Questions
- 对不同 agent 平台，skill 边界是否应该继续保留平台耦合，还是尽早抽成平台无关 contract。
- 当 memory model 稳定后，runtime 应该优先长成 CLI、库，还是服务。
- 除了测试之外，是否需要一层更明确的 knowledge/skill lint 来约束行为边界。

## Related Knowledge
- [agent-oriented-cli-tooling.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/patterns/agent-oriented-cli-tooling.md)
- [knowledge-index-contracts.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/patterns/knowledge-index-contracts.md)
- [repo-to-generalized-guidance.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/workflows/repo-to-generalized-guidance.md)
- [2026-05-03-script-first-automation.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/decisions/2026-05-03-script-first-automation.md)

## Evidence And Sources
- Sample-repo evidence:
  - One local sample repo on 2026-05-03 shifted from Markdown-first knowledge scaffolding to JSON records, then to project-local skills, and finally removed an unused runtime layer.
  - Key sample signals included movement toward `.agents/skills/`, explicit memory record types, schema constraints, and tests that enforced the reduced boundary.
- Generalized from:
  - repeated contrast between “make SOP executable in code” and “make agent behavior modular and reusable”
  - the workflow in [repo-to-generalized-guidance.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/workflows/repo-to-generalized-guidance.md), which prefers extracting reusable guidance instead of preserving repo-local detail
