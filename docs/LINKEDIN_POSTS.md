# Nonstop Agent - LinkedIn 광고 문구 모음

---

## 한국어 버전 (메인 포스팅)

### 🏆 메인 추천 포스팅

```
🎄 클로드 코드 2배 이벤트, 잘 참여하고 계신가요?

저는 솔직히... 못 하고 있었습니다 😅

토큰은 2배인데 제가 프롬프트를 안 치면 의미가 없더라고요.
밥 먹을 때, 회의할 때, 자는 동안... 클로드는 그냥 대기 중.

"이거 자동으로 계속 돌릴 수 없나?"

찾아보니 Anthropic이 이미 해결책을 내놨습니다.

📚 참고한 자료들:
• Anthropic 블로그: "Effective Harnesses for Long-Running Agents"
• 공식 레포: claude-quickstarts/autonomous-coding
• AI Spark Up: "AI 에이전트가 며칠 걸리는 작업을 혼자 완수하는 법"

이걸 Claude Code 스킬로 포팅했습니다.

---

🔥 Nonstop Agent란?

Claude가 24시간 혼자 코딩하게 만드는 자율 에이전트 프레임워크입니다.

• 세션 끊어져도 자동 재개
• Git + progress 파일로 상태 완벽 보존
• 다층 보안 (샌드박스 + 허용목록)

⚙️ 작동 원리:
1️⃣ app_spec.txt에 요구사항 작성
2️⃣ Initializer Agent가 프로젝트 설계 + feature_list.json 생성
3️⃣ Coding Agent가 기능을 하나씩 구현
4️⃣ 완료되면 다음 기능으로 → 무한 반복

---

📦 설치 (1분):

# 1. 스킬 설치
git clone https://github.com/seolcoding/nonstop-agent
cp -r nonstop-agent/skills ~/.claude/skills/

# 2. OAuth 토큰 설정 (필수!)
claude setup-token
# 발급된 토큰을 환경변수에 추가
export CLAUDE_CODE_OAUTH_TOKEN="your-token-here"

🚀 사용법:

Claude Code 열고 이렇게 말하세요:
→ "nonstop agent 만들어줘"
→ "롱 러닝 에이전트로 Todo 앱 개발해줘"
→ "자율 에이전트 실행해줘"

그러면 스킬이 자동으로:
1. 프로젝트 폴더 생성
2. app_spec.txt 기반으로 feature_list.json 작성
3. 기능 구현 시작
4. 끝날 때까지 계속 돌아감

---

퇴근할 때 실행 → 아침에 MVP 완성
(코드 리뷰는 필수입니다 ㅋㅋ Claude도 실수함)

2배 이벤트 12/31까지니까 한번 써보세요!
피드백, PR 언제나 환영입니다 🙌

👉 github.com/seolcoding/nonstop-agent

#ClaudeAI #AI코딩 #자율에이전트 #개발자 #오픈소스 #Anthropic #생산성
```

---

### 짧은 버전 (Twitter/X용)

```
🔥 일해라 클로드!

클로드 2배 이벤트인데 내가 병목이라 토큰을 못 쓰는 게 아쉬웠음

→ Anthropic 공식 가이드 보고 자동화 스킬 만듦
→ 퇴근할 때 실행하면 아침에 기능 완성

github.com/seolcoding/nonstop-agent

#ClaudeAI #자율에이전트
```

---

### 버전 2: 밈 스타일 🤣

```
클로드: "뭐 도와드릴까요?"
나: "..."
클로드: "..."
나: "..."

[3시간 후]

나: "아 맞다 클로드 있었지"

---

이게 저였습니다.

클로드 Pro 결제해놓고 제가 병목이라 토큰 낭비 중... 💸

그래서 만들었습니다.
🔥 Nonstop Agent - 24시간 알아서 코딩하는 스킬

퇴근할 때 "Todo 앱 만들어줘" 하고 실행
→ 아침에 출근하면 MVP 완성

Anthropic 공식 가이드라인 기반이라 안정적!

github.com/seolcoding/nonstop-agent

#ClaudeAI #개발자일상 #자동화 #야근탈출
```

---

### 버전 3: 문제-해결 스타일 💡

```
❌ 문제:
"Claude Pro 결제했는데 내가 안 쓰면 의미없잖아..."

❌ 더 큰 문제:
"세션 끊기면 다시 처음부터 설명해야 함"

❌ 진짜 문제:
"대규모 프로젝트는 하루에 못 끝냄"

---

✅ 해결책: Nonstop Agent

Anthropic이 공식 블로그에서 해결책 공개함:
→ "Effective Harnesses for Long-Running Agents"

핵심 아이디어:
1️⃣ Initializer Agent: 프로젝트 설계
2️⃣ Coding Agent: 기능 구현
3️⃣ Git + JSON으로 상태 저장
4️⃣ 세션 끊어져도 자동 재개

이거 Claude Code 스킬로 포팅했습니다.

📦 github.com/seolcoding/nonstop-agent

지금 클로드 2배 이벤트니까 써보세요!
(12/25~31 홀리데이 프로모션)

#ClaudeAI #Anthropic #개발자 #생산성
```

