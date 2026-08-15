# AI NARRATION ENGINE PRD v1.0

- 작성일: 2026-08-15
- 프로젝트: YouTube AI Automation System
- 제품명: AI Narration Engine
- 약칭: ANE
- 버전: v1.0
- 주요 개발 언어: Python 3.12+
- 문자 인코딩: UTF-8

---

## 1. 제품 정의

`AI_NARRATION_ENGINE`은 단순 TTS 프로그램이 아니라, 원고를 사람이 실제로 말하는 것에 가깝게 변환하기 위한 통합 음성 생성 엔진이다.

목표는 다음과 같다.

> 사람이 실제로 말하는 것처럼 문맥을 이해하고, 정확하게 발음하고, 자연스럽게 쉬고, 강조하고, 감정을 조절하며, 생성 결과를 스스로 검사하고 수정하는 AI 음성 생성 시스템을 구축한다.

주요 해결 대상은 다음과 같다.

1. 한글 + 영어 + 숫자 혼합 발음 오류
2. 전문용어·제품명·화학식 오류
3. 숫자·단위·날짜·금액 읽기 오류
4. 기계적인 일정 속도 읽기
5. 문맥과 무관한 Pause
6. 호흡 없는 긴 문장
7. 감정과 강조 부족
8. Voice Clone의 부자연스러움
9. 생성 후 발음 오류 검출 부족
10. 동일 오류 반복 발생

---

## 2. 사용자 경험 목표

사용자는 원본 대본만 입력한다.

예:

```text
삼성전자는 HBM4 12H 제품과 NVIDIA H100을 비교했습니다.
그런데 시장이 주목하는 것은 성능이 아닙니다.
진짜 중요한 것은 가격입니다.
```

시스템은 내부적으로 다음을 수행한다.

```text
원문 분석
  ↓
전문용어·혼합어 탐지
  ↓
숫자·영문·단위 발음 결정
  ↓
문장 의미 분석
  ↓
호흡 구간 결정
  ↓
Pause 위치·길이 결정
  ↓
강조·속도·억양·감정 결정
  ↓
Voice Clone/TTS 생성
  ↓
발음·Pause·오디오 품질 검사
  ↓
문제 구간만 자동 재생성
  ↓
성공 결과 DB 저장
  ↓
최종 오디오
```

---

## 3. 핵심 설계 원칙

### 3.1 Display Text와 Speech Text 분리

원본 대본은 절대로 훼손하지 않는다.

```python
display_text = "삼성전자는 NVIDIA H100과 HBM4를 발표했습니다."
speech_text = "삼성전자는 엔비디아 에이치 백과 에이치비엠 포를 발표했습니다."
```

`display_text`는 자막·제목·설명·원문 보존에 사용하고, `speech_text`는 TTS/Voice Clone 전용으로 사용한다.

### 3.2 Rule First, LLM Last

처리 우선순위는 다음과 같다.

```text
CACHE
  ↓
VERIFIED DB
  ↓
PATTERN
  ↓
DETERMINISTIC RULE
  ↓
G2P / IPA
  ↓
LLM EXCEPTION RESOLVER
```

LLM은 애매한 경우에만 호출한다.

### 3.3 Self-Learning

한 번 성공한 발음·Pause·엔진 설정은 재사용한다.

### 3.4 Segment Retry

한 단어 오류 때문에 전체 오디오를 재생성하지 않는다. 문제 구간만 재생성하고 자연스럽게 이어 붙인다.

---

## 4. 전체 아키텍처

```text
                         ORIGINAL SCRIPT
                                │
                                ▼
                      SEMANTIC ANALYZER
                                │
             ┌──────────────────┴──────────────────┐
             │                                     │
             ▼                                     ▼
   PRONUNCIATION ENGINE                     PROSODY ENGINE
             │                                     │
             └──────────────────┬──────────────────┘
                                ▼
                         VOICE PROFILE
                                │
                                ▼
                         TTS / VOICE CLONE
                                │
                                ▼
                         AUDIO QA ENGINE
                                │
                   ┌────────────┴────────────┐
                   │                         │
                  PASS                      FAIL
                   │                         │
                   ▼                         ▼
              PRODUCTION                SEGMENT RETRY
                                             │
                                             ▼
                                      SELF-LEARNING DB
```

