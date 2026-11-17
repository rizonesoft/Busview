# AGENTS.md

This repository follows the Conclave-SDK 3-agent conventions.

## Goal

Ship Busview version 1: a driverless Windows hardware inventory that gives upgrade advice (RAM first), saves and compares snapshots, and explains BIOS beep codes, built in C++23 on the Resolute-SDK toolchain with the resolute-ui interface.

## This project

Busview is one tool of Rizonesoft's Resolute suite of Windows system utilities: it reads what hardware is inside a computer and says what to do about it. It is developed and released standalone, as one statically linked executable with a read-only SQLite database beside it, and is also bundled with the Resolute launcher (`rizonesoft/Resolute`), which imports it only when a distribution is built. Windows only: C++23 on llvm-mingw, CMake and Ninja, the suite's Direct2D UI library, Catch2 v3 for tests, Python for the database build.

| Path | Purpose |
| ---- | ------- |
| `src/`, `resources/`, `tests/` | The tool, its embedded resources and its Catch2 suites |
| `data/`, `tools/` | The database's text sources (each row sourced and dated) and the scripts that compile them |
| `sdk.json`, `sdk/` | The Resolute-SDK pin, and the SDK at that commit (not tracked; `pwsh scripts/sdk.ps1`) |
| `design/` | The interface contract `SPEC.md`, the working design it was written from, and its captures |
| `brand/`, `DESIGN.md` | The tool's identity, built by `python brand/build.py`, and its window's sections |
| `reference/beepcodes-au3/` | The AutoIt BiosCodes source the beep codes come from. Frozen: read, never edited |
| `todo/` | The plan. Read `todo/README.md` before authoring or implementing |

Commands that verify the work: `pwsh scripts/sdk.ps1 -Check` (the SDK is at the pin), `python brand/build.py --check` (the brand assets are current), `python scripts/todo-graph.py validate` and `plan --check` (the plan), and, once D00 T01 §1 and §2 have shipped, `pwsh scripts/build.ps1` and `pwsh scripts/check-all.ps1`.

Rules that are this project's own:

- **Shared code comes from the SDK and is never copied.** The UI library, the framework, the build policies and the toolchain are `sdk/`. If Busview needs a shared control or facility, it is added to Resolute-SDK and taken here by bumping `sdk.json`. A private settings writer, log writer, About dialog, button or progress bar is a defect. The Board diagram is the one surface of Busview's own, drawn on the SDK's render context and tokens.
- **`sdk/` is never edited here.** A change to it is made in the SDK's repository.
- **The window is `design/SPEC.md`, 1:1.** Every control, state and string there is built as written, and a difference is a defect or a commit that changes the contract, the design and the captures together and says why.
- **No kernel driver.** Version 1 reads everything from user mode. Nothing that needs ring 0 (sensors, SPD, model-specific registers) is added without the owner's decision.
- **Firmware is untrusted input.** Every table, EDID block and descriptor is parsed through `src/core/ByteReader.h`, and every parser has tests with truncated and malformed input under AddressSanitizer.
- **Nothing invented.** A value the machine did not report is absent, never guessed, and advice that lacks its facts says "not known" with the reason.
- **Busview changes nothing on the computer** except files the user asked for (snapshots, reports) in the user's own folders, written atomically and read back. Nothing leaves the computer, and exports hide identifying values by default.
- **Every database row carries its source and the date it was taken.** Maker-tested kit lists and proprietary finders are not copied.
- **Sections waiting on the SDK** carry the Need `sdk-framework`. It is removed when the SDK section they need has shipped and `sdk.json` pins a commit that has it.
- **The tool never depends at runtime** on another tool, on the launcher or on a suite-wide file.
- **Licence:** GPL v3. Resolute-SDK is MIT and may be linked; nothing GPL goes back into it.

## Working rules

- Verify files, routes, schemas, tools, and commands before relying on them. A path someone mentions is a hypothesis until it is on disk.
- Inspect existing patterns, imports, the package manager, the framework, and the test commands before editing. Do not infer architecture or tool schemas from memory when the repository can answer.
- Resolve a tool by capability before path. Prefer explicit config, then discovery, then a setup-required state. Store discovered paths only in ignored local config and never hardcode user-specific absolute paths.
- Prefer global or user-level tool installs. Add repo-scoped wrappers only when they encode project-specific behavior or reproducible commands.
- Real data only. Demo or seed data stays behind an explicit demo mode and is labeled as such.
- Run the relevant typecheck, lint, and tests after a change.
- Fix at the owning layer: a setting in its setting, behaviour in the code that produces it, data in the data. No output filters that hide a problem. Code changes end the report with a `Layer:` line.
- Markdown prose is never hard-wrapped: one line per paragraph and per list item. Every Markdown table row stays `<= 120` characters so raw `.md` files never wrap.
- Never use em dashes or en dashes anywhere: prose, code, comments, commit messages and generated files.
- Temporary files and full logs go to scratch, never the repository: the session scratchpad when one is given, otherwise the folder `paths.scratch` names in `.conclave/local.toml`, otherwise the operating system's temporary folder.

