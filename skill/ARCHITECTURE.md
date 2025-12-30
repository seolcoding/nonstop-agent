# Autonomous Agent Architecture Guide

Anthropic의 롱 러닝 에이전트 베스트 프랙티스 기반 아키텍처 상세 가이드입니다.

## 핵심 개념

### 1. 2-Agent 패턴

```
┌─────────────────────────────────────────────────────────────┐
│                    SESSION 1 (First Run)                     │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              INITIALIZER AGENT                           │ │
│  │  - app_spec.txt 읽기                                    │ │
│  │  - feature_list.json 생성 (200+ 테스트)                 │ │
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
│  │  4. 브라우저 자동화로 테스트                            │ │
│  │  5. feature_list.json 업데이트                          │ │
│  │  6. Git 커밋                                            │ │
│  │  7. claude-progress.txt 업데이트                        │ │
│  └─────────────────────────────────────────────────────────┘ │
│                              │                               │
│                              ▼                               │
│                     반복 (자동 재시작)                       │
└─────────────────────────────────────────────────────────────┘
```

### 2. 상태 지속성 메커니즘

```
┌─────────────────────────────────────────────────────────────┐
│                    STATE PERSISTENCE                         │
├─────────────────────────────────────────────────────────────┤
│  feature_list.json    ← 기능 체크리스트 (Source of Truth)   │
│  claude-progress.txt  ← 세션별 진행 기록                    │
│  Git History          ← 코드 변경 히스토리                  │
│  app_spec.txt         ← 원본 요구사항 (불변)                │
└─────────────────────────────────────────────────────────────┘
```

### 3. 기존 프로젝트 분석 흐름

```
┌─────────────────────────────────────────────────────────────┐
│                  EXISTING PROJECT ANALYSIS                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Step 1: 프로젝트 구조 파악                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  - README.md, CLAUDE.md 읽기                           │ │
│  │  - package.json / pyproject.toml 확인                  │ │
│  │  - 디렉토리 구조 탐색                                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ↓                                   │
│  Step 2: 기존 요구사항 분석                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  - docs/, specs/ 문서 확인                             │ │
│  │  - GitHub Issues, TODO 주석 수집                       │ │
│  │  - 기존 테스트에서 요구사항 역추론                     │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ↓                                   │
│  Step 3: 테스트 실행 (필수!)                                │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  npm test / pytest / uv run pytest                     │ │
│  │  - 통과/실패 테스트 파악                               │ │
│  │  - 테스트 커버리지 확인                                │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ↓                                   │
│  Step 4: 현재 상태 기록                                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  claude-progress.txt에 초기 분석 결과 기록             │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 인증 (Authentication)

Claude Agent SDK는 번들된 Claude Code CLI를 통해 인증합니다.

| 환경변수 | 설명 |
|----------|------|
| `CLAUDE_CODE_OAUTH_TOKEN` | Claude Code CLI OAuth 토큰 (필수) |

```bash
# Claude Code CLI 로그인 후 토큰 설정
export CLAUDE_CODE_OAUTH_TOKEN="your-oauth-token"

# 또는 Claude Code CLI로 직접 로그인
claude login
```

> **참고**: SDK는 직접 API를 호출하지 않고 번들된 CLI를 사용합니다.
> 참조: https://pypi.org/project/claude-agent-sdk/

## 보안 모델

### Defense in Depth (다중 방어 계층)

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 1: OS-Level Sandbox                                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  - 격리된 환경에서 Bash 명령 실행                      │ │
│  │  - 파일시스템 탈출 방지                                │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Layer 2: Filesystem Restrictions                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  - 프로젝트 디렉토리로 제한 (./**)                     │ │
│  │  - Read, Write, Edit 도구 범위 제한                    │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Layer 3: Command Allowlist                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  - bash_security_hook으로 명령어 검증                  │ │
│  │  - 허용된 명령어만 실행 가능                           │ │
│  │  - pkill, chmod 등 민감한 명령어 추가 검증             │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 허용 명령어 기본 목록

| 카테고리 | 명령어 |
|----------|--------|
| 파일 검사 | `ls`, `cat`, `head`, `tail`, `wc`, `grep` |
| 파일 작업 | `cp`, `mkdir`, `chmod` (+x만) |
| 디렉토리 | `pwd` |
| Node.js | `npm`, `node`, `npx`, `yarn`, `pnpm` |
| Python | `python`, `pip`, `uv`, `pytest` |
| Git | `git` |
| 프로세스 | `ps`, `lsof`, `sleep`, `pkill` (제한적) |

## feature_list.json 구조

```json
[
  {
    "id": 1,
    "category": "functional",
    "description": "사용자가 로그인 페이지에서 이메일/비밀번호로 로그인할 수 있다",
    "steps": [
      "Step 1: 로그인 페이지로 이동",
      "Step 2: 이메일 입력",
      "Step 3: 비밀번호 입력",
      "Step 4: 로그인 버튼 클릭",
      "Step 5: 대시보드로 리다이렉트 확인"
    ],
    "passes": false
  },
  {
    "category": "style",
    "description": "로그인 버튼에 hover 효과가 있다",
    "steps": [
      "Step 1: 로그인 페이지로 이동",
      "Step 2: 로그인 버튼에 마우스 hover",
      "Step 3: 스크린샷 캡처",
      "Step 4: 색상 변경 확인"
    ],
    "passes": false
  }
]
```

### 규칙

1. **불변성**: `description`, `steps`는 절대 수정 금지
2. **유일한 변경**: `passes: false` → `passes: true` (검증 후만)
3. **우선순위**: 핵심 기능부터 순차적으로 정렬
4. **테스트 깊이**: 최소 25개의 테스트는 10+ 단계

## Claude Agent SDK 사용

> **참고**: SDK가 `claude_code_sdk`에서 `claude_agent_sdk`로 이름이 변경되었습니다.

### Python 예시

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, HookMatcher

client = ClaudeSDKClient(
    options=ClaudeAgentOptions(
        model="claude-sonnet-4-5-20250929",
        system_prompt="You are an expert developer...",
        allowed_tools=["Read", "Write", "Edit", "Glob", "Grep", "Bash"],
        hooks={
            "PreToolUse": [
                HookMatcher(matcher="Bash", hooks=[bash_security_hook]),
            ],
        },
        max_turns=1000,
        cwd=str(project_dir),

        # Session resumption support
        resume=resume_session_id,  # Optional: resume from previous session

        # File checkpointing for rewind capability
        enable_file_checkpointing=True,

        # Load CLAUDE.md from project directory
        setting_sources=["project"],

        # Sandbox configuration
        sandbox={
            "enabled": True,
            "autoAllowBashIfSandboxed": True,
            "network": {
                "allowLocalBinding": True,  # Allow dev servers
            }
        },
    )
)

async with client:
    await client.query(prompt)
    async for msg in client.receive_response():
        # 응답 처리
        pass
```