---

## 5. 상위 모듈

```text
AI_NARRATION_ENGINE
│
├── PRONUNCIATION_ENGINE
├── PROSODY_ENGINE
├── AUDIO_QA_ENGINE
├── VOICE_PROFILE_MODULE
├── VOICE_CLONE_MODULE
├── TTS_ENGINE_ROUTER
├── PRONUNCIATION_DATA_FACTORY
├── PROSODY_DATA_FACTORY
├── HUMAN_PROSODY_LEARNING_MODULE
├── YOUTUBE_PROSODY_LEARNING_MODULE
└── SELF_LEARNING_ENGINE
```

---

# PART A. PRONUNCIATION ENGINE

## 6. 목적

`PRONUNCIATION_ENGINE`은 **무엇을 어떻게 읽을 것인가**를 결정한다.

```text
PRONUNCIATION_ENGINE
│
├── UnicodeNormalizer
├── MixedTokenParser
├── LanguageSegmenter
├── EntityClassifier
├── ProtectedTermManager
├── NumberSemanticParser
├── DateTimeParser
├── CurrencyParser
├── UnitParser
├── PronunciationDictionary
├── DomainDictionary
├── PatternDictionary
├── G2PEngine
├── IPAEngine
├── CandidateGenerator
├── CandidateRanker
├── LLMExceptionResolver
└── EngineSpecificFormatter
```

---

## 7. Unicode Normalizer

입력 문자 차이를 정규화한다.

예:

```text
３.５ＧＨｚ → 3.5GHz
㎏ → kg
％ → %
– / — → -
```

---

## 8. Mixed Token Parser

한글·영문·숫자·기호가 섞인 표현을 의미 단위로 분석한다.

```text
Galaxy S25 Ultra 512GB
```

예상 구조:

```json
[
  {"text":"Galaxy","type":"BRAND"},
  {"text":"S25","type":"MODEL"},
  {"text":"Ultra","type":"PRODUCT_NAME"},
  {"text":"512GB","type":"CAPACITY"}
]
```

문자를 바로 읽지 않고 `문자 → 의미 → 발음` 순서로 처리한다.

---

## 9. Entity Classifier

지원 타입:

```text
PERSON
COMPANY
BRAND
PRODUCT
MODEL
AI_MODEL
SOFTWARE_VERSION
SEMICONDUCTOR
CHEMICAL
MEDICAL
FINANCE
LOGISTICS
CONSTRUCTION
DATE
TIME
MONEY
UNIT
PERCENT
PHONE
SERIAL
```

예:

```text
H100
→ type=MODEL
→ domain=semiconductor
→ company=NVIDIA
```

---

## 10. Number Semantic Parser

같은 숫자라도 문맥에 따라 다르게 읽는다.

| 입력 | 발음 예 |
|---|---|
| 4명 | 네 명 |
| 4개 | 네 개 |
| 4kg | 사 킬로그램 |
| 4% | 사 퍼센트 |
| 4시 | 네 시 |
| 4월 | 사월 |
| 4G | 포 지 |
| HBM4 | 에이치비엠 포 |
| GPT-5.6 | 지피티 파이브 포인트 식스 |

지원 타입:

```text
CARDINAL
COUNTER
DATE
TIME
MONEY
PERCENT
DECIMAL
MODEL
VERSION
PHONE
SERIAL
UNIT
CHEMICAL
RANGE
ORDINAL
```

---

## 11. Pattern Dictionary

모든 표현을 DB에 개별 저장하지 않고 패턴으로 처리한다.

```text
GPT-{VERSION}
HBM{GENERATION}
RTX {MODEL}
Galaxy S{MODEL}
```

