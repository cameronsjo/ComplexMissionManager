---
description: Split the user-provided mission cluster into task groups that can execute in parallel, then hand them to worker agents for concurrent completion
argument-hint: "<task_descriptions>"
model: haiku
---

Use `complexMissionManager:task-assigner` to analyze, decompose, execute, and finally report on the large mission set described by `task_descriptions`.
