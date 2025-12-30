# Nonstop Agent

**Claude를 위한 롱 러닝 자율 에이전트 harness** - 여러 세션에 걸쳐 지속적으로 작업하는 자율 에이전트를 구축하기 위한 프레임워크입니다.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

[English](README.md) | **한국어**

## 개요

Nonstop Agent는 복잡한 프로젝트에서 지속적으로 작업할 수 있는 Claude 기반 자율 에이전트를 실행하기 위한 프로덕션 수준의 프레임워크입니다. Anthropic의 엔지니어링 가이드라인의 베스트 프랙티스를 구현합니다:

- **2-Agent 패턴**: Initializer 에이전트가 프로젝트를 설정하고, Coding 에이전트가 작업을 이어받음
- **상태 지속성**: git + 진행 파일을 통해 세션 간 진행 상황 유지
- **다층 보안**: 샌드박스, 권한, 명령어 허용 목록을 통한 심층 방어
- **세션 재개**: 이전 세션에서 원활하게 작업 계속

## 영감 및 참고 자료

이 프로젝트는 다음을 기반으로 제작되었습니다:

### Anthropic 공식 자료

1. **[Anthropic Engineering: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)**
   - 2-Agent 패턴 (Initializer + Coding)
   - 심층 방어 보안 모델
   - git + 진행 파일을 통한 상태 지속성

2. **[Anthropic Claude Quickstarts - Autonomous Coding](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)**
   - 자율 코딩 에이전트 레퍼런스 구현
   - 진행 추적을 위한 `feature_list.json` 패턴

3. **[Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)**
   - Claude 기반 에이전트 구축을 위한 공식 SDK
   - 훅, 권한, 세션 관리

### 커뮤니티 자료