예:

```text
GPT-8
HBM5
RTX 7090
```

새 모델이 등장해도 규칙으로 처리할 수 있게 한다.

---

## 12. Protected Term Manager

LLM이나 정규화 로직이 고유명사·제품명·화학식을 임의 변경하지 못하도록 보호한다.

예:

```text
GPT-5.6
HBM4
NMC811
Li2CO3
Galaxy S25 Ultra
RTX 5090
```

원문은 유지하고 발음용 별도 alias만 생성한다.

---

## 13. 대규모 Pronunciation DB

### 13.1 Seed DB 목표

```text
V0 Seed          150,000~200,000+
V1 Domain        250,000~350,000+
V2 Entity        500,000+
```

항목 수보다 **출처·정확도·검증 상태**를 우선한다.

### 13.2 분류

```text
PRONUNCIATION MASTER DB
│
├── 한국어 기본 발음
├── 영어 기본 발음
├── 숫자/단위 규칙
├── 기업·브랜드
├── AI/IT
├── 반도체
├── 금융/경제
├── 의학
├── 화학
├── 물류
├── 건축
├── 인명
├── 지명
└── User Custom
```

### 13.3 Seed 데이터 후보

- 국립국어원 한국어 사전/전문용어 API
- CMU Pronouncing Dictionary
- Unicode CLDR 기반 숫자·단위 Locale 데이터
- g2pK 등 한국어 G2P
- 제조사·기관 공식 용어
- 사용자 직접 검증 데이터

각 데이터 소스는 라이선스·출처를 DB에 함께 저장한다.

---

## 14. Source Priority

발음 충돌 시 우선순위:

```text
1. USER_VERIFIED
2. MANUFACTURER / OFFICIAL
3. AUTHORITATIVE_DICTIONARY
4. DOMAIN_DICTIONARY
5. G2P / IPA
6. LLM_INFERENCE
```

---

## 15. Pronunciation DB Schema

권장 DB는 SQLite로 시작하고, 필요시 PostgreSQL로 확장한다.

주요 필드:

```text
term
canonical_term
language
domain
term_type
display_text
speech_text
ipa
arpabet
pattern
context_rule
source
source_url
license
confidence
verification_status
tts_engine
voice_id
usage_count
success_count
failure_count
created_at
updated_at
last_verified_at
```

---

## 16. 발음 후보 생성 및 랭킹

애매한 표현은 여러 후보를 생성한다.

예:

```text
H200
```

후보:

```text
에이치 이백
에이치 투 헌드레드
에이치 이 공 공
```

랭킹 우선순위:

```text
Verified User DB
→ Domain DB
→ Official Rule
→ Deterministic Rule
→ G2P / IPA
→ LLM
```

---

# PART B. PROSODY ENGINE

## 17. 목적

`PROSODY_ENGINE`은 **어디에서 쉬고, 얼마나 쉬고, 어떤 속도·강조·감정으로 말할 것인가**를 결정한다.

```text
PROSODY_ENGINE
│
├── SemanticRoleDetector
├── BreathGroupDetector
├── PauseDetector
├── PauseDurationPredictor
├── SpeakingRateController
├── EmphasisDetector
├── PitchController
├── EnergyController
├── EmotionController
├── RhythmController
├── GenreStyleSelector
├── HumanProsodyMatcher
└── PersonalProsodyProfile
```

---

## 18. Pause 등급

초기값:

| 등급 | 의미 | 기준 |
|---|---|---:|
| P0 | 거의 없음 | 0~100ms |
| P1 | 짧은 호흡 | 150~250ms |
| P2 | 구절 분리 | 250~450ms |
| P3 | 문장 종료 | 450~700ms |
| P4 | 강조/전환 | 700~1,000ms |
| P5 | 극적 쉼 | 1,000~1,800ms |

이 값은 Voice Profile과 장르별로 튜닝한다.

---

## 19. Semantic Role Detector

문장 역할을 먼저 분석한다.

