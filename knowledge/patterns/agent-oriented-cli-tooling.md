# Agent-Oriented CLI Tooling

## Summary
- 给 agent 用的 CLI，不应只是“人类也能运行的脚本”，而应被设计成一个稳定的能力边界。默认推荐：用离散命令暴露粗粒度能力，用 JSON 作为主契约，用 `doctor`/capability discovery 处理环境前提，用统一错误模型处理失败路径，用确定性工件路径承载副作用。CLI 适合作为 agent 与重依赖、本地工具、跨语言能力之间的隔离层。

## Context
- 来源样本：`media-extract`。
- 目标是沉淀“什么样的工具适合做成 agent CLI，以及应怎么设计”的长期模式。

## Verified Facts
- 样本 repo 把能力拆成多个独立命令，而不是一个黑盒分析入口：`doctor`、`probe`、`extract-audio`、`sample-frames`、`transcribe`。
- 样本 repo 用统一 `success/failure` JSON 结构表达结果和错误，说明 agent 更适合消费稳定契约，而不是依赖散乱 stdout。
- 样本 repo 同时支持人类可读的 `doctor` 输出和 `doctor --json`，说明“人类操作入口”和“agent 契约入口”可以共存，但必须显式切换。
- Node 官方文档说明 `node:child_process` 是标准子进程能力基础。
- Execa 官方 README 明确强调它是在 `child_process` 之上、面向程序化执行优化的封装，提供更好的错误对象、跨平台行为和输入输出控制。
- `cac` 适合轻量 CLI，官方包描述里强调它支持命令、选项、帮助输出和 TypeScript，适合构建简单但结构清晰的工具。

## Recommendation
- 什么时候优先做 CLI：
  - 能力本身是离散动作，不是长时间交互式会话。
  - 依赖本地二进制、系统工具或跨语言运行时。
  - 需要让不同 agent、不同脚本、不同宿主语言都能复用同一能力。
  - 副作用主要是“生成文件/工件”，而不是维护长期内存状态。
- 什么时候不要优先做 CLI：
  - 需要极低延迟、多次细粒度调用。
  - 需要常驻缓存、会话状态、队列、并发调度。
  - 调用方和实现方在同一运行时里，直接函数调用明显更简单。
- 默认设计原则：
  - 一个命令只做一件清晰的事。
  - 默认输出机器可消费；如果要有人类模式，显式加开关。
  - 成功和失败都必须有稳定 JSON 形状。
  - 在真正执行前先暴露 capability/doctor。
  - 输出路径必须可预测、可幂等、可防冲突。
  - 错误信息要包含可行动的 remediation，而不仅是 stderr 原文。

## Applicable Scenarios
- 本地 agent 工具箱。
- 跨语言工具封装，例如 Node 编排 Python、FFmpeg、Git、ImageMagick。
- 重依赖但粗粒度的工程能力，如媒体处理、文档转换、代码生成、环境检查。
- 需要把复杂系统依赖隐藏在简单命令面后面。

## Non-Applicable Scenarios
- 高频细粒度函数调用。
- 需要长驻内存缓存和复杂并发调度的系统。
- 需要远程多租户共享能力，更适合直接做服务而不是本地 CLI。

## Tradeoffs And Risks
- CLI 边界清晰，但会引入进程启动成本和文件系统协调成本。
- 如果 JSON 契约不稳定，agent 集成会比人类脚本更脆弱。
- 如果默认输出目录没有冲突控制，多个输入或重复执行会互相污染。
- 如果没有 `doctor`，agent 会把环境错误误判成业务失败。
- 如果命令粒度太粗，错误定位困难；太细，则编排成本升高。

## Implementation Notes
- 推荐的最小命令集合：
  - `doctor`: 环境、依赖、能力探测
  - `probe`: 轻量读操作，不产生重副作用
  - `run-*` / `extract-*` / `convert-*`: 具名执行动作
- 推荐的结果模型：
  - `ok`
  - `command`
  - `input`
  - `outputs`
  - `warnings`
  - `error`
- 推荐的错误模型：
  - 稳定的错误码
  - 用户可读 message
  - 结构化 details
  - 可选 remediation/install command
- 同步 vs 异步：
  - 短任务、本地串行任务：同步 CLI 足够，简单可靠。
  - 长任务、批量任务、可取消任务：应显式设计异步 job 模型，或至少支持 timeout、cancel、progress。
- Node 实现建议：
  - 基础版可直接用 `node:child_process`
  - 一旦出现超时、取消、流式输出、跨平台兼容、详细错误需求，优先评估 `execa`
  - 轻量命令编排可用 `cac`；若命令树和插件能力增长，再评估更重的 CLI 框架

## Open Questions
- 对于 agent 场景，默认应该是“JSON 默认、人类模式显式开启”，还是继续保留“人类默认、JSON 用开关开启”。
- 是否需要把 manifest 输出提升为所有 agent CLI 的强制约束，而不是局部约定。

## Related Knowledge
- [local-media-artifact-pipeline.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/patterns/local-media-artifact-pipeline.md)
- [video-understanding-preprocessing-pipeline.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/patterns/video-understanding-preprocessing-pipeline.md)
- [build-agent-cli-from-sample-repo.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/workflows/build-agent-cli-from-sample-repo.md)

## Evidence And Sources
- Sample repo evidence:
  - `/Users/chijiaduo/develop/media-extract/src/cli.ts`
  - `/Users/chijiaduo/develop/media-extract/src/lib/output.ts`
  - `/Users/chijiaduo/develop/media-extract/src/lib/doctor.ts`
  - `/Users/chijiaduo/develop/media-extract/src/lib/fs.ts`
  - `/Users/chijiaduo/develop/media-extract/README.md`
- External sources:
  - [Node.js child_process](https://nodejs.org/api/child_process.html)
  - [sindresorhus/execa](https://github.com/sindresorhus/execa)
  - [cac on npm](https://www.npmjs.com/package/cac)