---

### 버전 4: 스토리텔링 📖

```
어제 퇴근할 때 이랬습니다.

"클로드야, 이 스펙대로 Todo 앱 만들어줘"
[실행]
[퇴근]
[맥주 한잔]
[잠]

오늘 아침 출근해서 봤더니...

✅ FastAPI 백엔드 완성
✅ SQLite DB 연동
✅ 기본 CRUD API
✅ 테스트 코드까지

???

이게 가능했던 이유:
→ Anthropic 공식 "Long-Running Agent" 가이드라인
→ 2-Agent 패턴 (설계 + 구현 분리)
→ Git으로 상태 저장해서 세션 끊어져도 이어서 작업

오픈소스로 공개합니다.

github.com/seolcoding/nonstop-agent

물론 코드 리뷰는 필수입니다 ㅋㅋ
(Claude도 실수함)

#ClaudeAI #자율에이전트 #오픈소스 #개발자
```

---

### 버전 5: 기술 딥다이브 🔧

```
🔧 Claude Code로 24시간 자율 코딩 에이전트 만들기

TL;DR: Anthropic 공식 가이드 → Claude Code 스킬로 포팅

---

📚 레퍼런스:
• anthropic.com/engineering/effective-harnesses-for-long-running-agents
• github.com/anthropics/claude-quickstarts/autonomous-coding
• aisparkup.com/posts/7101

---

⚙️ 아키텍처:

Session 1 (Initializer):
app_spec.txt 읽기 → feature_list.json 생성 → 프로젝트 구조 설정

Session 2, 3, 4... (Coding):
feature_list.json 읽기 → 미완료 기능 선택 → 구현 → 테스트 → passes: true

상태 저장:
• feature_list.json (기능 체크리스트)
• claude-progress.txt (세션 로그)
• Git commits (코드 변경사항)

---

🛡️ 보안 (Defense-in-Depth):
1. OS Sandbox
2. cwd 제한 (프로젝트 폴더만)
3. Bash 허용목록 (rm, curl 차단)

---

📦 설치:
git clone https://github.com/seolcoding/nonstop-agent
cp -r skills ~/.claude/skills/

🚀 실행:
"롱 러닝 에이전트 만들어줘"

---

Claude Agent SDK 0.1.18 기반
MIT License

github.com/seolcoding/nonstop-agent

#ClaudeAgentSDK #Python #오픈소스 #Anthropic
```

---

### 버전 6: 숏폼 (Twitter/Thread용) 🐦

```
🧵 Claude 24시간 코딩시키는 법 (1/5)

클로드 2배 이벤트인데...
내가 안 쓰면 의미없잖아요?

자동으로 계속 돌리는 방법 찾아봤습니다.
👇
```

```
(2/5)
Anthropic이 이미 해결책 공개함:

"Effective Harnesses for Long-Running Agents"

핵심:
• 2개 에이전트 (설계 + 구현)
• Git으로 상태 저장
• 세션 끊어져도 자동 재개
```

```
(3/5)
이걸 Claude Code 스킬로 만들었습니다.

작동 방식:
1. app_spec.txt 작성
2. 스킬 실행
3. 알아서 feature_list.json 생성
4. 기능 하나씩 구현
5. 무한 반복
```

```
(4/5)
보안도 신경 씀:
✅ OS 샌드박스
✅ 프로젝트 폴더만 접근
✅ 위험한 명령어 차단

실수해도 피해 최소화!
```

```
(5/5)
📦 github.com/seolcoding/nonstop-agent

MIT 라이선스
피드백 환영!

홀리데이 이벤트 끝나기 전에 써보세요 🎄
(12/31까지)

#ClaudeAI
```

---

### 버전 7: 직장인 공감 😅

```
월요일 아침 회의:
"이번 주까지 이 기능 가능할까요?"
"네... (불가능)"

---

금요일 퇴근 전:
"클로드야 이거 만들어줘"
[Nonstop Agent 실행]

---

월요일 아침:
"다 됐습니다 :)"
"???"

---

비결: github.com/seolcoding/nonstop-agent

Anthropic 공식 가이드라인 기반
24시간 자율 코딩 에이전트

(코드 리뷰는 해야 함 주의)

#개발자 #야근탈출 #ClaudeAI #자동화
```

---

## English Versions

### 1. Short Version (Under 280 characters)

```
What if coding happened while you sleep?

Nonstop Agent codes 24/7 without stopping.
- Auto-resume when sessions disconnect
- Multi-layer security
- Built on Anthropic best practices

Wake up to completed features.

github.com/seolcoding/nonstop-agent

#AICoding #AutonomousAgent #ClaudeAI #DevProductivity #Automation
```