```text
INTRODUCTION
INFORMATION
EXPLANATION
CONTRAST
WARNING
QUESTION
REVEAL
EMPHASIS
SUMMARY
CONCLUSION
CALL_TO_ACTION
```

예:

```text
그런데 중요한 문제가 있습니다.
```

분석:

```text
ROLE=CONTRAST
IMPORTANCE=HIGH
EMOTION=SERIOUS
```

출력 계획:

```text
그런데...
[P4]
중요한 문제가 있습니다.
```

---

## 20. Breath Group Detector

문장이 길더라도 의미 단위로 호흡을 나눈다.

예:

```text
삼성전자는 차세대 HBM4 생산 확대를 통해 /
급증하는 글로벌 AI 반도체 수요에 대응하기 위해 /
올해 하반기부터 /
생산 시설 투자를 확대할 계획입니다.
```

각 `/` 지점에 P1~P2 수준의 호흡을 배치한다.

---

## 21. Prosody 제어 요소

```text
Pause Position
Pause Duration
Breath
Speaking Rate
Pitch
Energy / Volume
Emphasis
Emotion
Rhythm
Sentence-ending Intonation
Hesitation
Phrase Grouping
```

Pause 하나만 조정하지 않고 속도·강조·pitch를 함께 설계한다.

---

## 22. Genre Prosody Profile

지원 장르:

```text
NEWS
DOCUMENTARY
FINANCE_ANALYSIS
TECH_REVIEW
EDUCATION
STORYTELLING
MYSTERY
SHORTS_HIGH_ENERGY
INTERVIEW
LECTURE
COMMERCIAL
CALM_EXPERT
```

각 Profile은 다음을 저장한다.

```text
speaking_rate
pause_duration
pause_frequency
pitch_range
energy
emphasis_strength
emotion_level
breath_frequency
```

---

# PART C. HUMAN / YOUTUBE PROSODY LEARNING

## 23. Human Prosody Learning

목표는 특정 사람의 음색을 복제하는 것이 아니라, 사람이 실제로 말할 때 나타나는 **좋은 전달 패턴**을 추출하는 것이다.

사용 데이터는 자체 제작, 사용 허가, 라이선스가 명확한 음성 중심으로 구성한다.

분석 데이터:

```text
Pause Position
Pause Duration
Speaking Rate
Pitch
Energy
Emphasis
Breath
Rhythm
Emotion
Sentence-ending Intonation
Hesitation
Phrase Grouping
```

---

## 24. Human Prosody Data Factory

```text
LICENSED HUMAN AUDIO
       ↓
AudioSegmenter
       ↓
STT
       ↓
Forced Alignment
       ↓
Pause Extraction
       ↓
Pitch / Rate / Energy Extraction
       ↓
Semantic Context Analysis
       ↓
PROSODY DATABASE
```

---

## 25. 장르별 Prosody Experts

```text
PROSODY_EXPERTS
│
├── NEWS_EXPERT
├── DOCUMENTARY_EXPERT
├── FINANCE_EXPERT
├── TECH_EXPERT
├── EDUCATION_EXPERT
├── STORYTELLING_EXPERT
├── INTERVIEW_EXPERT
├── SHORTS_EXPERT
└── DRAMA_STYLE_EXPERT
```

특정 화자를 그대로 따라 하기보다 여러 화자의 공통 패턴을 추출한다.

---

## 26. YouTube Prosody Learning

유튜브용 별도 학습 계층을 제공한다.

```text
YOUTUBE_PROSODY_LEARNING_MODULE
│
├── TranscriptAligner
├── PauseExtractor
├── BreathExtractor
├── SpeakingRateExtractor
├── PitchExtractor
├── EnergyExtractor
├── EmphasisDetector
├── SemanticRoleDetector
├── GenreClassifier
├── HookDetector
├── StyleNormalizer
└── ProsodyPatternDB
```

목표:

