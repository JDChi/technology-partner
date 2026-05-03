# Build Agent CLI From Sample Repo

## Summary
- 当用户给一个样本 repo，希望沉淀“agent 工具型 CLI”的长期方法时，默认流程不是先描述 repo，而是先拆出能力边界、契约模型、依赖模型、工件模型，再决定哪些部分应该进入 `patterns/`、哪些进入 `workflows/`。目标是从具体实现抽出“如何再造一个类似工具”的方法论。

## Trigger Or Use Case
- 用户给出一个工具 repo，并希望我提炼可复用的 CLI 模式。
- 需要把某个本地工具项目抽象成 agent 可复用的方法，而不是单次项目理解。
- 需要为后续多个工具项目建立统一判断框架。

## Inputs Needed
- README：看目标、范围、依赖、操作方式。
- 入口文件：看命令面和默认交互方式。
- 命令实现：看能力拆分粒度。
- 输出/错误模块：看契约是否稳定。
- 测试：看哪些行为被作者视为核心承诺。
- 如涉及生态选型，再补官方文档或主仓库证据。

## Step-By-Step Process
1. 先读 README。
   识别这个工具的用户是谁，是人、脚本还是 agent；识别它是“处理器”“分析器”还是“编排器”。
2. 读 CLI 入口。
   记录命令集合、帮助输出、默认输出模式、参数风格。
3. 读命令实现。
   看作者如何划分能力边界，是否存在黑盒命令，是否能单独复用某一步。
4. 读输出与错误模型。
   判断是否有稳定 JSON 契约，是否有统一错误码、warning、details、remediation。
5. 读环境探测与依赖管理。
   看是否有 `doctor`、capability discovery、安装建议、平台限制。
6. 读文件系统策略。
   看输出目录是否幂等、是否防冲突、是否把工件当一等公民。
7. 读测试。
   判断 repo 真正承诺的行为边界，而不是只看 README 描述。
8. 抽象成四个问题。
   - 这个工具暴露了哪些能力单元
   - 它如何让 agent 判断“能不能做”
   - 它如何让 agent 读取结果和错误
   - 它如何管理副作用和工件
9. 再决定知识落点。
   - 方案判断写进 `patterns/`
   - 操作方法写进 `workflows/`
   - 只有当用户需要 repo 理解本身时，才写 `architecture/`
10. 最后补外部证据。
   对库选型、官方支持范围、实现替代项做官方校验，避免把样本 repo 的当前偏好写成长期事实。

## Expected Outputs
- 一份“agent 工具型 CLI 应该怎么设计”的模式文档。
- 如 repo 还体现了领域能力，再补一份该领域的独立模式文档。
- 一份“以后怎样从样本 repo 抽象到长期知识”的操作流程。

## Quality Checks
- 产物应该能指导“下一个类似工具怎么做”，而不是只解释“这个 repo 怎么写”。
- 结论应区分：
  - 样本 repo 已验证事实
  - 我们的推荐模式
  - 仍需确认的开放问题
- 如果删掉 repo 名称，文档仍然成立，说明抽象层级基本对了。

## Non-Goal
- 不做目录树抄写。
- 不把 README 原话改写后当成知识沉淀。
- 不把样本项目的所有实现细节都升级成长期规范。

## Related Knowledge
- [repo-to-generalized-guidance.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/workflows/repo-to-generalized-guidance.md)
- [agent-oriented-cli-tooling.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/patterns/agent-oriented-cli-tooling.md)
- [video-understanding-preprocessing-pipeline.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/patterns/video-understanding-preprocessing-pipeline.md)
