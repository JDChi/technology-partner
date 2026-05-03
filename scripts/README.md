# Scripts

This directory is the first automation layer for `technology-partner`.

## Purpose
- Hold small, focused automation scripts that reduce repeated knowledge-work chores.
- Prefer scripts here before introducing a formal CLI.

## Current Policy
- Start with standalone scripts.
- Keep each script narrow and task-specific.
- Avoid inventing a command surface too early.
- Revisit a dedicated CLI only after scripts show repeated patterns worth unifying.

## Likely Early Candidates
- knowledge entry scaffolding
- knowledge index sync
- knowledge consistency checks
- GitHub stars analysis/export helpers

## Current Script
- `knowledge_index.py`: create new knowledge entries and rebuild `knowledge/index.json`

## Migration Rule
- If script count, shared logic, and argument patterns grow enough, promote the proven subset into a real CLI later.