> 특정 유튜버의 목소리를 복제하지 않고, 듣기 편하고 시청 집중을 높이는 전달 패턴을 추출한다.

---

## 27. Personal Prosody Profile

사용자 자신의 자연스러운 실제 음성 20~30분 이상을 분석해 개인 Profile을 만든다.

예:

```python
MY_PROSODY_PROFILE = {
    "default_rate": 0.96,
    "short_pause_ms": 220,
    "phrase_pause_ms": 360,
    "sentence_pause_ms": 590,
    "contrast_pause_ms": 760,
    "reveal_pause_ms": 1050,
    "emphasis_strength": 0.72
}
```

최종 Voice 스타일은 다음을 조합한다.

```text
MY VOICE CLONE
+
MY PROSODY PROFILE
+
HUMAN PROSODY DB
+
GENRE PROSODY EXPERT
+
PRONUNCIATION ENGINE
```

---

# PART D. VOICE CLONE / TTS ROUTING

## 28. Voice Clone Module

역할 구분:

```text
PRONUNCIATION → 어떻게 발음할 것인가
PROSODY       → 어떻게 말할 것인가
VOICE CLONE   → 누구의 목소리로 말할 것인가
```

Voice Clone은 Pronunciation과 Prosody 결정을 대신하지 않는다.

---

## 29. Voice Profile

```text
voice_id
language
default_rate
pitch_bias
energy_bias
pause_profile
pronunciation_override
genre_preferences
```

특정 Voice Clone에서만 잘못 읽는 단어는 Voice-specific override를 저장한다.

---

## 30. TTS Engine Router

한 회사에 종속되지 않는다.

```text
TTS_ENGINE_ROUTER
│
├── ElevenLabs
├── Azure Speech
├── Google Cloud TTS
├── OpenAI-compatible voice engine
└── Local TTS
```

공통 인터페이스 예:

```python
class TTSEngineAdapter:
    def synthesize(self, text, voice_id, prosody):
        raise NotImplementedError

    def supports_ssml(self):
        raise NotImplementedError

    def supports_phoneme(self):
        raise NotImplementedError

    def supports_voice_clone(self):
        raise NotImplementedError
```

---

## 31. Engine-Specific Formatter

내부 표현:

```json
{
  "text": "그런데",
  "pause_after_ms": 750,
  "rate": 0.90,
  "emotion": "serious"
}
```

엔진별 형식으로 변환한다.

SSML 예:

```xml
그런데
<break time="750ms"/>
```

ElevenLabs 계열은 해당 모델이 지원하는 pause/audio tag/발음 사전 기능에 맞게 변환한다.

---

# PART E. AUDIO QA ENGINE

## 32. 목적

`AUDIO_QA_ENGINE`은 **실제로 제대로 발음하고 말했는가**를 검사한다.

```text
AUDIO_QA_ENGINE
│
├── STTVerifier
├── PronunciationVerifier
├── NumberVerifier
├── NamedEntityVerifier
├── PauseVerifier
├── SpeakingRateVerifier
├── SilenceVerifier
├── VolumeVerifier
├── ClippingVerifier
├── RepetitionVerifier
├── ForcedAlignmentVerifier
└── QualityScore
```

---

## 33. STT Round-Trip QA

```text
speech_text
   ↓
TTS
   ↓
audio.wav
   ↓
STT
   ↓
transcribed_text
   ↓
원래 speech_text와 비교
```

예:

```text
목표: 엔비디아 에이치 백
결과: 엔비디아 에이치 일공공
→ FAIL
```

---

## 34. Forced Alignment QA

텍스트와 실제 음성을 단어·음소 단위로 정렬해 다음 문제를 찾는다.

```text
단어 누락
단어 반복
잘린 단어
지나치게 긴 발음
비정상 Pause
잘못된 음소
```

---

## 35. Prosody QA

계획된 Pause와 실제 오디오 Pause를 비교한다.

```text
계획 750ms
실제 160ms
→ FAIL

계획 750ms
실제 710ms
→ PASS
```

