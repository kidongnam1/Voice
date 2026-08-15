from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class PausePlan:
    text: str
    pause_ms: int
    level: str


class BasicProsodyPlanner:
    """Rule-based Phase 1 pause planner.

    This intentionally avoids attempting expressive prosody. It provides a
    deterministic baseline that later genre/personal prosody models can
    override.
    """

    _PAUSE_BY_MARK = {
        ",": (220, "P1"),
        ";": (320, "P2"),
        ":": (320, "P2"),
        ".": (560, "P3"),
        "?": (650, "P3"),
        "!": (650, "P3"),
    }

    def plan(self, text: str) -> list[PausePlan]:
        pieces = re.split(r"([,;:.?!])", text)
        plans: list[PausePlan] = []
        buffer = ""

        for piece in pieces:
            if not piece:
                continue
            if piece in self._PAUSE_BY_MARK:
                buffer += piece
                pause_ms, level = self._PAUSE_BY_MARK[piece]
                if buffer.strip():
                    plans.append(PausePlan(buffer.strip(), pause_ms, level))
                buffer = ""
            else:
                buffer += piece

        if buffer.strip():
            plans.append(PausePlan(buffer.strip(), 0, "P0"))

        return plans
