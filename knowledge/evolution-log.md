# Evolution Log

Track meaningful changes to the knowledge system here.

## 2026-04-30
- Initialized the `technology-partner` project.
- Established the durable knowledge layout under `knowledge/`.
- Defined the agent contract in `AGENTS.md`.
- Added templates to support future knowledge capture and refinement.

## 2026-05-03
- Added a reusable pattern note for local media artifact pipelines instead of storing repo-specific notes for `media-extract`.
- Added a workflow note to standardize how concrete repositories should be abstracted into generalized guidance.
- Added a video-understanding preprocessing pattern focused on minimal artifact generation before downstream analysis.
- Added an agent-oriented CLI tooling pattern and a sample-repo-to-pattern workflow for future tool repos.
- Added a scenario note for `mlx-whisper` covering its Apple Silicon fit, API/CLI surface, and environment caveats observed locally.
- Updated `AGENTS.md` to explicitly prefer authenticated `gh` evidence for GitHub remote-state questions and to call out the `gh-cli` skill.
- Added a decision record to keep automation script-first for now, plus a `scripts/` directory README to delay premature CLI design.
- Added `scripts/knowledge_index.py` and migrated the durable knowledge entry point from `knowledge/index.md` to `knowledge/index.json`.
- Added a pattern note that promotes `knowledge/index.json` from a usable implementation detail to an explicit agent-first knowledge index contract.
- Replaced a repo-specific evolution note with a generalized agent-workspace design-order pattern, to avoid binding durable knowledge to local machine paths and sample-specific structure.