허용 오차는 장르·엔진별로 설정한다.

---

## 36. Segment Retry

20분 오디오에서 07:13의 `NMC811`만 틀렸다면 전체를 재생성하지 않는다.

```text
문제 Segment 탐색
  ↓
앞뒤 자연스러운 경계 결정
  ↓
해당 Segment만 재생성
  ↓
Crossfade
  ↓
Audio QA 재검사
  ↓
기존 오디오 교체
```

---

# PART F. SELF-LEARNING

## 37. 저장 대상

```text
발음 성공       → Pronunciation DB
Pause 성공      → Prosody DB
Voice별 성공    → Voice Profile
사용자 수정     → User Override DB
실패 기록       → Failure Pattern DB
```

---

## 38. Learning Priority

```text
USER VERIFIED
  ↓
ENGINE VERIFIED
  ↓
REPEATED SUCCESS
  ↓
DOMAIN DB
  ↓
GLOBAL DB
  ↓
RULE
  ↓
G2P
  ↓
LLM
```

---

## 39. Confidence Score

```text
0.95~1.00 → VERIFIED
0.85~0.94 → HIGH
0.70~0.84 → REVIEW
< 0.70    → RESOLUTION_REQUIRED
```

불확실한 발음은 임의 확정하지 않는다.

---

# PART G. DATA FACTORIES

## 40. Pronunciation Data Factory

```text
PRONUNCIATION_DATA_FACTORY
│
├── SourceCollector
├── LicenseChecker
├── KoreanDictionaryImporter
├── EnglishDictionaryImporter
├── TerminologyImporter
├── BrandEntityImporter
├── PatternGenerator
├── Deduplicator
├── ConflictResolver
├── ConfidenceScorer
├── DBValidator
└── IncrementalUpdater
```

목표는 초기 Seed DB를 자동 구축하고 신규 용어를 지속 갱신하는 것이다.

---

## 41. Prosody Data Factory

```text
PROSODY_DATA_FACTORY
│
├── LicensedAudioCollector
├── AudioSegmenter
├── TranscriptAligner
├── PauseExtractor
├── BreathExtractor
├── PitchExtractor
├── RateExtractor
├── EnergyExtractor
├── EmphasisDetector
├── GenreClassifier
├── SemanticContextAnalyzer
├── StyleNormalizer
└── ProsodyDBBuilder
```

---

# PART H. DATABASE

## 42. 초기 DB 구조

초기에는 SQLite를 사용한다.

```text
data/
├── pronunciation.db
├── prosody.db
├── learning.db
└── voice_profiles.db
```

대규모 서비스화 시 PostgreSQL로 전환 가능하도록 Repository Layer를 분리한다.

### pronunciation.db

```text
terms
pronunciations
patterns
aliases
domains
sources
verification
engine_overrides
usage_stats
```

### prosody.db

```text
pause_patterns
breath_groups
genre_profiles
semantic_roles
pitch_patterns
rate_patterns
emphasis_patterns
human_samples
youtube_patterns
```

### learning.db

```text
corrections
successful_generations
failed_generations
retry_history
user_overrides
qa_scores
```

---

# PART I. PYTHON PACKAGE STRUCTURE

## 43. 권장 구조

```text
ai_narration_engine/
│
├── __init__.py
├── engine.py
├── config.py
│
├── pronunciation/
│   ├── compiler.py
│   ├── tokenizer.py
│   ├── entity_classifier.py
│   ├── number_parser.py
│   ├── unit_parser.py
│   ├── dictionary.py
│   ├── g2p.py
│   ├── ipa.py
│   ├── candidate_ranker.py
│   └── llm_resolver.py
│
├── prosody/
│   ├── director.py
│   ├── semantic_roles.py
│   ├── breath_groups.py
│   ├── pause_predictor.py
│   ├── rate_controller.py
│   ├── emphasis.py
│   ├── emotion.py
│   └── genre_profiles.py
│
├── voice/
│   ├── profile.py
│   ├── clone.py
│   └── router.py
│
├── adapters/
│   ├── elevenlabs.py
│   ├── azure.py
│   ├── google.py
│   └── local.py
│
├── qa/
│   ├── stt.py
│   ├── pronunciation.py
│   ├── pause.py
│   ├── alignment.py
│   ├── audio_quality.py
│   └── segment_retry.py
│
├── learning/
│   ├── pronunciation_learning.py
│   ├── prosody_learning.py
│   └── cache.py
│
├── data_factory/
│   ├── pronunciation_builder.py
│   └── prosody_builder.py
│
├── db/
├── tests/
└── logs/
    └── app.log
```

