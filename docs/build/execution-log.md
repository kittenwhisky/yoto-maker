# Execution Log: Yoto Card Maker Build

## Parallelization Strategy

### Dependency graph

```
Phase 1: Scaffold (sequential — main agent)
    │
    ├──▶ Phase 2: catalog.py  ─┐
    ├──▶ Phase 3: download.py  ├──▶ Phase 5: Test ──▶ Phase 6: CLAUDE.md
    └──▶ Phase 4: cli.py      ─┘
         (parallel phases, each runs the Code → Test → Review loop below)
```

## Per-Phase Subagent Loop

Each of Phases 2, 3, 4 runs this 3-agent loop independently:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐  │
│  │ 1. Coder     │───▶│ 2. Tester    │───▶│ 3. Review │  │
│  │              │    │              │    │           │  │
│  │ Writes/fixes │    │ Runs tests   │    │ Compares  │  │
│  │ module code  │    │ Creates test │    │ test fail │  │
│  │              │    │ report       │    │ report vs │  │
│  │              │    │              │    │ PRD, plan │  │
│  └──────▲───────┘    └──────────────┘    │ & exec-log│  │
│         │                                │           │  │
│         │         Debug plan with        │ Creates   │  │
│         └────────── fix tasks ◀──────────│ debug plan│  │
│                                          └───────────┘  │
│                                                         │
│  Loop exits when:                                       │
│    ✓ All tests pass                                     │
│    ✓ Code matches PRD.md, plan.md, execution-log.md     │
└─────────────────────────────────────────────────────────┘
```

### Agent 1: Coder
- **Input**: Phase task description (first run) or debug plan from Reviewer (subsequent runs)
- **Action**: Writes or updates the module source code
- **Output**: Updated source files
- **CLAUDE.md**: If any files are added, renamed, or removed, update the Project Structure section in `CLAUDE.md` immediately

### Agent 2: Tester
- **Input**: The code written by Agent 1
- **Action**: Runs tests against the module, validates behavior
- **Output**: Test report — lists passed/failed tests with failure reasons

### Agent 3: Reviewer
- **Input**: Test report + PRD.md + plan.md + execution-log.md
- **Action**:
  1. Analyzes test failures and their root causes
  2. Checks code compliance with PRD.md, plan.md, execution-log.md
  3. Creates a debug coding plan with specific fix tasks
  4. Updates execution-log.md and plan.md if needed
- **Output**: Debug plan sent back to Agent 1 (Coder)
- **Loop exit**: If all tests pass and code matches requirements, marks phase complete

## Coordination: Main Agent Role

- The main agent orchestrates the overall flow:
  1. Executes Phase 1 (scaffold) directly
  2. Launches Phases 2, 3, 4 in parallel — each running its own Code→Test→Review loop
  3. Monitors all 3 phase loops via output files
  4. Updates the TodoWrite task list as each phase completes
  5. Only proceeds to Phase 5 (integration test) after all 3 loops exit successfully
  6. Executes Phase 6 (CLAUDE.md) after integration test passes

## Error Handling

- If a phase loop exceeds a reasonable iteration count (e.g., 3 cycles), the main agent intervenes directly
- The Reviewer agent's debug plan is specific and actionable — not vague directives
- The main agent does a final cross-module consistency check after all phases complete (e.g., cli.py imports match actual function signatures in catalog.py and download.py)

## Git Strategy

- GitHub repo created during Phase 1 scaffold (`gh repo create`)
- After each phase passes its Code→Test→Review loop, the main agent:
  1. Commits the phase's code to `main`
  2. Tags the commit (e.g., `phase-2-catalog`)
  3. Pushes to GitHub
- This means each phase is independently preserved even if later phases aren't complete yet

## Execution Timeline

| Step | Method | Agents | Git action |
|------|--------|--------|------------|
| Scaffold | Main agent | — | Commit + push + tag `phase-1-scaffold` |
| catalog.py | Parallel loop | Coder → Tester → Reviewer | Commit + push + tag `phase-2-catalog` |
| download.py | Parallel loop | Coder → Tester → Reviewer | Commit + push + tag `phase-3-download` |
| cli.py | Parallel loop | Coder → Tester → Reviewer | Commit + push + tag `phase-4-cli` |
| Integration test | Main agent | — | — |
| Docs (README + CLAUDE.md) | Main agent | — | Commit + push + tag `phase-6-docs` |
