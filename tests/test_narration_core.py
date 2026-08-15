from app.narration import NarrationEngine
from app.narration.pronunciation.normalizer import UnicodeNormalizer
from app.narration.pronunciation.number_parser import NumberSemanticParser


def test_unicode_normalizer_nfkc_and_symbols():
    normalizer = UnicodeNormalizer()
    assert normalizer.normalize("３.５ＧＨｚ") == "3.5GHz"
    assert normalizer.normalize("10㎏") == "10kg"


def test_seed_dictionary_and_mixed_terms():
    result = NarrationEngine().compile(
        "삼성전자는 NVIDIA H100과 HBM4를 발표했습니다."
    )
    assert result.display_text == "삼성전자는 NVIDIA H100과 HBM4를 발표했습니다."
    assert "엔비디아 에이치 백" in result.speech_text
    assert "에이치비엠 포" in result.speech_text


def test_ai_model_pronunciation():
    result = NarrationEngine().compile("GPT-5.6과 ChatGPT를 비교합니다.")
    assert "지피티 파이브 포인트 식스" in result.speech_text
    assert "챗지피티" in result.speech_text


def test_number_percent_unit_year_and_counter_rules():
    parser = NumberSemanticParser()
    assert parser.normalize("3.5%") == "삼 점 오 퍼센트"
    assert parser.normalize("512GB") == "오백십이 기가바이트"
    assert parser.normalize("2026년") == "이천이십육년"
    assert parser.normalize("4명") == "네 명"
    assert parser.normalize("4시") == "네 시"


def test_basic_pause_plan_is_generated():
    result = NarrationEngine().compile(
        "첫 번째 문장입니다. 그런데 중요한 문제가 있습니다?"
    )
    assert len(result.prosody_plan) == 2
    assert result.prosody_plan[0].level == "P3"
    assert result.prosody_plan[0].pause_ms == 560
    assert result.prosody_plan[1].level == "P3"
    assert result.prosody_plan[1].pause_ms == 650


def test_chemical_seed_terms():
    result = NarrationEngine().compile("LiOH, Li2CO3, H2O2, NMC811")
    assert "수산화리튬" in result.speech_text
    assert "탄산리튬" in result.speech_text
    assert "과산화수소" in result.speech_text
    assert "엔엠씨 팔일일" in result.speech_text


def test_empty_input_rejected():
    engine = NarrationEngine()
    try:
        engine.compile("   ")
    except ValueError as exc:
        assert "must not be empty" in str(exc)
    else:
        raise AssertionError("empty input must raise ValueError")