---

## 44. Main API

외부 프로그램에서는 내부 구조를 몰라도 된다.

```python
from ai_narration_engine import NarrationEngine

engine = NarrationEngine(
    language="ko-KR",
    genre="finance",
    voice_profile="my_voice"
)

result = engine.generate(
    """
    삼성전자는 HBM4 12H 제품과 NVIDIA H100을 비교했습니다.
    그런데 시장이 주목하는 것은 성능이 아닙니다.
    진짜 중요한 것은 가격입니다.
    """
)

print(result.audio_path)
```

반환 항목:

```text
result.display_text
result.speech_text
result.pronunciation_map
result.prosody_plan
result.qa_score
result.retry_count
result.audio_path
```

---

# PART J. LOGGING / DEBUG

## 45. Logging 정책

실행 상태는 화면과 파일에 동시에 기록한다.

```python
print("[NarrationEngine] pronunciation complete")
print("[NarrationEngine] prosody complete")
print("[NarrationEngine] QA score:", score)
```

동시에:

```python
logging.info(...)
logging.warning(...)
logging.error(...)
```

로그 경로:

```text
logs/app.log
```

예외 발생 시 정확한 위치를 남긴다.

```python
import traceback

error = traceback.format_exc()
print(error)
logging.error(error)
```

---

# PART K. 개발 단계

## 46. Phase 1 — MVP Core

```text
Unicode Normalizer
Mixed Token Parser
Number Parser
Unit Parser
Pattern Dictionary
Seed Pronunciation DB
Basic Prosody / Pause
ElevenLabs 또는 선택 TTS Adapter
```

목표: 실제 TTS 음성을 생성할 수 있는 기본 엔진 완성.

---

## 47. Phase 2 — Audio QA

```text
STT Round Trip
Pronunciation QA
Pause QA
Segment Retry
Learning DB
```

목표: 오류 자동 발견 및 문제 구간 재생성.

---

## 48. Phase 3 — Advanced Prosody

```text
Semantic Role
Breath Group
Genre Profile
Speaking Rate
Emphasis
Emotion
Pitch
Rhythm
```

목표: 문맥에 따라 사람처럼 읽는 기능 강화.

---

## 49. Phase 4 — Personal Voice

```text
Voice Clone
My Prosody Profile
My Pronunciation Overrides
Voice-specific DB
```

목표: 사용자 고유 목소리와 말투에 근접.

---

## 50. Phase 5 — Human/YouTube Prosody Learning

```text
Licensed Human Corpus
News-style
Documentary
Interview
Lecture
YouTube-style narration
```

목표: 자연스러운 인간 화법 및 장르별 전달 패턴 학습.

---

## 51. Phase 6 — Self-Improving Engine

```text
Auto Candidate Generation
Auto Retry
Auto QA
Successful Pattern Learning
Failure Pattern Learning
Adaptive Engine Selection
```

목표: 사용할수록 정확도가 높아지는 엔진.

---

# PART L. TEST / QA

## 52. 필수 발음 테스트

```text
GPT-5
GPT-5.6
5G
Galaxy S25 Ultra
RTX 5090
H100
H200
HBM4
HBM4 12H
512GB
3.5GHz
100MB/s
2026년 8월 15일
오후 3시 30분
1명
2명
3명
4명
1개
2개
3개
4개
3.5%
5억원
LiOH
Li2CO3
H2O2
NMC811
```

