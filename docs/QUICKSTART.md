# Nonstop Agent 빠른 시작 가이드

**5분 안에 자율 코딩 에이전트를 설정하고 실행하세요!**

---

## 1단계: 설치 (1분)

Claude Code에서 아래 명령어를 실행하세요:

```bash
# 마켓플레이스에서 플러그인 추가
/plugin marketplace add seolcoding/nonstop-agent

# 플러그인 설치
/plugin install nonstop-agent@seolcoding/nonstop-agent
```

또는 수동 설치:

```bash
git clone https://github.com/seolcoding/nonstop-agent.git
cp -r nonstop-agent/skills ~/.claude/skills/nonstop-agent
```

---

## 2단계: 인증 설정 (1분)

```bash
# OAuth 토큰 발급
claude setup-token

# 발급된 토큰을 환경변수에 추가
export CLAUDE_CODE_OAUTH_TOKEN="your-token-here"

# 영구 설정하려면 .zshrc 또는 .bashrc에 추가
echo 'export CLAUDE_CODE_OAUTH_TOKEN="your-token-here"' >> ~/.zshrc
```

---

## 3단계: app_spec.txt 작성 (2분)

프로젝트 디렉토리에 `app_spec.txt` 파일을 만드세요:

```bash
mkdir -p my_project
cat > my_project/app_spec.txt << 'EOF'
# 할 일 관리 앱 (Todo App)

## 기능 요구사항

### 핵심 기능
1. 할 일 추가 - 제목과 설명을 입력하여 새 할 일 생성
2. 할 일 목록 조회 - 모든 할 일을 리스트로 표시
3. 할 일 완료 처리 - 체크박스로 완료/미완료 토글
4. 할 일 삭제 - 필요 없는 항목 삭제

### 추가 기능
5. 우선순위 설정 - 높음/중간/낮음
6. 마감일 설정 - 날짜 선택기로 마감일 지정
7. 검색 기능 - 키워드로 할 일 검색

## 기술 스택
- Backend: Python + FastAPI
- Database: SQLite
- Frontend: HTML + Tailwind CSS + htmx

## 비기능 요구사항
- 테스트 커버리지 80% 이상
- 모든 API에 입력 검증
- 반응형 디자인
EOF
```

---

## 4단계: 에이전트 실행 (1분)

### 방법 1: Claude Code 스킬 호출 (권장)

Claude Code에서 다음과 같이 말하세요:

```
"롱 러닝 에이전트 만들어줘"
"nonstop agent로 my_project 개발해줘"
"자율 에이전트로 Todo 앱 만들어줘"
```

### 방법 2: 직접 실행

```bash
# 새 프로젝트 시작
uv run nonstop-agent --project-dir ./my_project

# 기존 프로젝트 분석 후 시작
uv run nonstop-agent --project-dir ./existing_project --analyze-first

# 이전 세션 재개
uv run nonstop-agent --project-dir ./my_project --resume
```

---

## 결과 확인

에이전트가 실행되면 다음 파일들이 생성됩니다:

```
my_project/
├── app_spec.txt           # 원본 요구사항 (불변)
├── feature_list.json      # 기능 체크리스트
├── claude-progress.txt    # 세션별 진행 기록
├── claude_session.json    # 세션 ID (재개용)
├── src/                   # 생성된 소스 코드
└── tests/                 # 테스트 코드
```

### 진행 상황 확인

```bash
# 완료된 기능 수 확인
cat feature_list.json | jq '[.[] | select(.passes == true)] | length'

# 상세 진행 기록 보기
cat claude-progress.txt

# Git 커밋 히스토리 확인
git log --oneline -10
```

### feature_list.json 예시

```json
[
  {
    "category": "functional",
    "description": "할 일 추가 - 제목과 설명을 입력하여 새 할 일 생성",
    "steps": [
      "Step 1: POST /todos API 엔드포인트 생성",
      "Step 2: TodoCreate 스키마 정의",
      "Step 3: 데이터베이스에 저장 로직 구현",
      "Step 4: 단위 테스트 작성 및 실행"
    ],
    "passes": true  // 완료됨!
  },
  {
    "category": "functional",
    "description": "할 일 목록 조회 - 모든 할 일을 리스트로 표시",
    "steps": [...],
    "passes": false  // 아직 구현 중
  }
]
```

---

## 핵심 개념

### 24/7 자율 코딩

Nonstop Agent는 **잠자는 동안에도 코딩**합니다:

1. **세션 1**: Initializer 에이전트가 프로젝트 구조 설정
2. **세션 2, 3, 4...**: Coding 에이전트가 기능을 하나씩 구현
3. **자동 재개**: 세션이 끊어져도 `--resume`으로 이어서 작업

### 상태 지속성

- `feature_list.json`: 기능 완료 여부 추적
- `claude-progress.txt`: 세션별 상세 기록
- Git 커밋: 모든 변경사항 버전 관리

### 다층 보안

```
계층 1: OS 샌드박스 - 격리된 실행 환경
계층 2: 파일시스템 제한 - 프로젝트 디렉토리만 접근
계층 3: 명령어 허용목록 - 승인된 명령만 실행
```

---

## 문제 해결

### "Authentication failed" 오류

```bash
# Claude Code CLI 재로그인
claude login
```

### 에이전트가 멈췄을 때

```bash
# 마지막 세션에서 재개
uv run nonstop-agent --project-dir ./my_project --resume
```

### 진행 상황 초기화

```bash
# 주의: 모든 진행 기록이 삭제됩니다
rm feature_list.json claude-progress.txt claude_session.json
git reset --hard HEAD~N  # N개 커밋 되돌리기
```

---

## 다음 단계

- [상세 문서](ARCHITECTURE.md) - 아키텍처 심층 분석
- [GitHub 저장소](https://github.com/seolcoding/nonstop-agent) - 소스 코드 및 이슈
- [기여 가이드](../CONTRIBUTING.md) - 프로젝트 기여 방법

---

**질문이 있으신가요?** GitHub Issues에 문의해 주세요!
