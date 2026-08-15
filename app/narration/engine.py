from __future__ import annotations

from dataclasses import dataclass

from .pronunciation.dictionary import PronunciationDictionary
from .pronunciation.normalizer import UnicodeNormalizer
from .pronunciation.number_parser import NumberSemanticParser
from .prosody.basic_pause import BasicProsodyPlanner, PausePlan


@dataclass(frozen=True)
class NarrationResult:
    display_text: str
    speech_text: str
    prosody_plan: tuple[PausePlan, ...]


class NarrationEngine:
    """Phase 1 narration compiler.

    Keeps the display/original text intact while producing a deterministic
    speech-oriented text and a basic pause plan. Audio generation is added in
    later phases.
    """

    def __init__(self) -> None:
        self.normalizer = UnicodeNormalizer()
        self.dictionary = PronunciationDictionary()
        self.number_parser = NumberSemanticParser()
        self.prosody = BasicProsodyPlanner()

    def compile(self, text: str) -> NarrationResult:
        if not isinstance(text, str):
            raise TypeError("text must be str")
        if not text.strip():
            raise ValueError("text must not be empty")

        display_text = text
        normalized = self.normalizer.normalize(text)
        pronounced = self.dictionary.apply(normalized)
        speech_text = self.number_parser.normalize(pronounced)
        prosody_plan = tuple(self.prosody.plan(speech_text))

        return NarrationResult(
            display_text=display_text,
            speech_text=speech_text,
            prosody_plan=prosody_plan,
        )