## 53. Prosody 테스트

```text
하지만 문제가 있습니다.
그런데 중요한 사실이 하나 있습니다.
결국 결과는 완전히 달랐습니다.
진짜 중요한 것은 가격입니다.
왜 이런 일이 벌어진 것일까요?
```

---

# PART M. ACCEPTANCE CRITERIA

## 54. MVP

```text
혼합 텍스트 발음 정확도 ≥ 95%
Seed Dictionary 적용
Basic Pause 적용
Voice Clone 연결 가능
```

## 55. V1

```text
반복 전문용어 정확도 ≥ 98%
STT QA
Segment Retry
Learning DB
Genre Prosody
```

## 56. V2

```text
Verified Dictionary 정확도 ≥ 99%
Forced Alignment
Human Prosody DB
Personal Prosody Profile
Adaptive Pause
```

---

# PART N. KPI

## 57. 핵심 KPI

```text
Pronunciation Accuracy
Pause Accuracy
STT Match Rate
Retry Rate
Audio QA Score
User Correction Rate
Dictionary Hit Rate
LLM Call Rate
Generation Cost
Generation Latency
```

장기 방향:

```text
Dictionary Hit Rate ↑
User Correction Rate ↓
LLM Call Rate ↓
Retry Rate ↓
Audio QA Score ↑
```

---

# PART O. 저작권 / Voice Safety

## 58. Human/YouTube 음성 사용 원칙

- 특정 사람의 목소리를 동의 없이 복제하는 기능은 기본 범위에서 제외한다.
- 뉴스·드라마·영화·유튜브 음성은 음색 복제가 아니라 Pause, Rate, Pitch, Energy, Rhythm 등 일반적 Prosody 패턴 분석을 중심으로 한다.
- 실제 모델 학습 및 데이터셋 구축에는 자체 녹음, 사용 허가 데이터, 라이선스가 명확한 Corpus를 우선한다.
- 데이터 소스마다 출처와 라이선스 메타데이터를 반드시 저장한다.

---

# PART P. 최종 제품 철학

## 59. 실패를 없애는 것이 아니라 실패를 학습한다

목표는 다음이 아니다.

```text
TTS가 한 번도 틀리지 않는다.
```

현실적인 목표는:

```text
틀릴 가능성을 줄인다
  ↓
틀리면 자동으로 찾아낸다
  ↓
틀린 부분만 고친다
  ↓
다시 검사한다
  ↓
성공한 방법을 저장한다
  ↓
같은 오류를 다시 하지 않는다
```

---

## 60. 최종 목표 상태

```text
사람의 좋은 화법
+
사용자의 고유 목소리
+
정확한 전문용어 발음
+
문맥에 맞는 Pause
+
호흡과 리듬
+
장르별 표현
+
자동 QA
+
Self-Learning
```

최종 제품 정의:

> **원고만 입력하면 사람처럼 자연스럽고 정확하게 읽어주는 개인화 AI 내레이터.**

---

# 61. YouTube Automation 전체 연결

```text
TOPIC
  ↓
RESEARCH
  ↓
FACT_CHECK
  ↓
SCRIPT
  ↓
RETENTION
  ↓
MONETIZATION
  ↓
COPYRIGHT
  ↓
AD_SAFETY
  ↓
TTS_DIRECTOR
  ↓
══════════════════════════════════
        AI NARRATION ENGINE
══════════════════════════════════
  │
  ├─ PRONUNCIATION_ENGINE
  ├─ PROSODY_ENGINE
  ├─ VOICE_PROFILE
  ├─ VOICE_CLONE
  ├─ AUDIO_QA_ENGINE
  ├─ SEGMENT_RETRY
  └─ SELF_LEARNING
  │
  ↓
PRODUCTION
  ↓
VIDEO_QA
  ↓
YOUTUBE_UPLOAD
```

---

**END OF PRD v1.0**
