# Complex Mission Manager - Intelligent Multi-Level Task Decomposition and Parallel Execution System

- Version: 1.0.1

A powerful Claude Code Plugin that automatically decomposes complex tasks into task groups that can run in parallel and orchestrates them through multi-level agents for efficient completion.

## Author

LostAbaddon
- Email: lostabaddon@gmail.com
- Website: https://lostabaddon.github.io/

## Features

### 🎯 Core Capabilities

- **Intelligent Task Decomposition**: Automatically analyzes complex tasks and splits them into parallelizable task groups
- **Multi-level Agent Collaboration**: A three-tier agent architecture keeps execution efficient
- **Parallel Task Execution**: Maximizes parallel capacity to boost throughput
- **Automatic Git Branch Management**: Automatically creates and switches to a dedicated development branch inside git repositories
- **Comprehensive Execution Log**: WorkLog.md captures the entire execution process for traceability and debugging

### 🏗️ Three-Tier Agent Architecture

#### Task Assigner (task-assigner)
- Receives the user's complex task
- Analyzes task dependencies and resource conflicts
- Splits the work into task groups that can run in parallel
- Launches multiple task execution managers in parallel
- Consolidates the results from every task group

#### Task Planner (task-planner)
- Receives the details for each parallel task group
- Manages Git branches (auto_develop_YYYY_MM_DD)
- Creates and maintains the WorkLog.md execution log
- Decomposes the work into atomic subtasks
- Sequentially invokes the subtask executor to complete each subtask
- Reviews completion status and produces an execution brief

#### Task Executor (task-executor)
- Executes concrete atomic subtasks
- Records progress in WorkLog.md as the "crew member"
- Strictly follows working directory constraints
- Reports results back to the task execution manager

### 📋 Task Decomposition Guidelines

#### Tasks Suitable for Parallel Execution
- ✅ Read-only operations (file reads, web searches, page analysis)
- ✅ Modification work on files located in different directories
- ✅ Tasks that are entirely independent and have no cross-impact

#### Tasks That Must Remain Sequential
- ❌ Tasks that may modify the same file
- ❌ Tasks with explicit dependencies
- ❌ Tasks that require shared state

### 🔄 Workflow

```
User submits a complex task
        ↓
task-assigner analyzes and splits into parallel task groups
        ↓
Parallel launch of task-planner instances ────┬──── Task Group 1
                                            ├──── Task Group 2
                                            └──── Task Group 3
        ↓
Each task-planner:
  1. Switches Git branches
  2. Creates WorkLog.md
  3. Decomposes subtasks
  4. Sequentially calls SubAgent C ────┬──── Subtask 1
                                     ├──── Subtask 2
                                     └──── Subtask 3
  5. Reviews results and prepares a brief
        ↓
task-assigner aggregates every brief
        ↓
Reports the outcome to the user
```

## Use Cases

### Scenario 1: Research and Documentation
```
User: "Collect the latest information about AI foundation models while organizing the project documentation"

Split into:
- Task Group 1: Collect AI foundation model information (network operations)
- Task Group 2: Organize project documentation (local file operations)
```

### Scenario 2: Full-Stack Web Development
```
User: "Build a blog website with both frontend and backend"

Split into:
- Task Group 1: Backend development (backend/ directory)
- Task Group 2: Frontend development (frontend/ directory)
```

### Scenario 3: Developing Multiple Modules
```
User: "Add user authentication, data analytics, and notification system modules"

Split into:
- Task Group 1: User authentication module (auth/ directory)
- Task Group 2: Data analytics module (analytics/ directory)
- Task Group 3: Notification system (notifications/ directory)
```

## Highlighted Capabilities

### Automatic Git Branch Management

Each task group automatically:
1. Checks whether the working directory is a git repository
2. Creates or switches to the `auto_develop_YYYY_MM_DD` branch when inside a repository
3. Performs all operations on that branch
4. Skips branch operations and continues if the directory is not a repository

**Note**: It never initializes a non-git directory as a repository.

### WorkLog.md Conversation Workflow

Every task group generates `WorkLog.md`, capturing the full execution trace:

```markdown
# Work Log

**Task Title**: Build the user authentication module
**Start Time**: 2025-11-03 14:30:00
**Working Directory**: /path/to/project

---

## Task Details
{Detailed task description}

---

## Execution Log

### Captain: Task Started
Begin executing the task and prepare to decompose subtasks.

### Captain: Subtask Decomposition Completed
The task has been split into the following subtasks:
1. Create the authentication module boilerplate
2. Implement the login feature
3. Implement the registration feature
...

### Crew Member: Subtask Execution Started
{Subtask execution process}

### Crew Member: Subtask Execution Completed
{Completion notes}

### Captain: Task Completed
All subtasks are finished and the quality check passed.
```

### Execution Report

A structured report is generated after execution:

```markdown
# Task Execution Report

## Summary
- Total task groups: 3
- Completed: 3
- Partially completed: 0
- Failed: 0

## Task Group Details

### Task Group 1: User authentication module
**Status**: Success

**Completed work**:
- Created the module boilerplate
- Implemented login and registration
- Added JWT token validation

**Deliverables**:
- auth/index.js
- auth/middleware.js
- auth/utils.js

---

{Other task groups...}
```

## Installation

Copy this plugin to the Claude Code plugins directory:

```bash
cp -r ComplexMissionManager ~/.claude/plugins/
```

Or add it to your project's `.claude/plugins/` directory.

## Configuration

No additional configuration is required; it is ready to use after installation.

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

### 1. Write Precise Task Descriptions

Provide detailed task descriptions that include:
- Specific objectives
- Constraints
- Expected outputs
- Quality requirements

### 2. Assign Working Directories Thoughtfully

- Use distinct working directories for different task types
- Avoid having multiple tasks modify the same file in one directory
- Use absolute paths instead of relative paths

### 3. Leverage Parallel Execution

- Identify tasks that can run in parallel
- Separate independent work into different task groups
- Avoid forcing decomposition when dependencies exist

### 4. Review Execution Logs

- Inspect WorkLog.md for the execution timeline
- Diagnose issues through the log
- Refine task descriptions based on findings

## Notes

### ⚠️ Git Operations

- Run git commands only when the working directory is a repository
- Never initialize a non-git directory
- Always follow the `auto_develop_YYYY_MM_DD` branch naming convention

### ⚠️ File Operations

- All write operations by SubAgent C must stay within the assigned working directory
- Read operations are unrestricted and can access any location
- Do not modify files outside the working directory

### ⚠️ Task Decomposition

- Do not over-decompose simple tasks
- A single task group is a valid result when appropriate
- Prioritize task independence over raw parallelism

## License

MIT License - see [LICENSE](LICENSE) for details

## Contributing

Issues and Pull Requests are welcome!

---

## Marketplace

This project is listed in the [self-hosted Marketplace](https://github.com/lostabaddon/CCMarketplace), which will continue to receive new plugins—stay tuned!

---

## Changelog

### v1.0.0 (2025-11-03)
- Initial release
- Implemented the three-tier agent architecture
- Added support for task decomposition and parallel execution
- Automated Git branch management
- WorkLog.md execution log
