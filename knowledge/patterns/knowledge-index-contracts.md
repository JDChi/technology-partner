# Knowledge Index Contracts

## Summary
- 对 agent-first 的知识系统，主索引应被设计成稳定的机器接口，而不是顺手维护的人类目录页。默认推荐：用 `knowledge/index.json` 作为唯一主索引，明确最小字段 contract，规定生成端以真实文件系统为准，消费端先查索引再开具体文档。Markdown 目录页如果未来需要，只应作为派生视图，而不是主源。

## Context
- `technology-partner` 已经把知识库作为长期记忆使用，agent 每次回答前都需要先判断“已有知识里有没有相关条目”。
- 旧的 `knowledge/index.md` 适合人类浏览，但对 agent 来说是半结构化文本：需要自己解析 section、路径、摘要和层级语义。
- 当前我们已经引入 `scripts/knowledge_index.py` 和 `knowledge/index.json`，但如果不把字段语义和使用边界文档化，它仍然只是“现在能用的一种实现”，而不是长期稳定接口。

## Recommendation
- 把 `knowledge/index.json` 视为唯一主索引。
- 主索引默认首先服务 agent 和脚本，不优先服务人类浏览。
- 索引 contract 应保持小而稳，先固定最小必要字段，再谨慎扩展。
- 如果未来仍需要 Markdown 目录页，它只能从 `index.json` 派生生成，不能反向成为主源。

## Applicable Scenarios
- 需要让 agent 在回答前快速发现已有知识，而不是每次遍历整个 `knowledge/`。
- 需要脚本稳定地创建、同步、校验和重建知识入口。
- 需要把知识系统从“文件夹约定”提升为“可被程序消费的接口”。
- 需要未来继续增加自动化，例如知识体检、近重复检测或索引导出。

## Non-Applicable Scenarios
- 知识量极小，且只有人类手工浏览，不需要任何自动化入口。
- 索引只作为一次性迁移脚本的中间产物，不打算长期维护。
- 系统不要求 agent 先查知识再回答，而是始终人工指定文档路径。

## Tradeoffs And Risks
- JSON 更利于 agent 和脚本消费，但直接阅读体验弱于 Markdown 目录页。
- 一旦字段成为 contract，后续修改会产生兼容成本，不能随意重命名或删改。
- 如果索引和真实文件系统不同步，agent 会被错误入口误导，因此同步脚本和校验机制必须可靠。
- 把主索引优先给机器使用，会弱化“打开一个目录页就能读完全局”的人类体验。

## Implementation Notes
- 主索引路径：
  - `knowledge/index.json`
- 最小字段 contract：
  - `type`: 条目类型，例如 `pattern`、`scenario`、`workflow`、`decision`
  - `path`: 相对 `knowledge/` 的文档路径
  - `title`: 文档一级标题
  - `slug`: 稳定、简短的机器标识
- 条件字段 contract：
  - `date`: 仅当条目本身天然有日期语义时使用，例如 `decision`
  - `created_at`: 记录索引当前看到该文件的基础时间信息；它可以用于排序或粗粒度筛查，但不应被误解为“正式发布日期”
- 生成端规则：
  - 以真实文件系统为准，而不是以旧索引或人类目录页为准
  - 由 `scripts/knowledge_index.py` 负责创建和同步
  - 当前默认接受 `README` 型目录说明进入索引，但这是一条当前规则，不代表永恒最佳实践
- 消费端规则：
  - 先查 `index.json`，再按 `path` 打开具体文档
  - 先判断是否已有相关条目，再决定更新旧文档还是新建条目
  - 当索引字段不足以回答问题时，必须回到正文，而不是把索引当作知识全文
- 演进原则：
  - 新字段默认后向兼容
  - 不为了“以后也许会用”而过早加入 `tags`、`summary`、`related` 等字段
  - 先把字段语义定稳，再考虑导出 Markdown 视图或更复杂校验

## Open Questions
- 当前 `created_at` 是否应继续沿用文件时间语义，还是未来切换成更明确的文档元数据来源。
- `README` 型目录说明未来是否应继续作为正式索引项，还是降级为可选辅助说明。
- 当知识条目数量继续增长时，是否需要增加 `summary` 或 `related` 之类的新字段。

## Related Knowledge
- [2026-05-03-script-first-automation.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/decisions/2026-05-03-script-first-automation.md)
- [agent-oriented-cli-tooling.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/patterns/agent-oriented-cli-tooling.md)
- [repo-to-generalized-guidance.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/workflows/repo-to-generalized-guidance.md)
