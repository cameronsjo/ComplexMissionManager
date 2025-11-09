# Complex Mission Manager - Intelligent Multi-Level Task Decomposition and Parallel Execution System

- Version: 1.0.1

A powerful Claude Code Plugin that can automatically decompose complex tasks into groups that can be executed in parallel and efficiently complete them through multi-level agent collaboration.

## Author

LostAbaddon
- Email: lostabaddon@gmail.com
- Website: https://lostabaddon.github.io/

## Features

### 🎯 Core Capabilities

- **Intelligent task decomposition**: Automatically analyzes complex requests and breaks them into task groups that can run in parallel
- **Multi-level agent collaboration**: A three-layer agent architecture that keeps execution efficient
- **Parallel task execution**: Maximizes parallel capacity to improve throughput
- **Automatic Git branch management**: Automatically creates and switches to a dedicated development branch inside Git repositories
- **Complete execution logs**: `WorkLog.md` tracks the entire execution process for easy auditing and troubleshooting

### 🏗️ Three-Layer Agent Architecture

#### Task Assigner (`task-assigner`)
- Receives the user's complex mission
- Analyzes task dependencies and resource conflicts
- Decomposes the mission into parallelizable task groups
- Launches multiple task planners in parallel
- Aggregates the outcomes from all task groups

#### Task Planner (`task-planner`)
- Receives the detailed information for a parallel task group
- Manages Git branches (`auto_develop_YYYY_MM_DD`)
- Creates and maintains the execution log `WorkLog.md`
- Breaks the group into atomic subtasks
- Sequentially invokes the task executor for each subtask
- Reviews the final results and produces a briefing

#### Task Executor (`task-executor`)
- Executes specific atomic subtasks
- Logs the process in `WorkLog.md` as a "teammate"
- Strictly adheres to the working directory constraints
- Reports results back to the task planner

### 📋 Principles for Task Decomposition

#### Tasks that can be run in parallel
- ✅ Read-only operations (file reads, web searches, web page analysis)
- ✅ Modifications to files located in different directories
- ✅ Fully independent tasks that do not affect each other

#### Tasks that cannot be run in parallel
- ❌ Tasks that may modify the same file
- ❌ Tasks with explicit dependencies
- ❌ Tasks that require shared state

### 🔄 Workflow

```
User submits a complex mission
        ↓
Task assigner analyzes and splits into parallel task groups
        ↓
Parallel launch of multiple task planners ────┬──── Task Group 1
                                            ├──── Task Group 2
                                            └──── Task Group 3
        ↓
Each task planner:
  1. Switches Git branches
  2. Creates WorkLog.md
  3. Decomposes into subtasks
  4. Sequentially invokes SubAgent C ────┬──── Subtask 1
                                       ├──── Subtask 2
                                       └──── Subtask 3
  5. Reviews the results and prepares a briefing
        ↓
Task assigner aggregates all briefings
        ↓
Reports the execution results to the user
```

## Use Cases

### Scenario 1: Information gathering and documentation
```
User: "Collect the latest information about AI large language models and tidy up the project documentation at the same time."

Decomposed into:
- Task Group 1: AI large model research (network operations)
- Task Group 2: Project documentation cleanup (local file operations)
```

### Scenario 2: Full-stack web development
```
User: "Build a blog website with both frontend and backend."

Decomposed into:
- Task Group 1: Backend development (`backend/` directory)
- Task Group 2: Frontend development (`frontend/` directory)
```

### Scenario 3: Multi-module feature development
```
User: "Add user authentication, data analytics, and notification system modules."

Decomposed into:
- Task Group 1: Authentication module (`auth/` directory)
- Task Group 2: Analytics module (`analytics/` directory)
- Task Group 3: Notification system (`notifications/` directory)
```

## Highlight Features

### Automatic Git Branch Management

Each task group automatically:
1. Checks whether the working directory is a Git repository
2. If so, creates or switches to the `auto_develop_YYYY_MM_DD` branch
3. Executes all operations on that branch
4. If it is not a Git repository, skips Git operations and proceeds

**Note**: The system never forces non-Git directories to be initialized as repositories.

## Overall Status
- Total task groups: 3
- Completed successfully: 3
- Partially completed: 0
- Failed: 0

## Task Group Details

### Task Group 1: Authentication module development
**Status**: Success

**Achievements**:
- Created the foundational files for the authentication module
- Implemented login and registration
- Added JWT token verification

**Deliverables**:
- `auth/index.js`
- `auth/middleware.js`
- `auth/utils.js`

---

{Other task groups...}
```

## Installation

Copy this plugin into the Claude Code `plugins` directory:

```bash
cp -r ComplexMissionManager ~/.claude/plugins/
```

Alternatively, add it to your project's `.claude/plugins/` directory.

## Configuration

No extra configuration is required—just install and start using it.

## Technical Architecture

### Agent Communication Flow

```
task-assigner
    ↓ (parallel invocation)
task-planner × N
    ↓ (sequential invocation)
task-executor × M
```

## Best Practices

### 1. Provide clear task descriptions

Include details such as:
- Concrete objectives
- Constraints
- Expected deliverables
- Quality requirements

### 2. Choose working directories wisely

- Assign different directories for different types of tasks
- Avoid multiple tasks modifying the same files
- Prefer absolute paths over relative paths

### 3. Fully leverage parallelism

- Identify tasks that can safely run in parallel
- Split independent work into separate task groups
- Avoid forcing decomposition when dependencies exist

### 4. Review execution logs

- Check `WorkLog.md` for detailed progress
- Use the logs to diagnose issues
- Refine task descriptions based on the logs

## Notes

### ⚠️ Git operations

- Only perform Git commands when the directory is already a Git repository
- Never force-init a repository
- Branch names always follow the `auto_develop_YYYY_MM_DD` pattern

### ⚠️ File operations

- All write operations by the task executor must stay within the working directory
- Read operations are unrestricted and may access any location
- Avoid modifying files outside the assigned working directory

### ⚠️ Task decomposition

- Do not over-split simple tasks
- A single task can be a valid decomposition result
- Prioritize independence over parallelism

## Automation

The repository includes a scheduled GitHub Actions workflow that syncs the latest
changes from the original project, translates any non-English content, and opens a
pull request targeting the `language/english` branch. The translation step uses
OpenAI Codex so that Markdown prose is rendered in polished, natural English and
the workflow automatically approves and merges successful updates.

To enable the automation:

1. Create the `language/english` branch in the remote repository (a one-time
   setup). Future workflow runs will fast-forward or create the branch as needed.
2. Create a repository variable named `UPSTREAM_REPO` whose value is the
   `<owner>/<repo>` slug of the original project (for example
   `lostabaddon/ComplexMissionManager`).
3. Optionally provide `UPSTREAM_BRANCH` if the upstream default branch is not
   `main`.
4. Add an `OPENAI_API_KEY` secret with access to Codex (`code-davinci-002`). The
   workflow uses this key to translate and polish documentation segments.

Manual runs are available from the **Actions** tab through the `Auto translate
upstream content to English` workflow.

## License

MIT License — see the [LICENSE](LICENSE) file for details.

## Contributing

Issues and pull requests are welcome!

---

## Marketplace

This project is listed on the [self-hosted Marketplace](https://github.com/lostabaddon/CCMarketplace). More plugins will be added there over time—stay tuned!

---

## Changelog

### v1.0.0 (2025-11-03)
- Initial release
- Implements the three-layer agent architecture
- Supports task decomposition and parallel execution
- Automatic Git branch management
- `WorkLog.md` execution logging
