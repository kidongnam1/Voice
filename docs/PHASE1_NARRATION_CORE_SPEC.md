# Phase 1 — AI Narration Core 상세 개발명세

- 작성일: 2026-08-15
- 상위 PRD: `docs/AI_NARRATION_ENGINE_PRD_v1.0.md`
- 브랜치: `phase1-narration-core`
- 목표: 외부 TTS API 없이 발음 전처리와 기본 Prosody 계획을 재현 가능하게 검증한다.

## 1. 범위

Phase 1에 포함한다.

1. Unicode/NFKC 정규화
2. 검증된 Seed 발음 사전
3. 한글+영문+숫자 혼합 표현 변환
4. 숫자·소수·퍼센트·연도·단위·기초 카운터 처리
5. 기본 문장/구절 Pause 계획
6. 단일 `NarrationEngine.compile()` API
7. pytest 회귀 테스트

Phase 1에서 제외한다.

- 실제 음성 합성
- Voice Clone
- STT Round-trip QA
- Forced Alignment
- Human/YouTube Prosody 학습
- LLM 예외 판정

위 기능은 Phase 2 이후에 연결한다.

## 2. 핵심 원칙

- `display_text`는 원문을 보존한다.
- `speech_text`만 발음용으로 변환한다.
- 확실한 규칙과 검증 사전을 LLM보다 우선한다.
- 같은 입력은 항상 같은 결과를 반환해야 한다.
- Termux/Windows/Linux에서 동일한 테스트가 통과해야 한다.

## 3. 처리 순서

```text
Original Text
  ↓
UnicodeNormalizer
  ↓
PronunciationDictionary
  ↓
NumberSemanticParser
  ↓
BasicProsodyPlanner
  ↓
NarrationResult
```

## 4. 공개 API

```python
from app.narration import NarrationEngine

engine = NarrationEngine()
result = engine.compile(
    "삼성전자는 NVIDIA H100과 HBM4를 발표했고 가격은 3.5% 상승했습니다."
)

print(result.display_text)
print(result.speech_text)
print(result.prosody_plan)
```

## 5. Acceptance Criteria

다음 테스트를 자동화한다.

- `３.５ＧＨｚ` → Unicode 정규화
- `NVIDIA H100` → `엔비디아 에이치 백`
- `HBM4` → `에이치비엠 포`
- `GPT-5.6` → `지피티 파이브 포인트 식스`
- `3.5%` → `삼 점 오 퍼센트`
- `512GB` → `오백십이 기가바이트`
- `2026년` → `이천이십육년`
- `4명` → `네 명`
- `4시` → `네 시`
- 마침표/물음표/느낌표 뒤 기본 Pause 계획 생성

## 6. 성공 기준

- 기존 테스트 회귀 없음
- 신규 Phase 1 테스트 전체 PASS
- 외부 API 키 없이 실행 가능
- UTF-8 한글 데이터 정상 로딩
- 실행 중 오류 발생 시 호출자가 원인을 추적할 수 있는 명확한 예외 제공

## 7. 다음 단계

Phase 1 통과 후 순서:

1. TTS Engine Adapter
2. ElevenLabs 연결
3. Voice Profile / Voice Clone
4. STT Audio QA
5. Segment Retry
6. Self-Learning DB
7. Advanced/Human Prosody
