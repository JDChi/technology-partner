# When To Use MLX-Whisper

## Summary
- `mlx-whisper` 适合作为 Apple Silicon 本地 ASR 的默认优先候选，前提是我们要的是“本机离线转录能力”，而不是跨平台统一部署。它比“简单调用 Whisper 模型”更完整：同时提供 CLI 和 Python API，支持自动语言检测、翻译、词级时间戳、clip 级裁剪和多种输出格式。但它也明显绑定 MLX 运行时和本地设备能力，因此不应把它当作通用跨环境 ASR 基座。

## Context
- 这份笔记用于回答两个问题：
  - `mlx-whisper` 到底是什么能力边界
  - 在我们的方案里，它应该处于什么位置

## Verified Facts
- 官方 README 说明它是基于 MLX 的 Whisper 实现，面向 Apple silicon，并通过 Hugging Face Hub 使用模型。
- PyPI 当前最新版本是 `0.4.3`，发布时间为 2025-08-29，要求 Python >= 3.8。
- 官方 README 说明它同时提供：
  - CLI：`mlx_whisper audio_file.mp3`
  - Python API：`mlx_whisper.transcribe(...)`
- 官方 README 说明默认模型是 `mlx-community/whisper-tiny`，并且 `path_or_hf_repo` 可以指向 Hugging Face 上的 MLX Whisper 模型，模型会自动下载。
- 安装后的 `cli.py` 显示 CLI 支持：
  - 输出格式：`txt`、`vtt`、`srt`、`tsv`、`json`、`all`
  - 任务：`transcribe`、`translate`
  - `--language`
  - `--word-timestamps`
  - `--clip-timestamps`
  - `--initial-prompt`
  - 多个输出排版相关参数
- 安装后的 `transcribe.py` 显示：
  - `transcribe()` 默认支持自动语言检测
  - 支持 `word_timestamps`
  - 支持 `clip_timestamps`
  - 支持 `condition_on_previous_text`
  - 通过 `ModelHolder` 在同一进程内复用已加载模型
- 当前本机环境中，`python3 -m pip show mlx-whisper` 显示已安装 `mlx-whisper 0.4.3`。
- 当前 Codex 会话里直接运行 `mlx_whisper -h` 会在导入阶段报错：`No Metal device available`。这是一个本地验证事实，说明在当前 headless/sandboxed 会话里它拿不到所需设备能力。

## Recommendation
- 默认推荐把 `mlx-whisper` 放在这个位置：
  - Apple Silicon 单机、本地 agent、本地工作流：优先候选
  - 跨平台服务端、Linux GPU、容器化统一部署：不要当默认首选
- 在我们的系统里，推荐把它当成“后端能力”而不是“系统契约”：
  - 对外暴露稳定的 `transcribe` 接口
  - 内部后端可以是 `mlx-whisper`
  - 不要把上层工具直接绑定到它的默认模型、默认输出命名或自动下载行为

## Applicable Scenarios
- 主要运行环境是 Apple Silicon Mac。
- 需要本地离线转录，不想走云服务。
- 希望 agent 既能 shell 调 CLI，也能在 Python 内直接调用 API。
- 希望拿到词级时间戳、翻译或 clip 级处理能力。

## Non-Applicable Scenarios
- 要求同一套后端在 Linux、Windows、容器和 CI 环境稳定一致。
- 需要纯服务端、大规模批处理、多租户部署。
- 当前运行环境经常是 headless、sandboxed、拿不到 Metal/本地设备能力。

## Tradeoffs And Risks
- 优点：
  - 对 Apple Silicon 本地体验友好
  - 能力比“只给 txt 输出”的极简 CLI 丰富很多
  - 有 API，不一定非得 shell out
  - 同进程模型复用意味着服务化封装时有潜力减少重复加载成本
- 风险：
  - 设备环境依赖明显，不是“装上 pip 就哪都能跑”
  - 官方默认模型是 `tiny`，如果我们需要更高质量，必须在包装层显式指定模型
  - 自动下载模型虽然方便，但会让首次运行行为、缓存路径和可重复性变得更隐式
  - 如果我们只走 CLI 模式，会浪费它的 API 和进程内模型复用优势

## Implementation Notes
- 对我们当前方向的建议：
  - 如果继续做本地 Mac 优先工具，`mlx-whisper` 可以作为默认后端保留。
  - 但包装层不要沿用它的默认模型，应该显式指定我们自己的默认值。
  - 如果后面要做批量转录或长驻 worker，优先评估直接调用 Python API，而不是每次重新起一个 `mlx_whisper` 子进程。
  - 如果需要跨平台后端切换，应该把它放在统一 ASR provider 接口后面。
- 对 `media-extract` 样本的一个重要修正：
  - `media-extract` 当前把“默认 medium 且不自动下载”当作系统策略。
  - 这不是 `mlx-whisper` 的原生默认行为，而是我们包装层的有意收敛。

## Open Questions
- 对我们来说，后续更重要的是“单机体验最好”还是“后端统一可迁移”。
- 如果需要批处理/守护进程模式，是否应直接绕过 CLI，改用 Python API 持久化加载模型。

## Related Knowledge
- [local-media-artifact-pipeline.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/patterns/local-media-artifact-pipeline.md)
- [video-understanding-preprocessing-pipeline.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/patterns/video-understanding-preprocessing-pipeline.md)
- [agent-oriented-cli-tooling.md](/Users/chijiaduo/develop/my-agents/technology-partner/knowledge/patterns/agent-oriented-cli-tooling.md)

## Evidence And Sources
- Local evidence:
  - `python3 -m pip show mlx-whisper`
  - `mlx_whisper -h` in the current Codex session
  - `/Users/chijiaduo/Library/Python/3.14/lib/python/site-packages/mlx_whisper/cli.py`
  - `/Users/chijiaduo/Library/Python/3.14/lib/python/site-packages/mlx_whisper/transcribe.py`
- External sources:
  - [mlx-examples Whisper README](https://github.com/ml-explore/mlx-examples/blob/main/whisper/README.md)
  - [mlx-whisper on PyPI](https://pypi.org/project/mlx-whisper/)
  - [MLX README](https://github.com/ml-explore/mlx)
