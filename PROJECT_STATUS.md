# PROJECT_STATUS

업데이트: 2026-08-15 21:35 KST

## 프로젝트

- Repository: `kidongnam1/Voice`
- Product name: Ruby YouTube Revenue Engine
- Current baseline: v0.6
- Target architecture: v0.7 + AI Narration Engine
- AI Narration PRD: `docs/AI_NARRATION_ENGINE_PRD_v1.0.md` (v1.0 Freeze)
- Active development branch: `phase1-narration-core`

## 완료

- [x] Core Script Schema
- [x] Plan → Draft → Score → Rewrite → Finalize 구조
- [x] Retention Gate
- [x] Revenue / Promise / Originality 구조
- [x] Analytics feedback 기본 Schema
- [x] 7개 전문 Audit 모듈 기본 설계
- [x] 기본 pytest 테스트
- [x] 18개 수익 최적화 로직 최종 아키텍처 정의
- [x] Human Review Gate 정의
- [x] AI Narration Engine 통합 PRD v1.0 작성 및 Freeze
- [x] Phase 1 상세 개발명세 작성
- [x] Phase 1 NarrationEngine API 골격
- [x] Unicode/NFKC Normalizer
- [x] NumberSemanticParser 기본 규칙
- [x] Seed Pronunciation Dictionary 구조
- [x] Basic Prosody/Pause Planner
- [x] Phase 1 pytest 회귀 테스트 작성

## Phase 1 검증 대상

- [ ] GitHub Actions pytest PASS
- [ ] Termux pytest PASS
- [ ] Windows pytest PASS
- [ ] 한글/영어/숫자 혼합 테스트셋 확장
- [ ] Seed 발음사전 대량 구축 파이프라인 설계

## 다음 단계

### AI Narration Engine

- [ ] Phase 1 테스트 결과에 따른 버그 수정
- [ ] TTS Engine Adapter
- [ ] ElevenLabs 연결
- [ ] Voice Profile / Voice Clone
- [ ] STT Audio QA
- [ ] Segment Retry
- [ ] Self-Learning DB
- [ ] Advanced/Human/YouTube Prosody

### 기존 Revenue Engine

- [ ] v0.7 18개 Module Schema 구현
- [ ] Module Orchestrator 구현
- [ ] Rewrite Controller + Regression Check 구현
- [ ] 실제 LLM Adapter 연결
- [ ] Fact Check 외부 소스 연결
- [ ] YouTube Analytics API 연결
- [ ] Ruby Viral Finder 연결
- [ ] ElevenLabs / Vrew / Canva 연결
- [ ] 통합 UI

## 품질 기준

- 테스트 없는 핵심 로직 merge 금지
- Fact/Copyright/Ad Safety 고위험은 Human Review로 이동
- API Key는 저장소에 커밋 금지
- 기능 완료 시 PROJECT_STATUS.md 업데이트
- 발음용 `speech_text`와 원본 `display_text`는 항상 분리
- 외부 API보다 검증 DB/규칙을 우선하고 애매한 경우에만 LLM 사용