### TypeScript 예시

```typescript
import { ClaudeAgentClient, query } from "@anthropic-ai/claude-agent-sdk";

// Simple query interface
for await (const message of query({
  prompt: "Implement the login feature",
  options: {
    allowedTools: ["Read", "Write", "Edit", "Bash"],
    permissionMode: "acceptEdits",

    // Session resumption
    resume: previousSessionId,

    // File checkpointing
    enableFileCheckpointing: true,

    // Load project settings
    settingSources: ["project"],
  }
})) {
  console.log(message);
}
```

## 세션 관리 (Session Management)

### Session Resumption

에이전트는 세션 ID를 저장하여 이후 세션에서 이전 컨텍스트를 복구할 수 있습니다:

```
┌─────────────────────────────────────────────────────────────┐
│                   SESSION MANAGEMENT                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Session 1 (Fresh Start)                                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  1. 에이전트 실행                                       │ │
│  │  2. 작업 수행                                           │ │
│  │  3. session_id 수신 → claude_session.json 저장          │ │
│  └─────────────────────────────────────────────────────────┘ │
│                          ↓                                    │
│  Session 2 (Resume with --resume flag)                        │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  1. claude_session.json에서 session_id 로드             │ │
│  │  2. resume=session_id로 클라이언트 생성                 │ │
│  │  3. 이전 컨텍스트와 함께 작업 계속                      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### File Checkpointing

`enable_file_checkpointing=True` 옵션으로 파일 변경 이력을 추적하여
필요시 이전 상태로 되돌릴 수 있습니다.

## 세션 라이프사이클

```
┌──────────────────────────────────────────────────────────┐
│                   SESSION LIFECYCLE                       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  START                                                   │
│    │                                                     │
│    ▼                                                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │  1. 환경 파악                                      │  │
│  │     - pwd, ls, git log                             │  │
│  │     - claude-progress.txt 읽기                     │  │
│  │     - feature_list.json 읽기                       │  │
│  └────────────────────────────────────────────────────┘  │
│    │                                                     │
│    ▼                                                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │  2. 서버 시작 (필요시)                             │  │
│  │     - ./init.sh 실행                               │  │
│  └────────────────────────────────────────────────────┘  │
│    │                                                     │
│    ▼                                                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │  3. 기존 기능 검증 (회귀 테스트)                   │  │
│  │     - passes: true인 기능 1-2개 테스트             │  │
│  │     - 문제 발견 시 passes: false로 변경            │  │
│  └────────────────────────────────────────────────────┘  │
│    │                                                     │
│    ▼                                                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │  4. 새 기능 구현                                   │  │
│  │     - passes: false인 첫 번째 기능 선택            │  │
│  │     - 코드 작성                                    │  │
│  │     - 브라우저 자동화로 테스트                     │  │
│  └────────────────────────────────────────────────────┘  │
│    │                                                     │
│    ▼                                                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │  5. 상태 저장                                      │  │
│  │     - feature_list.json 업데이트                   │  │
│  │     - git commit                                   │  │
│  │     - claude-progress.txt 업데이트                 │  │
│  └────────────────────────────────────────────────────┘  │
│    │                                                     │
│    ▼                                                     │
│  END (자동으로 다음 세션 시작)                           │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## 참고 자료

- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Claude Agent SDK Documentation](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Autonomous Coding Demo](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)
