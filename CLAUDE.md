# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Summary

Python CLI tool that downloads audio from a YouTube playlist as MP3 files. User provides a playlist URL, the tool generates a CSV catalog for validation, then batch-downloads the validated tracks.

## Project Structure

```
yoto-maker/
├── CLAUDE.md                       # This file — AI assistant context
├── docs/
│   ├── build/
│   │   ├── PRD.md                  # Product requirements
│   │   ├── plan.md                 # Build plan with phases
│   │   └── execution-log.md       # Subagent workflow and execution strategy
│   └── chat/
│       └── decisions.md            # Key decisions with rationale
└── src/
    └── yoto_maker/
        ├── __init__.py
        ├── cli.py                  # Interactive menu entry point (InquirerPy)
        ├── catalog.py              # YouTube playlist → CSV extraction (yt-dlp)
        └── download.py             # CSV → MP3 batch download (yt-dlp + ffmpeg)
```

## Keeping This File Current

**This file must be updated whenever the project structure, commands, or conventions change.** This applies to the main agent, all subagents (Coder, Tester, Reviewer), and future chat sessions. If you add, rename, or remove a module, update the structure above immediately — do not defer to a later phase.

## Decision Tracking

When decisions are made during a chat session — such as technology choices, scope changes, architecture changes, or convention changes — append them to `docs/chat/decisions.md` before the session ends. Use the existing table format in that file.

## Project Documentation

- `docs/build/PRD.md` — Product requirements
- `docs/build/plan.md` — Build plan with phases
- `docs/build/execution-log.md` — Subagent workflow and execution strategy
- `docs/chat/decisions.md` — All key decisions with rationale

Review these files at the start of each session to understand project context.
