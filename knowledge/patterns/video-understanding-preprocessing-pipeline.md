# Video Understanding Preprocessing Pipeline

## Summary
- 在做视频理解之前，推荐先建立一个独立的“前处理流水线”，把原始视频变成稳定、可复用的工件集合，而不是让上层 agent 或模型直接面对原始文件。默认结构应分为：能力探测、元数据探测、媒体规范化、可选增强、工件清单输出。这样做的重点不是“提取更多”，而是“只提取后续理解真正需要的最小工件”。

## Context
- 来源样本：`media-extract` 这类本地媒体提取 CLI。
- 目标是沉淀“视频理解前应该如何前处理”的通用流程，而不是记录某个具体项目。

## Verified Facts
- `ffprobe` 官方文档明确支持机器可读输出，适合在任何后续理解前先建立结构化元数据基线。
- FFmpeg 官方 filters 文档明确提供 `fps` 等视频采样能力，说明抽帧、降采样、时间轴裁剪适合作为独立前处理步骤，而不是必须在理解阶段临时完成。
- PyAV 官方文档明确提醒：如果 `ffmpeg` 命令就能完成任务，PyAV 反而可能增加复杂度；只有需要深入 frame/packet/container 层时才值得引入。
- 在样本 repo 中，命令被拆成 `doctor`、`probe`、`extract-audio`、`sample-frames`、`transcribe`，说明“分步工件化”天然适合 CLI 设计，而不是做成一个黑盒 `analyze` 命令。

## Recommendation
- 默认推荐的分层：
  - 第 1 层，能力探测：先确认本机能做什么，避免后续步骤在中途失败。
  - 第 2 层，元数据探测：先拿到 duration、streams、分辨率、是否有音轨等基础事实。
  - 第 3 层，媒体规范化：只把后续理解依赖的媒介变成标准形式，例如 16k 单声道 wav、统一命名的 jpg 帧。
  - 第 4 层，可选增强：仅在需求明确时再加 ASR、OCR、VAD、场景切分、词级时间戳等昂贵步骤。
  - 第 5 层，工件清单：统一输出 manifest/JSON，让上层 agent 只消费路径和结构化字段，不直接依赖底层命令细节。
- 默认步骤顺序：
  1. `doctor` 或 capability check
  2. `probe`
  3. 决策分支：是否需要音频、帧、字幕、OCR、场景切分
  4. `extract-audio`
  5. `sample-frames`
  6. 可选 `transcribe`
  7. 输出工件 manifest

## Applicable Scenarios
- 需要让 agent、多模态模型或人工分析复用同一批中间工件。
- 视频较大、成本较高，不希望每次从原始文件重新计算。
- 需要把“媒体处理失败”和“理解失败”区分开。
- 需要支持多种后续任务，例如摘要、检索、审核、字幕、片段标注。

## Non-Applicable Scenarios
- 一次性脚本，且不会复用中间产物。
- 实时流式处理，延迟要求高到无法接受离线工件化。
- 已有成熟媒体平台统一产出元数据、缩略图、字幕和场景信息。

## Tradeoffs And Risks
- 前处理层做得太重，会把“理解前置”误做成“预先计算一切”，导致成本和复杂度飙升。
- 抽帧如果只按固定 `fps` 做，容易漏掉场景切换或关键瞬间；但一开始就引入复杂场景切分，也会让默认链路过重。
- 音频规范化如果固定为单一路径，可能不适合保真要求高或多音轨保留要求强的场景。
- 如果没有显式 manifest，上层 agent 容易重新推断工件含义，造成隐式耦合。

## Implementation Notes
- 必做项：
  - 能力探测
  - 元数据探测
  - 标准化输出命名
  - 结构化 manifest
- 可选项：
  - ASR：只有在确实需要文本层时才开启
  - OCR：只有在视频信息大量来自画面文字时开启
  - 场景切分：只有在要做片段级理解、索引或检索时开启
  - 词级时间戳 / diarization / VAD：只有在字幕编辑、说话人级分析、精确对齐时开启
- 推荐的输出结构：
  - `metadata.json`
  - `audio.wav`
  - `frames/`
  - `transcript.txt|srt`
  - `manifest.json`
- 推荐的控制原则：
  - 先最小化，再增强
  - 先离散命令，再组合工作流
  - 先工件契约，再理解策略

## Open Questions
- 是否需要把场景切分提升为默认能力，而不是可选增强。
- 是否需要支持“片段级前处理”，避免长视频一次性全量处理。

## Related Knowledge
- [local-media-artifact-pipeline.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/patterns/local-media-artifact-pipeline.md)
- [agent-oriented-cli-tooling.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/patterns/agent-oriented-cli-tooling.md)
- [build-agent-cli-from-sample-repo.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/workflows/build-agent-cli-from-sample-repo.md)

## Evidence And Sources
- Sample repo evidence:
  - `/Users/chijiaduo/develop/media-extract/src/cli.ts`
  - `/Users/chijiaduo/develop/media-extract/src/commands/probe.ts`
  - `/Users/chijiaduo/develop/media-extract/src/commands/extract-audio.ts`
  - `/Users/chijiaduo/develop/media-extract/src/commands/sample-frames.ts`
  - `/Users/chijiaduo/develop/media-extract/src/commands/transcribe.ts`
- External sources:
  - [FFmpeg ffprobe Documentation](https://ffmpeg.org/ffprobe.html)
  - [FFmpeg Filters Documentation](https://ffmpeg.org/ffmpeg-filters.html)
  - [PyAV Documentation](https://pyav.org/docs/develop/index.html)
