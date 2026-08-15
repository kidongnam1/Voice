from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")


class LLMClient(ABC):
    """LLM 공급자를 Pipeline에서 분리하기 위한 인터페이스."""

    @abstractmethod
    def generate(self, *, system: str, user: str, output_model: type[T]) -> T:
        raise NotImplementedError


class MockLLM(LLMClient):
    def generate(self, *, system: str, user: str, output_model: type[T]) -> T:
        raise NotImplementedError("실제 LLM Adapter를 연결하거나 테스트용 FakeLLM을 주입하세요.")
