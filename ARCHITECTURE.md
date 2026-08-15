# ARCHITECTURE — Ruby YouTube Revenue Engine v0.7 Target

## 1. Pre-Production Layer

- TREND_TIMING_MODULE
- CHANNEL_STRATEGY_MODULE
- SEARCH_DISCOVERY_MODULE
- AUDIENCE_INTENT_MODULE
- INFORMATION_VALUE_MODULE
- TRUST_AUTHORITY_MODULE

목표: 대본을 쓰기 전에 **누구에게, 왜, 지금, 어떤 각도로 말할지** 확정한다.

## 2. Script Generation Layer

- Planner
- Script Architect
- Hook Writer
- Script Writer
- Emotional Architecture

출력은 자유 텍스트가 아니라 Beat 단위 구조화 데이터로 저장한다.

## 3. Audit Layer

- FACT_CHECK_MODULE
- COPYRIGHT_MODULE
- AD_SAFETY_MODULE
- RETENTION_MODULE
- MONETIZATION_MODULE
- ORIGINALITY_MODULE

각 모듈은 별도의 score/gate/reason/recommendation을 반환한다.

## 4. Rewrite Layer

REWRITE_CONTROLLER는 전체 대본을 무조건 다시 쓰지 않는다.

```text
Audit Failure
  ↓
Failure Classification
  ↓
Target Beat / Section Identification
  ↓
Targeted Rewrite
  ↓
Regression Check
  ↓
Accept / Rollback
```

이미 통과한 영역의 점수가 크게 떨어지면 새 버전을 폐기하고 이전 버전을 유지한다.

## 5. Packaging & Production Layer

- CTR_PACKAGING_MODULE
- PRODUCTION_MODULE
- SESSION_GROWTH_MODULE
- EXPERIMENTATION_MODULE

생성 대상:
- Title A/B/C
- Thumbnail concepts A/B/C
- Voice/TTS script
- Subtitle plan
- B-roll
- Chapter candidates
- Mid-roll candidates
- Next-video bridge

## 6. Human Review Gate

다음 조건에서는 자동 게시 금지:
- Fact check unresolved
- Copyright risk high
- Ad safety high risk
- 의료·법률·금융 등 고위험 정확성 이슈
- 정책 안전성 불명확

## 7. Learning Layer

YouTube Analytics 결과를 Beat와 매핑한다.

```text
Predicted Score
  +
Actual CTR / Retention / Watch Time / Revenue / Subscriber Gain
  ↓
Pattern Learning
  ↓
Channel-specific Writing Rules
```

이 계층은 다음 대본의 Planner와 Rewrite Controller에 피드백한다.
