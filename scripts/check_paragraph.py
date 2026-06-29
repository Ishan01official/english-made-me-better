from __future__ import annotations

import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.check_sentence import check_sentence


def split_sentences(paragraph: str) -> list[str]:
    text = paragraph.strip()
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [part.strip() for part in parts if part.strip()]


def check_paragraph(paragraph: str) -> dict:
    original = paragraph.strip()
    sentences = split_sentences(original)
    checked = [check_sentence(sentence) for sentence in sentences]
    corrected_sentences = [item["corrected"] for item in checked]

    repeated_words = re.findall(r"\b(\w+)\s+\1\b", original, flags=re.IGNORECASE)
    long_sentences = [
        sentence for sentence in corrected_sentences
        if len(re.findall(r"\b\w+\b", sentence)) > 25
    ]

    clearer_version = " ".join(corrected_sentences)
    professional_version = clearer_version
    professional_version = re.sub(r"\bPlease reply\.\b", "Please reply when you get a chance.", professional_version)

    return {
        "original": original,
        "sentence_count": len(sentences),
        "sentences": checked,
        "repeated_words": repeated_words,
        "long_sentences": long_sentences,
        "clearer_version": clearer_version,
        "professional_version": professional_version,
    }


def format_result(result: dict) -> str:
    lines = [
        "Original:",
        result["original"],
        "",
        f"Sentence count: {result['sentence_count']}",
        "",
        "Corrected sentences:",
    ]
    for idx, item in enumerate(result["sentences"], 1):
        lines.append(f"{idx}. {item['corrected']}")
    lines.extend([
        "",
        "Repeated words:",
        ", ".join(result["repeated_words"]) or "None",
        "",
        "Long sentences:",
        str(len(result["long_sentences"])),
        "",
        "Clearer version:",
        result["clearer_version"],
        "",
        "Professional version:",
        result["professional_version"],
    ])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print('Usage: python scripts/check_paragraph.py "Today morning I completed it. Please revert back."')
        return 1
    result = check_paragraph(" ".join(argv))
    print(format_result(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
