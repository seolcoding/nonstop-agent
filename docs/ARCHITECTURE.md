# Nonstop Agent Architecture Guide

Anthropic의 롱 러닝 에이전트 베스트 프랙티스 기반 아키텍처 상세 가이드입니다.

## Core Concepts

### 1. 2-Agent Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                    SESSION 1 (First Run)                     │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              INITIALIZER AGENT                           │ │
│  │  - app_spec.txt 읽기                                    │ │
│  │  - feature_list.json 생성                               │ │
│  │  - init.sh 생성                                         │ │
│  │  - 프로젝트 구조 설정                                   │ │
│  │  - Git 초기화 및 첫 커밋                                │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 SESSION 2, 3, 4, ... (Continuation)          │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                CODING AGENT                              │ │
│  │  1. 환경 파악 (git log, progress.txt)                   │ │
│  │  2. 기존 테스트 검증                                    │ │
│  │  3. 하나의 기능 선택 및 구현                            │ │
│  │  4. 테스트로 검증                                       │ │
│  │  5. feature_list.json 업데이트                          │ │
│  │  6. Git 커밋                                            │ │
│  │  7. claude-progress.txt 업데이트                        │ │
│  └─────────────────────────────────────────────────────────┘ │
│                              │                               │
│                              ▼                               │
│                     반복 (자동 재시작)                       │
└─────────────────────────────────────────────────────────────┘
```

### 2. State Persistence Mechanism

```
┌─────────────────────────────────────────────────────────────┐
│                    STATE PERSISTENCE                         │
├─────────────────────────────────────────────────────────────┤
│  feature_list.json    ← Feature checklist (Source of Truth) │
│  claude-progress.txt  ← Session-by-session progress notes   │
│  Git History          ← Code change history                 │
│  app_spec.txt         ← Original requirements (immutable)   │
└─────────────────────────────────────────────────────────────┘
```

### 3. Existing Project Analysis Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  EXISTING PROJECT ANALYSIS                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Step 1: Project Structure Analysis                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  - Read README.md, CLAUDE.md                           │ │
│  │  - Check package.json / pyproject.toml                 │ │
│  │  - Explore directory structure                         │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ↓                                   │
│  Step 2: Requirements Discovery                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  - Find docs/, specs/ documents                        │ │
│  │  - Collect GitHub Issues, TODO comments                │ │
│  │  - Reverse-engineer requirements from tests            │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ↓                                   │
│  Step 3: Run Tests (CRITICAL!)                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  npm test / pytest / uv run pytest                     │ │
│  │  - Identify passing/failing tests                      │ │
│  │  - Check test coverage                                 │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ↓                                   │
│  Step 4: Document Current State                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Record analysis results in claude-progress.txt        │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Authentication

Claude Agent SDK authenticates via the bundled Claude Code CLI.

| Environment Variable | Description |
|---------------------|-------------|
| `CLAUDE_CODE_OAUTH_TOKEN` | Claude Code CLI OAuth token |

```bash
# Login via Claude Code CLI
claude login

# Or set token directly
export CLAUDE_CODE_OAUTH_TOKEN="your-oauth-token"
```

> **Note**: The SDK uses the bundled CLI for authentication, not direct API calls.
> Reference: https://pypi.org/project/claude-agent-sdk/

## Security Model

### Defense in Depth (Multi-Layer Defense)

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 1: OS-Level Sandbox                                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  - Isolated environment for bash commands              │ │
│  │  - Filesystem escape prevention                        │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Layer 2: Filesystem Restrictions                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  - Limited to project directory (./**)                 │ │
│  │  - Read, Write, Edit tools scoped                     │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Layer 3: Command Allowlist                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  - bash_security_hook validates commands               │ │
│  │  - Only allowed commands can execute                   │ │
│  │  - Extra validation for pkill, chmod, etc.            │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Default Allowed Commands

| Category | Commands |
|----------|----------|
| File Inspection | `ls`, `cat`, `head`, `tail`, `wc`, `grep` |
| File Operations | `cp`, `mkdir`, `chmod` (+x only) |
| Directory | `pwd` |
| Node.js | `npm`, `node`, `npx`, `yarn`, `pnpm` |
| Python | `python`, `pip`, `uv`, `pytest` |
| Git | `git` |
| Process | `ps`, `lsof`, `sleep`, `pkill` (limited) |

## feature_list.json Structure

```json
[
  {
    "id": 1,
    "category": "functional",
    "description": "User can login with email and password",
    "steps": [
      "Step 1: Navigate to login page",
      "Step 2: Enter email",
      "Step 3: Enter password",
      "Step 4: Click login button",
      "Step 5: Verify redirect to dashboard"
    ],
    "passes": false
  },
  {
    "category": "style",
    "description": "Login button has hover effect",
    "steps": [
      "Step 1: Navigate to login page",
      "Step 2: Hover over login button",
      "Step 3: Capture screenshot",
      "Step 4: Verify color change"
    ],
    "passes": false
  }
]
```

### Rules

1. **Immutability**: `description`, `steps` must NEVER be modified
2. **Only allowed change**: `passes: false` → `passes: true` (after verification)
3. **Priority**: Core features ordered first
4. **Test depth**: At least 25 tests should have 10+ steps

## Session Lifecycle

```
┌──────────────────────────────────────────────────────────┐
│                   SESSION LIFECYCLE                       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  START                                                   │
│    │                                                     │
│    ▼                                                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │  1. Orient                                         │  │
│  │     - pwd, ls, git log                             │  │
│  │     - Read claude-progress.txt                     │  │
│  │     - Read feature_list.json                       │  │
│  └────────────────────────────────────────────────────┘  │
│    │                                                     │
│    ▼                                                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │  2. Start Servers (if needed)                      │  │
│  │     - Run ./init.sh                                │  │
│  └────────────────────────────────────────────────────┘  │
│    │                                                     │
│    ▼                                                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │  3. Verify Existing Features (Regression Test)     │  │
│  │     - Test 1-2 passing features                    │  │
│  │     - Mark as false if issues found                │  │
│  └────────────────────────────────────────────────────┘  │
│    │                                                     │
│    ▼                                                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │  4. Implement New Feature                          │  │
│  │     - Select first passes: false feature           │  │
│  │     - Write code                                   │  │
│  │     - Test                                         │  │
│  └────────────────────────────────────────────────────┘  │
│    │                                                     │
│    ▼                                                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │  5. Save State                                     │  │
│  │     - Update feature_list.json                     │  │
│  │     - git commit                                   │  │
│  │     - Update claude-progress.txt                   │  │
│  └────────────────────────────────────────────────────┘  │
│    │                                                     │
│    ▼                                                     │
│  END (Auto-start next session)                           │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## References

- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Claude Agent SDK Documentation](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Autonomous Coding Demo](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)