---

### 2. Medium Version (Under 500 characters)

```
"Start the agent when you leave work. Wake up to completed features."

Introducing Nonstop Agent.

A Claude-powered autonomous coding agent that works while you sleep.

What makes it special?

1. 24/7 Continuous Work
   - Auto-resume on disconnection
   - State preserved via git + progress files

2. Defense-in-Depth Security
   - OS sandbox
   - Filesystem restrictions
   - Command allowlist

3. Anthropic Official Guidelines
   - 2-Agent pattern (Initializer + Coding)
   - Battle-tested best practices

One command to start:
/plugin marketplace add seolcoding/nonstop-agent

Your time is valuable.
Let the agent handle repetitive work.

github.com/seolcoding/nonstop-agent

#AIDevelopment #ClaudeAI #AutonomousAgent #DevOps #DevTools #Automation #Startup #Productivity
```

---

### 3. Long Version (Under 1000 characters)

```
"Coding while you sleep" - Now it's reality.

I'm excited to open-source Nonstop Agent, a project I've been building for months.

The Problem:
AI coding assistants are powerful, but sessions reset when disconnected. For large projects, this inefficiency compounds.

The Solution:
Nonstop Agent implements Anthropic's "Long-Running Agent" best practices.

Key Features:

1. 2-Agent Pattern
   - Initializer Agent: Sets up project in first session
   - Coding Agent: Implements features in subsequent sessions

2. Complete State Persistence
   - feature_list.json: Tracks feature completion
   - claude-progress.txt: Session-by-session notes
   - Git: Version control for all changes

3. Defense-in-Depth Security
   - Layer 1: OS-level sandbox
   - Layer 2: Project directory restrictions
   - Layer 3: Command allowlist only

4. Session Resumption
   --resume flag continues where you left off

Use Case:
- Write app_spec.txt before leaving work
- Start the agent
- Wake up to a working MVP

Tech Stack:
- Claude Opus 4.5
- Claude Agent SDK
- Python / TypeScript support

Get Started:
1. /plugin marketplace add seolcoding/nonstop-agent
2. Write app_spec.txt
3. Run the agent
4. Review results

Looking forward to your feedback!
Stars and Issues welcome!

github.com/seolcoding/nonstop-agent

#AI #MachineLearning #ClaudeAI #AutonomousAgent #Developer #Programming #OpenSource #Startup #DevTools #Automation #Productivity #Coding #SoftwareEngineering #Anthropic
```

---

## 해시태그 모음

### 한국어

```
#AI코딩 #자율에이전트 #ClaudeAI #개발자생산성 #자동화 #AI개발 #DevOps #개발자도구 #프로그래밍자동화 #스타트업 #생산성향상 #오픈소스 #머신러닝 #인공지능 #코딩자동화
```

### English

```
#AICoding #AutonomousAgent #ClaudeAI #DevProductivity #Automation #AIDevelopment #DevOps #DevTools #OpenSource #Startup #Productivity #MachineLearning #SoftwareEngineering #Anthropic #CodingAutomation
```

---

## 이미지 제안

1. **히어로 이미지**: 밤하늘 배경 + 코드가 흐르는 모니터 + "Coding While You Sleep"
2. **다이어그램**: 2-Agent 패턴 플로우차트
3. **스크린샷**: feature_list.json에서 passes: true로 바뀌는 애니메이션
4. **비포/애프터**: 빈 폴더 → MVP 완성된 프로젝트 구조

---

## 게시 팁

1. **최적 시간**: 화~목 오전 8-10시 (한국/미국 시차 고려)
2. **첫 댓글**: 설치 링크와 간단한 튜토리얼 추가
3. **태그**: 관련 개발자 커뮤니티 리더 태그
4. **CTA**: "Star on GitHub" 또는 "Try it now" 명확히

---

## 영감 및 참고 자료 (References)

마케팅 문구에 포함할 수 있는 신뢰성 있는 참고 자료들:

### Anthropic 공식

- **[Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)** - Anthropic 엔지니어링 블로그
- **[Anthropic Claude Quickstarts](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)** - 공식 레퍼런스 구현
- **[Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)** - 공식 SDK 문서

### 커뮤니티 자료

- **[AI Spark Up: AI 에이전트가 며칠 걸리는 작업을 혼자 완수하는 법](https://aisparkup.com/posts/7101)** - 한국어 설명
- **[YouTube Tutorial 1](https://www.youtube.com/watch?v=YW09hhnVqNM)** - 자율 에이전트 개념
- **[YouTube Tutorial 2](https://www.youtube.com/watch?v=o-pMCoVPN_k)** - 롱 러닝 에이전트 데모

### 추천 문구

```
"Anthropic 공식 가이드라인을 기반으로 제작되었습니다."
"Built on Anthropic's official engineering best practices."

참고:
- anthropic.com/engineering/effective-harnesses-for-long-running-agents
- aisparkup.com/posts/7101
```
