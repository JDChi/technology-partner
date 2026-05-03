# technology-partner

This project is a persistent workspace for a Codex-based technology partner.

Its purpose is to support conversations like:
- discussing technical architecture and implementation strategy
- reading repositories and turning findings into reusable notes
- comparing方案, tradeoffs, workflows, and suitable scenarios
- accumulating a practical knowledge base that can be refined over time

## How To Use

Open this project in Codex and talk to it as your technical partner.

Typical prompts:
- "帮我看看这个仓库，理解一下整体架构。"
- "我想做一个 X，先从知识库里看看有没有类似方案。"
- "帮我比较 A 和 B 两种技术路线，给出建议。"
- "把我们刚讨论的方案整理进知识库。"
- "检查知识库里关于这个主题的内容，有冲突就帮我更新。"

## Project Structure

- `AGENTS.md`: persistent behavior and collaboration rules for the agent
- `knowledge/index.json`: machine-readable knowledge index for agent-first discovery
- `knowledge/`: long-term knowledge base
- `scripts/`: lightweight automation scripts for knowledge work
- `templates/`: reusable document templates for capturing durable knowledge

## Expected Working Loop

1. Read prior knowledge first.
2. Inspect repositories or supporting files when needed.
3. Produce a recommendation or structured analysis.
4. Write the reusable parts back into `knowledge/`.
5. Keep the machine index and evolution log current.

## Notes

- This project is designed to accumulate reusable technical knowledge, not just session notes.
- The agent should prefer refinement and consolidation over creating many overlapping files.
