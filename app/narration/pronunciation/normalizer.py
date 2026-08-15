from __future__ import annotations

import re
import unicodedata


class UnicodeNormalizer:
    """Normalize visually equivalent Unicode into stable TTS input."""

    _REPLACEMENTS = {
        "–": "-",
        "—": "-",
        "−": "-",
        "～": "~",
        "％": "%",
        "㎏": "kg",
        "㎞": "km",
    }

    def normalize(self, text: str) -> str:
        normalized = unicodedata.normalize("NFKC", text)
        for source, target in self._REPLACEMENTS.items():
            normalized = normalized.replace(source, target)

        # Preserve newlines, but collapse repeated horizontal whitespace.
        lines = [re.sub(r"[\t ]+", " ", line).strip() for line in normalized.splitlines()]
        return "\n".join(lines).strip()
