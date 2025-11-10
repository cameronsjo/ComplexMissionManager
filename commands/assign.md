---
description: Decompose the user-provided task cluster into task groups that can run in parallel, then hand them to worker agents for concurrent completion
argument-hint: "<task_descriptions>"
model: haiku
---

Use `complexMissionManager:task-assigner` to analyze, decompose, execute, and report on the large task group described by `task_descriptions`.
