---
description: Generate project tree structure and save to documentation folder
model: haiku
allowed-tools: inherit
---

# Generate Project Tree Structure

Generate project tree structure and save to `docs` folder.

## Instructions

- Run the !`pwd` command to get the current working directory
- Run the !`tree` and the !`git ls-files` command to generate the project tree structure excluding the rules below
- Create or update the `docs/tree.md` file with the project tree structure
- Make sure to validate the project tree structure with the rules below and fix any errors. Every single file that is not excluded should be included in the output.

## Rules

- Exclude: node*modules, dist, build, .git, coverage, .turbo, .wrangler, .cache, .temp, tmp, .DS_Store, .vscode, .cursor, .idea, .claude, .factory, .worktrees, .rollup.cache, .tanstack, playwright-report*, test-results, _.log, _.tsbuildinfo, \_.map, \*.bak, worker-configuration.d.ts, pnpm-lock.yaml, cf-validation
- Remove all CLAUDE.md and AGENTS.md files from output
- Remove entire `tests/` folder from output
- Remove entire `docs/` folder from output
- Format as markdown with code block