4. **[AI 에이전트가 며칠 걸리는 작업을 혼자 완수하는 법 (AI Spark Up)](https://aisparkup.com/posts/7101)**
   - Anthropic 2-agent 솔루션 한국어 설명
   - 컨텍스트 윈도우 관리 실용적 인사이트

5. **[YouTube: Claude Code 자율 에이전트 튜토리얼](https://www.youtube.com/watch?v=YW09hhnVqNM)**
   - 자율 에이전트 개념 영상 설명

6. **[YouTube: 롱 러닝 에이전트 구현](https://www.youtube.com/watch?v=o-pMCoVPN_k)**
   - 멀티 세션 에이전트 실전 데모

## 설치

### 옵션 1: Python 패키지로 설치

```bash
# uv 사용 (권장)
uv add nonstop-agent

# 또는 pip 사용
pip install nonstop-agent
```

### 옵션 2: Claude Code 플러그인으로 설치 (권장)

Claude Code에서 마켓플레이스를 통해 직접 설치:

```bash
# 마켓플레이스 추가
/plugin marketplace add seolcoding/nonstop-agent

# 플러그인 설치
/plugin install nonstop-agent@seolcoding/nonstop-agent
```

또는 수동 설치:

```bash
# 레포지토리 클론
git clone https://github.com/seolcoding/nonstop-agent.git

# skills 디렉토리를 Claude Code skills 디렉토리로 복사
cp -r nonstop-agent/skills ~/.claude/skills/nonstop-agent
```

설치 후 Claude Code에서 다음과 같이 호출:
- "롱 러닝 에이전트 만들어줘"
- "자율 에이전트 생성해줘"
- "nonstop agent 만들어줘"
- "Create an autonomous coding agent"

## 빠른 시작

### 1. 인증

에이전트는 OAuth 토큰이 필요합니다:

```bash
# OAuth 토큰 발급
claude setup-token

# 환경변수에 토큰 추가
export CLAUDE_CODE_OAUTH_TOKEN="your-token-here"

# 영구 설정하려면 쉘 프로필에 추가
echo 'export CLAUDE_CODE_OAUTH_TOKEN="your-token-here"' >> ~/.zshrc
```

### 2. 에이전트 실행

**새 프로젝트:**
```bash
# app_spec.txt와 함께 새 프로젝트 생성
uv run nonstop-agent --project-dir ./my_project
```

**기존 프로젝트:**
```bash
# 기존 코드베이스를 먼저 분석
uv run nonstop-agent --project-dir ./existing_project --analyze-first
```

**이전 세션 재개:**
```bash
# 중단된 곳에서 계속
uv run nonstop-agent --project-dir ./my_project --resume
```

### 3. 명령줄 옵션

```
--project-dir PATH      프로젝트 디렉토리 (기본값: ./project)
--model MODEL           사용할 Claude 모델 (기본값: claude-opus-4-5-20251101)
--max-iterations N      최대 반복 횟수 (기본값: 무제한)
--analyze-first         시작 전 기존 프로젝트 분석
--resume                마지막 세션에서 재개
--system-prompt TEXT    에이전트용 커스텀 시스템 프롬프트
```

## 작동 방식

### 세션 흐름

```
┌─────────────────────────────────────────────────────────────┐
│                    세션 1 (첫 실행)                           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              INITIALIZER AGENT                           │ │
│  │  - app_spec.txt 읽기                                    │ │
│  │  - feature_list.json 생성                               │ │
│  │  - 프로젝트 구조 설정                                    │ │
│  │  - Git 초기화 및 첫 커밋                                 │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 세션 2, 3, 4, ... (계속)                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                CODING AGENT                              │ │
│  │  1. 방향 설정: 진행 파일 읽기                            │ │
│  │  2. 검증: 기존 기능 동작 확인                            │ │
│  │  3. 구현: 한 번에 하나의 기능                            │ │
│  │  4. 테스트: 구현 검증                                    │ │
│  │  5. 커밋: git에 진행 상황 저장                           │ │
│  │  6. 반복                                                │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 상태 파일

| 파일 | 목적 |
|------|------|
| `app_spec.txt` | 원본 요구사항 (불변) |
| `feature_list.json` | 기능 체크리스트 (진실의 원천) |
| `claude-progress.txt` | 세션별 진행 노트 |
| `claude_session.json` | 재개용 세션 ID |
| Git 히스토리 | 코드 변경 및 커밋 이력 |

### 보안 계층

```
┌─────────────────────────────────────────────────────────────┐
│  계층 1: OS 수준 샌드박스                                     │
│  - 격리된 bash 명령 실행                                     │
│  - 파일시스템 탈출 방지                                      │
├─────────────────────────────────────────────────────────────┤
│  계층 2: 파일시스템 제한                                      │
│  - 프로젝트 디렉토리로 작업 제한                              │
│  - Read, Write, Edit 도구 범위 지정                         │
├─────────────────────────────────────────────────────────────┤
│  계층 3: 명령어 허용 목록                                     │
│  - 명시적으로 허용된 명령만 실행 가능                         │
│  - 민감한 명령에 대한 추가 검증                              │
└─────────────────────────────────────────────────────────────┘
```

## 커스터마이징

### 커스텀 시스템 프롬프트

```bash
uv run nonstop-agent --project-dir ./project \
  --system-prompt "당신은 전문 Python 개발자입니다..."
```

### 프로그래매틱 사용

```python
import asyncio
from pathlib import Path
from nonstop_agent import run_autonomous_agent

asyncio.run(
    run_autonomous_agent(
        project_dir=Path("./my_project"),
        model="claude-opus-4-5-20251101",
        max_iterations=10,
        analyze_first=True,
    )
)
```

### 허용 명령어 확장

```python
from nonstop_agent.security import add_allowed_command

# 허용 목록에 커스텀 명령어 추가
add_allowed_command("docker")
add_allowed_command("cargo")
```

## feature_list.json 형식

```json
[
  {
    "category": "functional",
    "description": "사용자가 이메일과 비밀번호로 로그인할 수 있다",
    "steps": [
      "1단계: 로그인 페이지로 이동",
      "2단계: 이메일 입력",
      "3단계: 비밀번호 입력",
      "4단계: 로그인 버튼 클릭",
      "5단계: 대시보드로 리다이렉트 확인"
    ],
    "passes": false
  }
]
```

**규칙:**
- `description`과 `steps`는 **불변** - 생성 후 절대 수정하지 않음
- 변경 가능: 검증 후 `"passes": false` → `"passes": true`
- 우선순위 순서: 핵심 기능 먼저

## 기여하기

기여를 환영합니다! 가이드라인은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참조해주세요.

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다 - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 감사의 말

효과적인 에이전트 harness 구축에 대한 훌륭한 문서와 Claude Agent SDK를 제공해주신 Anthropic 팀에 특별히 감사드립니다.
