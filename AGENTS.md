# Project Rules & Guidelines

## Core Philosophy: Ponytail (Level: Full)
- **Lazy Senior Dev**: The best code is the code never written. No over-engineering.
- **The Ladder**:
  1. Does this need to exist? If speculative/YAGNI -> skip it.
  2. Already in codebase? Reuse it.
  3. Standard library does it? Use stdlib.
  4. Native platform feature covers it? Use native (CSS over JS, HTML over libs, DB constraints over app logic).
  5. Installed dependency solves it? Use it. Do not install new packages when existing tools or a few lines of code suffice.
  6. Can it be one line? One line.
  7. Only then: minimal code that works.
- **Diffs & Architecture**:
  - Smallest working diff.
  - No speculative abstractions (no single-implementation interfaces, no unused factories/configs).
  - Deletion over addition.
  - Bug fixes must hit root cause, not symptom patching.
  - Mark intentional shortcuts with `# ponytail: <reason>, upgrade when <condition>`.

## DrawStory AI Context
- **Output Format**: 9:16 vertical video (1080x1920), 30fps.
- **Sync**: Storyboard timing strictly syncs to TTS audio length.
- **Async**: Keep heavy video/CV rendering in background workers; never block FastAPI HTTP endpoints.