## Operating directive

How to work without waiting to be told. When to ask the operator is listed under Safety, and only there.

- A task assigned is a task authorised: do it, then report what was done, with the evidence.
- Never end a turn with a question or an offer when the next step is known and unblocked: take the step.
- Finish the follow-ups this session can do safely (a config value, a setup step, a check to run again) and report them done, never as a list left for the operator.
- Ask the operator only for what Safety lists: once, with the options and the one you recommend, and keep working on everything the answer does not change.
- Fix forward: a risk found later is filed as ordinary work that blocks nothing, and a red check is fixed at its cause, never skipped or bypassed.
- Build the simplest design that meets the request in full, and add a check, gate or prerequisite only for a failure that has happened or one that would lose data, spend money or expose something.
- An unattended run never asks the operator: it takes the industry-standard option, records the decision and what reversing it would cost in the run file and files an owner item; it halts only through the run's own pause mechanism, and pauses instead of proceeding only for data loss, a credential, shared infrastructure or a calculation that looks wrong.

## Safety

- Local reversible work in the repository needs no confirmation, and neither does work outside it that the task authorised and that can be undone (a config value, a setup step, a deploy the task asked for).
- Ask the operator once before anything that destroys or exposes something, or that needs business context the repository lacks: dropping or overwriting data, a force-push, deleting outside the repository, creating, rotating or exposing a credential, sending mail or a message to a person, a SQL write or a production change with real blast radius.
- When a command needs sudo, give the operator the exact command to run with `! sudo ...`. Never store the sudo password.
- Never print, log, or commit a secret value.

## Git

A project with a branch workflow replaces the first rule with its own; the others hold everywhere.

- Develop on the main branch: commit there, with no feature branch, unless the operator asks for a branch in that task.
- Before staging, read `git status --short` and enough of the diff to understand every dirty file: another session or a person may be editing.
- Commit a safe side change (small, not secret, not generated, not in conflict) with the next coherent commit; stop and say why before touching one that conflicts, holds a secret or looks unsafe or generated.
- Never discard changes with `git reset`, `checkout`, `restore` or `clean` unless asked for that exact cleanup.
- After a commit, confirm it landed with `git log --oneline -1` and `git status --short`, and never filter hook output in a way that hides an error.
- When work is finished, remove the worktrees you or a subagent created, delete branches that are merged or whose content is verifiably on main, and prune dead worktree records.
- Never delete an unmerged branch whose content is not verifiably on main without asking.

## Skills

- Antigravity skills live in `.agents/skills/<name>/`, Claude skills in `.claude/skills/<name>/`, and Codex skills in `.codex/skills/<name>/`, all as real files, never symlinks. Change all three together.
- Follow [Agent Skills and Rules Structure](./docs/agent-skills-and-rules-structure.md) before adding or moving skills.
- Name a skill for its capability, not with a project prefix.
- Each agent reads and runs only its own directory (`.agents/` for Antigravity, `.claude/` for Claude Code, `.codex/` for Codex) and never edits another agent's skills unless asked.

## Subagents

- Delegate mechanical subtasks to subagents. Claude subagents pin an explicit `model:`: Sonnet by default, and Opus (with a `model_rationale:`) only where judgment quality needs it.
- Subagents read and run; they never write. Every Claude subagent declares an explicit `tools:` list without Edit, Write, MultiEdit, NotebookEdit or `*`. The main loop makes every change and verifies what subagents return.
- Antigravity uses native `Orchestrator (Carbon)` (`gemini-pro-orchestrator`), which plans on Carbon (`<plan_execute_protocol>`), hands execution to Hydrogen via `exit_plan_mode`, manages its own effort (rejecting `--effort`), and provides built-in subagents (`self`, `research`, `image-generator`) without custom `.agents/agents/*.md` files or wrapper scripts. Codex has no subagent definitions: it runs mechanical subtasks in the main session.
- Haiku is only for near-mechanical work, at least 90% mechanical (read-only lookups, inventories, structural checks), whose output a script or the main loop verifies. Pin `claude-haiku-5-5` or later, declare `mechanical_share:` (90 to 100), point `haiku_replay:` at a record of a known-answer replay that showed no loss against Sonnet, and give it no edit tools. Never use Haiku for review, audit, research, security, debugging, diagnosis, planning or design.
- Run `node scripts/verify-agent-tiers.mjs` after adding or changing a Claude agent definition in `.claude/agents/`; it enforces these rules.

## TODO workflow

Plan and build through the TODO system: [docs/todo-workflow.md](./docs/todo-workflow.md).
