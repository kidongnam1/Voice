from __future__ import annotations

import re


_DIGIT_KO = "영일이삼사오육칠팔구"
_NATIVE_COUNTER = {
    1: "한",
    2: "두",
    3: "세",
    4: "네",
}
_NATIVE_HOUR = {
    1: "한",
    2: "두",
    3: "세",
    4: "네",
    5: "다섯",
    6: "여섯",
    7: "일곱",
    8: "여덟",
    9: "아홉",
    10: "열",
    11: "열한",
    12: "열두",
}


def _read_under_10000(number: int) -> str:
    if number == 0:
        return ""
    digits = [1000, 100, 10, 1]
    units = ["천", "백", "십", ""]
    out: list[str] = []
    remainder = number
    for base, unit in zip(digits, units):
        value, remainder = divmod(remainder, base)
        if value:
            if value != 1 or base == 1:
                out.append(_DIGIT_KO[value])
            out.append(unit)
    return "".join(out)


def read_integer(number: int) -> str:
    if number == 0:
        return "영"
    if number < 0:
        return "마이너스 " + read_integer(abs(number))

    large_units = ["", "만", "억", "조"]
    chunks: list[str] = []
    idx = 0
    while number:
        number, chunk = divmod(number, 10000)
        if chunk:
            spoken = _read_under_10000(chunk)
            if chunk == 1 and idx > 0:
                spoken = ""
            chunks.append(spoken + large_units[idx])
        idx += 1
        if idx >= len(large_units) and number:
            raise ValueError("number too large for Phase 1 Korean reader")
    return "".join(reversed(chunks))


def read_decimal(value: str) -> str:
    if "." not in value:
        return read_integer(int(value))
    whole, fraction = value.split(".", 1)
    fraction_spoken = " ".join(_DIGIT_KO[int(ch)] for ch in fraction)
    return f"{read_integer(int(whole))} 점 {fraction_spoken}"


class NumberSemanticParser:
    """Deterministic Phase 1 Korean number/context normalizer."""

    _UNITS = {
        "MB/s": "메가바이트 퍼 세컨드",
        "GHz": "기가헤르츠",
        "MHz": "메가헤르츠",
        "TB": "테라바이트",
        "GB": "기가바이트",
        "MB": "메가바이트",
        "kg": "킬로그램",
        "km": "킬로미터",
        "cm": "센티미터",
        "mm": "밀리미터",
    }

    def normalize(self, text: str) -> str:
        text = re.sub(r"(?<!\d)(\d{4})년", self._replace_year, text)
        text = re.sub(r"(?<!\d)(\d+(?:\.\d+)?)%", self._replace_percent, text)

        for unit in sorted(self._UNITS, key=len, reverse=True):
            pattern = rf"(?<!\w)(\d+(?:\.\d+)?){re.escape(unit)}\b"
            text = re.sub(pattern, self._replace_unit(unit), text)

        text = re.sub(r"(?<!\d)([1-4])(명|개|대)\b", self._replace_native_counter, text)
        text = re.sub(r"(?<!\d)(1[0-2]|[1-9])시\b", self._replace_hour, text)
        return text

    @staticmethod
    def _replace_year(match: re.Match[str]) -> str:
        return f"{read_integer(int(match.group(1)))}년"

    @staticmethod
    def _replace_percent(match: re.Match[str]) -> str:
        return f"{read_decimal(match.group(1))} 퍼센트"

    def _replace_unit(self, unit: str):
        spoken_unit = self._UNITS[unit]

        def repl(match: re.Match[str]) -> str:
            return f"{read_decimal(match.group(1))} {spoken_unit}"

        return repl

    @staticmethod
    def _replace_native_counter(match: re.Match[str]) -> str:
        number = int(match.group(1))
        return f"{_NATIVE_COUNTER[number]} {match.group(2)}"

    @staticmethod
    def _replace_hour(match: re.Match[str]) -> str:
        number = int(match.group(1))
        return f"{_NATIVE_HOUR[number]} 시"
