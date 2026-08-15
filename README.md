# Ruby YouTube Revenue Engine

`kidongnam1/Voice`는 YouTube 수익화용 대본을 단순 생성하는 프로그램이 아니라, **기획 → 대본 → 검수 → 재작성 → 제작 → 분석 → 학습**을 반복하는 콘텐츠 최적화 엔진입니다.

## 현재 버전

- Core baseline: v0.6
- Architecture target: v0.7
- Python + Pydantic 기반
- LLM 공급자 교체 가능 구조
- 기본 테스트 포함

## 핵심 실행 흐름

```text
TOPIC
  ↓
TREND_TIMING / CHANNEL_STRATEGY / SEARCH_DISCOVERY
  ↓
AUDIENCE_INTENT / INFORMATION_VALUE / TRUST_AUTHORITY
  ↓
PLANNER → SCRIPT
  ↓
FACT_CHECK / COPYRIGHT / AD_SAFETY / RETENTION
MONETIZATION / ORIGINALITY / EMOTIONAL_ARCH
  ↓
REWRITE_CONTROLLER
  ↓
CTR_PACKAGING → PRODUCTION → SESSION_GROWTH → EXPERIMENTATION
  ↓
HUMAN_REVIEW_GATE
  ↓
UPLOAD → YOUTUBE_ANALYTICS → LEARNING LOOP
```

## 18개 핵심 로직

1. FACT_CHECK_MODULE — 주장·출처·최신성·계산 검수
2. COPYRIGHT_MODULE — 문장·구조·사례 유사도 스크리닝
3. AD_SAFETY_MODULE — 광고 제한 위험 표현 탐지
4. RETENTION_MODULE — 훅·오픈 루프·보상 지점 검수
5. MONETIZATION_MODULE — 광고·제휴·협찬·상품 전환 구조 검수
6. ORIGINALITY_MODULE — 반복·대량 생산 콘텐츠 위험 검수
7. PRODUCTION_MODULE — 화면·자막·TTS·챕터·미드롤 후보 검수
8. AUDIENCE_INTENT_MODULE — 검색·추천·구매·학습 등 시청 의도 분류
9. INFORMATION_VALUE_MODULE — 새로움·실용성·구체성·실행 가능성 평가
10. EMOTIONAL_ARCH_MODULE — 긴장·호기심·반전·보상 감정 곡선 설계
11. SESSION_GROWTH_MODULE — 다음 영상·시리즈·재방문 흐름 최적화
12. EXPERIMENTATION_MODULE — Hook/Title/Thumbnail 변형 실험 설계
13. CHANNEL_STRATEGY_MODULE — 채널 주제 분포·중복·콘텐츠 공백 관리
14. TREND_TIMING_MODULE — 트렌드·계절성·게시 타이밍 평가
15. SEARCH_DISCOVERY_MODULE — 검색/추천 발견 가능성 평가
16. TRUST_AUTHORITY_MODULE — 근거·출처·반대 관점·한계 보강
17. CTR_PACKAGING_MODULE — 제목·썸네일·첫 30초 패키징 일치 최적화
18. REWRITE_CONTROLLER — 실패한 구간만 표적 수정하고 회귀 검사

추가 안전장치: **HUMAN_REVIEW_GATE**. 사실·저작권·광고·고위험 분야에서 자동 게시를 차단하고 사람 검토로 전환합니다.

## 품질 원칙

- 하나의 종합점수만으로 통과시키지 않습니다.
- Retention, 수익성, 독창성, 정책 안전성, 사실성은 별도 Gate로 판단합니다.
- Revenue Score는 실제 RPM/CPM의 확정 예측값이 아니라 상대적인 잠재력 지표입니다.
- Copyright 검사는 법적 판정이 아니라 위험 스크리닝입니다.
- Fact Check는 외부 출처가 연결되지 않은 상태에서 출처를 만들어내지 않습니다.
- Analytics는 상관관계와 반복 패턴을 학습하되 인과관계를 과장하지 않습니다.

## 개발 순서

1. v0.7 — 18개 모듈 Schema + Orchestrator + Rewrite Controller
2. 실제 LLM Adapter 연결
3. 외부 Fact Check 소스 연결
4. YouTube Analytics 연결
5. Ruby Viral Finder 연결
6. ElevenLabs / Vrew / Canva 연동
7. 통합 UI
8. 채널별 Learning Database

## 실행

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
pytest -q
```

## 저장소 원칙

- API Key와 비밀번호는 `.env`에 두고 Git에 올리지 않습니다.
- 중요한 변경은 feature branch → PR → review → merge 방식으로 반영합니다.
- 각 단계 완료 시 `PROJECT_STATUS.md`를 업데이트합니다.
