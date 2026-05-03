# Local Media Artifact Pipeline

## Summary
- 推荐把“媒体理解”拆成两层：先做稳定的媒体工件提取，再做上层分析或 agent 推理。默认方案是 `ffprobe/ffmpeg` 负责探测、转码、抽帧，ASR 后端按运行环境选择 `mlx-whisper`、`faster-whisper` 或 `whisper.cpp`。这类方案适合先把视频变成可复用工件，再交给后续系统处理。

## Context
- 来源样本：`media-extract` 这类本地 CLI 项目。
- 目标不是记录某个项目，而是沉淀“本地媒体预处理应该怎么分层、选什么库、在什么场景下用”的通用判断。

## Verified Facts
- `ffprobe` 官方文档明确支持机器可读输出，适合做容器、流和格式探测。
- PyAV 官方文档明确说明：如果 `ffmpeg` 命令本身就能完成任务，PyAV 反而可能更麻烦；它更适合需要直接访问 container、stream、packet、frame 的场景。
- `faster-whisper` 官方 README 明确说明它基于 CTranslate2，并声称相对 `openai/whisper` 更快、占用更少内存；同时它通过 PyAV 解码音频，不依赖系统安装 `ffmpeg`。
- `mlx_whisper` 在 Apple 的 MLX Whisper 示例中提供 CLI 和 Python API，适合 Apple Silicon 上的本地转录。
- `whisper.cpp` 官方 README 明确强调可移植性、量化、CPU-only 和多种 GPU/硬件后端支持，适合强离线、低依赖或跨平台分发。
- OpenAI 官方 `whisper` 仓库是 Whisper 模型的参考实现，支持转录、翻译和语言识别，但它依赖系统安装 `ffmpeg`。

## Recommendation
- 默认推荐：
  使用 `ffprobe/ffmpeg` 作为媒体工件层的基础能力，再按 ASR 场景挑选后端。
- 库与适用场景：
  - `ffprobe`: 默认元数据探测。适合任何需要稳定读取 duration、stream、codec、bitrate、尺寸的流程。
  - `ffmpeg`: 默认转码、抽音频、抽帧。适合“处理动作明确”的流水线任务。
  - PyAV: 只有在你需要在 Python 内部逐帧、逐包、逐流处理时再用。比如自定义采样策略、和 NumPy/Pillow 深度联动。
  - `mlx-whisper`: Apple Silicon 本地单机优先。适合个人工作站、本地 agent、低运维链路。
  - `faster-whisper`: 跨平台本地/服务端优先。适合 Linux GPU、NVIDIA 服务器、希望通过 Python 服务封装 ASR 的场景。
  - `whisper.cpp`: 强离线、边缘设备、可执行分发优先。适合对部署独立性和硬件适配要求很高的场景。
  - OpenAI `whisper`: 作为参考实现、研究基线或兼容性起点可以用，但通常不是生产默认首选。

## Applicable Scenarios
- 需要先把视频变成结构化工件，再交给 agent 或下游系统分析。
- 需要离线、本地、可控的数据处理链路。
- 需要把“媒体提取”与“内容理解”解耦，避免每次都从原始视频重复计算。
- 需要一个可脚本化、可批处理、可复用的 CLI 或 worker。

## Non-Applicable Scenarios
- 只想做一次性、低可靠性的个人脚本，且不需要稳定的 JSON 契约。
- 主要需求是实时直播识别、低延迟流式字幕，而不是离线文件处理。
- 已经有成熟云媒体平台统一完成转码、缩略图、ASR，不需要再自建本地工件层。

## Tradeoffs And Risks
- `ffmpeg` shell-out 方案实现快、可移植，但错误处理、超时控制、进程取消、输出目录治理需要自己补齐。
- 本地 ASR 的可移植性差异很大。Apple Silicon、Linux GPU、纯 CPU 环境的最优库并不相同。
- 默认输出目录如果只按文件名或 stem 组织，容易产生工件冲突、陈旧抽帧残留、不同输入互相覆盖的问题。
- ASR 模型缓存、依赖探测、首次运行体验，是这类工具的主要可用性成本。

## Implementation Notes
- 推荐的默认流程：
  1. `doctor`: 先探测环境和模型状态。
  2. `probe`: 读取元数据，决定后续分支。
  3. `extract-audio`: 统一出规范音频，例如单声道、16k wav。
  4. `sample-frames`: 生成代表性帧，供视觉检查或后续多模态流程使用。
  5. `transcribe`: 仅在需要文本层时启用。
  6. 上层系统消费 JSON 输出和工件路径，不直接耦合底层命令细节。
- 建议把“提取层”输出稳定为 JSON 契约，把“解释层”放在单独步骤中。
- 建议输出目录至少包含输入文件哈希或规范化绝对路径摘要，不要只用文件 stem。
- 如果是 Node CLI，进程封装可以考虑从原生 `spawnSync` 升级到 `execa` 一类库，以获得更好的错误对象、跨平台行为和异步控制。

## Open Questions
- 是否需要把说话人分离、词级时间戳、VAD 作为一等能力；如果需要，需要单独评估更高层封装，而不是只靠基础 Whisper CLI。
- 未来是以本地 CLI 为主，还是会演进为服务端 worker；这会影响 ASR 后端默认选择。

## Related Knowledge
- [repo-to-generalized-guidance.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/workflows/repo-to-generalized-guidance.md)

## Sources
- [FFmpeg ffprobe Documentation](https://ffmpeg.org/ffprobe.html)
- [PyAV Documentation](https://pyav.org/docs/develop/index.html)
- [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- [ml-explore/mlx-examples Whisper README](https://github.com/ml-explore/mlx-examples/blob/main/whisper/README.md)
- [ggml-org/whisper.cpp](https://github.com/ggml-org/whisper.cpp)
- [openai/whisper](https://github.com/openai/whisper)
