# Script-First Automation For Technology Partner

## Date
- 2026-05-03

## Status
- Accepted

## Context
- `technology-partner` 当前还是一个以 `AGENTS.md`、`knowledge/` 和模板为核心的知识型项目。
- 我们已经识别出一些值得代码化的重复动作，例如知识条目脚手架、索引同步和知识体检。
- 但当前自动化需求还不够多，尚不足以支持一套正式 CLI 的复杂度和长期维护成本。

## Decision
- 先不设计独立 CLI。
- 先建立 `scripts/` 目录，把自动化能力以脚本形式逐步放进去。
- 等脚本数量、复用频率、参数模式和共享逻辑明显增长后，再评估是否收敛为正式 CLI。

## Alternatives Considered
- 现在就做一个 `tp` CLI。
- 完全不写代码，继续全部靠 agent 手工执行。

## Why This Decision
- Script-first 的进入成本更低，适合当前阶段。
- 这能让我们先验证哪些自动化动作真的高频、稳定、值得长期维护。
- 如果过早做 CLI，容易把项目带入“产品化工具链”复杂度，但核心认知边界还没有完全稳定。
- 如果完全不写代码，又会继续重复做机械工作，不利于知识工作流的长期效率。

## Tradeoffs
- Benefits
  - 实现成本低
  - 迭代快
  - 方便试错
  - 不会过早绑定命令面和用户接口
- Costs
  - 脚本入口可能不统一
  - 参数风格可能暂时不一致
  - 共享逻辑在早期可能会有轻微重复

## Applicable Scenarios
- 自动化需求仍在探索期。
- 需要优先验证“哪些动作值得代码化”。
- 项目核心仍是知识与方法，而不是工具分发。

## Revisit Conditions
- `scripts/` 中已经出现多于 5 个长期保留脚本。
- 多个脚本开始共享参数解析、文件创建、索引更新、日志输出等公共逻辑。
- 使用者已经开始频繁记忆脚本名和参数，而不是通过 agent 触发。
- 项目开始需要更明确的命令面、帮助信息和可分发能力。

## Related Knowledge
- [agent-oriented-cli-tooling.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/patterns/agent-oriented-cli-tooling.md)
- [repo-to-generalized-guidance.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/workflows/repo-to-generalized-guidance.md)
