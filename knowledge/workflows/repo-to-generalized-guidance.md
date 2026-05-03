# Repo To Generalized Guidance

## Summary
- 当用户给出一个具体项目时，默认不要只产出“这个项目的介绍”。应优先提炼成更高一层的知识：可复用方案、库选型边界、适用场景、风险和执行流程。项目只是证据样本，不是最终知识单位。

## Trigger Or Use Case
- 用户给出一个新项目，希望我“看一下”。
- 用户持续给不同 repo，但真正想沉淀的是跨项目可复用的方法和判断。
- 某个项目体现了一种典型技术模式，值得进入知识库长期复用。

## Inputs Needed
- 项目 README、配置、核心代码、测试。
- 用户显式目标：是要判断方案、沉淀模式、还是只是做代码 review。
- 如果涉及库选型、基础设施、产品或安全判断，还需要补官方文档或主仓库作为外部证据。

## Step-By-Step Process
1. 先确认抽象层级。
   如果用户给 repo，但目标是长期方法论，就把项目当样本，不把 repo 介绍当成主要输出。
2. 识别“项目特有”与“可复用”的边界。
   项目名、目录结构、具体函数实现通常是局部细节；能力分层、库搭配、失败模式、流程设计才是通用知识。
3. 抽出能力地图。
   用“目标 -> 可选库/组件 -> 适用场景 -> 风险 -> 推荐默认项”的形式重写。
4. 对不稳定事实做外部校验。
   尤其是库选型、模型后端、框架状态、官方支持范围，优先查官方文档或主仓库。
5. 沉淀到正确的知识类型。
   - 可复用方案：写入 `knowledge/patterns/`
   - 场景决策：写入 `knowledge/scenarios/`
   - 执行方法：写入 `knowledge/workflows/`
   - 具体 repo 理解：只有在用户确实需要时，才写入 `knowledge/architecture/`
6. 明确证据与假设。
   把“verified facts”“working assumptions”“open questions”分开，避免把项目偶然实现写成普适规律。

## Expected Outputs
- 一份或多份可复用知识条目，而不是 repo 游记。
- 一个清晰的默认推荐。
- 适用与不适用场景。
- 风险、约束、后续验证项。

## Quality Checks
- 读者即使没看过原项目，也能直接用这份知识做下一次判断。
- 知识条目不依赖某个 repo 的路径结构才能成立。
- 涉及最新生态判断时，已经补过官方来源。
- 没有把局部实现偏好误写成普遍最佳实践。

## Non-Goal
- 不为了“留痕”而记录每个项目的目录树。
- 不在没有复用价值时，堆积 repo 级笔记。
- 不把具体项目的临时 workaround 直接升级为长期模式。

## Related Knowledge
- [local-media-artifact-pipeline.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/patterns/local-media-artifact-pipeline.md)
