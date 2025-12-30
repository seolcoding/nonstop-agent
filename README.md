# Nonstop Agent

**Long-running autonomous agent harness for Claude** - A framework for building autonomous agents that work continuously across multiple sessions.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Overview

Nonstop Agent is a production-ready framework for running Claude-powered autonomous agents that can work continuously on complex projects. It implements best practices from Anthropic's engineering guidelines, including:

- **2-Agent Pattern**: Initializer agent sets up the project, Coding agents continue the work
- **State Persistence**: Progress survives across sessions via git + progress files
- **Defense-in-Depth Security**: Multi-layered security with sandbox, permissions, and command allowlists
- **Session Resumption**: Seamlessly continue work from previous sessions

## Inspiration & References

This project is inspired by and built upon:

1. **[Anthropic Engineering: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)**
   - 2-Agent pattern (Initializer + Coding)
   - Defense-in-depth security model
   - State persistence via git + progress files

2. **[Anthropic Claude Quickstarts - Autonomous Coding](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)**
   - Reference implementation for autonomous coding agents
   - `feature_list.json` pattern for tracking progress

3. **[Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)**
   - Official SDK for building Claude-powered agents
   - Hooks, permissions, and session management

## Installation

```bash
# Using uv (recommended)
uv add nonstop-agent

# Or using pip
pip install nonstop-agent
```

## Quick Start

### 1. Authentication

The agent uses Claude Code CLI for authentication:

```bash
# Login via Claude Code CLI
claude login

# Or set OAuth token directly
export CLAUDE_CODE_OAUTH_TOKEN="your-oauth-token"
```

### 2. Run the Agent

**New Project:**
```bash
# Create a new project with app_spec.txt
uv run nonstop-agent --project-dir ./my_project
```

**Existing Project:**
```bash
# Analyze existing codebase first
uv run nonstop-agent --project-dir ./existing_project --analyze-first
```

**Resume Previous Session:**
```bash
# Continue from where you left off
uv run nonstop-agent --project-dir ./my_project --resume
```

### 3. Command Line Options

```
--project-dir PATH      Directory for the project (default: ./project)
--model MODEL           Claude model to use (default: claude-sonnet-4-5-20250929)
--max-iterations N      Maximum number of iterations (default: unlimited)
--analyze-first         Analyze existing project before starting
--resume                Resume from the last session
--system-prompt TEXT    Custom system prompt for the agent
```

## How It Works

### Session Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    SESSION 1 (First Run)                     │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              INITIALIZER AGENT                           │ │
│  │  - Read app_spec.txt                                    │ │
│  │  - Create feature_list.json                             │ │
│  │  - Set up project structure                             │ │
│  │  - Git init and first commit                            │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 SESSION 2, 3, 4, ... (Continuation)          │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                CODING AGENT                              │ │
│  │  1. Orient: Read progress files                         │ │
│  │  2. Verify: Check existing features work                │ │
│  │  3. Implement: One feature at a time                    │ │
│  │  4. Test: Verify implementation                         │ │
│  │  5. Commit: Save progress to git                        │ │
│  │  6. Repeat                                              │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### State Files

| File | Purpose |
|------|---------|
| `app_spec.txt` | Original requirements (immutable) |
| `feature_list.json` | Feature checklist (source of truth) |
| `claude-progress.txt` | Session-by-session progress notes |
| `claude_session.json` | Session ID for resumption |
| Git history | Code changes and commit history |

### Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: OS-Level Sandbox                                   │
│  - Isolated bash command execution                          │
│  - Filesystem escape prevention                             │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: Filesystem Restrictions                            │
│  - Operations limited to project directory                  │
│  - Read, Write, Edit tools scoped                          │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: Command Allowlist                                  │
│  - Only explicitly permitted commands can run               │
│  - Extra validation for sensitive commands                  │
└─────────────────────────────────────────────────────────────┘
```

## Customization

### Custom System Prompt

```bash
uv run nonstop-agent --project-dir ./project \
  --system-prompt "You are an expert Python developer..."
```

### Programmatic Usage

```python
import asyncio
from pathlib import Path
from nonstop_agent import run_autonomous_agent

asyncio.run(
    run_autonomous_agent(
        project_dir=Path("./my_project"),
        model="claude-sonnet-4-5-20250929",
        max_iterations=10,
        analyze_first=True,
    )
)
```

### Extending Allowed Commands

```python
from nonstop_agent.security import add_allowed_command

# Add custom commands to the allowlist
add_allowed_command("docker")
add_allowed_command("cargo")
```

## feature_list.json Format

```json
[
  {
    "category": "functional",
    "description": "User can log in with email and password",
    "steps": [
      "Step 1: Navigate to login page",
      "Step 2: Enter email",
      "Step 3: Enter password",
      "Step 4: Click login button",
      "Step 5: Verify redirect to dashboard"
    ],
    "passes": false
  }
]
```

**Rules:**
- `description` and `steps` are **immutable** - never modify after creation
- Only change: `"passes": false` → `"passes": true` after verification
- Order by priority: core features first

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Special thanks to the Anthropic team for their excellent documentation on building effective agent harnesses and the Claude Agent SDK.
