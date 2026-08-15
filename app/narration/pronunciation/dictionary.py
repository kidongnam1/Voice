from __future__ import annotations

import json
import re
from pathlib import Path


class PronunciationDictionary:
    """Load UTF-8 seed dictionaries and apply longest-match replacements."""

    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = data_dir or (Path(__file__).resolve().parents[1] / "data")
        self.entries = self._load_entries()

    def _load_entries(self) -> dict[str, str]:
        entries: dict[str, str] = {}
        if not self.data_dir.exists():
            return entries
        for path in sorted(self.data_dir.glob("*.json")):
            with path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
            if not isinstance(payload, dict):
                raise ValueError(f"dictionary must be an object: {path}")
            for key, value in payload.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    raise ValueError(f"dictionary entries must be strings: {path}")
                entries[key] = value
        return entries

    def apply(self, text: str) -> str:
        result = text
        # Longest match first prevents HBM4 from being partially consumed by HBM.
        for term in sorted(self.entries, key=len, reverse=True):
            replacement = self.entries[term]
            pattern = re.compile(rf"(?<![A-Za-z0-9]){re.escape(term)}(?![A-Za-z0-9])")
            result = pattern.sub(replacement, result)
        return result
