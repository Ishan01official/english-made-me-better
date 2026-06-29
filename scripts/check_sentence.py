from __future__ import annotations

import re
import sys
from dataclasses import dataclass


@dataclass
class Rule:
    pattern: str
    replacement: str
    mistake: str
    explanation: str
    flags: int = re.IGNORECASE


RULES = [
    Rule(r"\bkindly do the needful\b", "please take the required action", "unclear professional phrase", "Use a direct action request."),
    Rule(r"\bi am having a doubt\b", "I have a question", "Indian English phrase", "Use 'I have a question' in professional English."),
    Rule(r"\bhe do\b", "he does", "subject-verb agreement", "Use 'does' with he/she/it."),
    Rule(r"\bshe do\b", "she does", "subject-verb agreement", "Use 'does' with he/she/it."),
    Rule(r"\bit do\b", "it does", "subject-verb agreement", "Use 'does' with he/she/it."),
    Rule(r"\bI has\b", "I have", "verb form", "Use 'have' with I."),
    Rule(r"\bhe have\b", "he has", "verb form", "Use 'has' with he/she/it."),
    Rule(r"\bshe have\b", "she has", "verb form", "Use 'has' with he/she/it."),
    Rule(r"\bit have\b", "it has", "verb form", "Use 'has' with he/she/it."),
    Rule(r"\bdid not went\b", "did not go", "verb after did", "After 'did', use the base verb."),
    Rule(r"\bdoes not knows\b", "does not know", "verb after does", "After 'does', use the base verb."),
    Rule(r"\bdo not knows\b", "do not know", "verb after do", "After 'do', use the base verb."),
    Rule(r"\bmore better\b", "better", "double comparative", "Use only one comparative form."),
    Rule(r"\bdiscuss about\b", "discuss", "unnecessary preposition", "Use 'discuss the topic', not 'discuss about the topic'."),
    Rule(r"\brevert back\b", "reply", "word choice", "Use 'reply' or 'respond'."),
    Rule(r"\btoday morning\b", "this morning", "time expression", "Use 'this morning'."),
]


PROFESSIONAL_REPLACEMENTS = [
    (r"\bplease reply\b", "Please reply when you get a chance."),
    (r"\bplease take the required action\b", "Please take the required action."),
    (r"\bi have a question\b", "I have a question about this issue."),
]


def _match_case(original: str, replacement: str) -> str:
    if original and original[0].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def check_sentence(sentence: str) -> dict:
    original = sentence.strip()
    corrected = original
    mistakes: list[str] = []
    explanations: list[str] = []

    if "  " in corrected:
        corrected = re.sub(r"\s{2,}", " ", corrected)
        mistakes.append("double spaces")
        explanations.append("Use one space between words.")

    repeated = re.search(r"\b(\w+)\s+\1\b", corrected, flags=re.IGNORECASE)
    if repeated:
        corrected = re.sub(r"\b(\w+)\s+\1\b", r"\1", corrected, flags=re.IGNORECASE)
        mistakes.append("repeated word")
        explanations.append("Remove repeated words.")

    for rule in RULES:
        def repl(match: re.Match) -> str:
            return _match_case(match.group(0), rule.replacement)

        new_value, count = re.subn(rule.pattern, repl, corrected, flags=rule.flags)
        if count:
            corrected = new_value
            mistakes.append(rule.mistake)
            explanations.append(rule.explanation)

    if corrected and corrected[0].islower():
        corrected = corrected[0].upper() + corrected[1:]
        mistakes.append("capitalization")
        explanations.append("Start a sentence with a capital letter.")

    if corrected and corrected[-1] not in ".!?":
        corrected += "."
        mistakes.append("ending punctuation")
        explanations.append("End a sentence with punctuation.")

    professional = corrected
    for pattern, replacement in PROFESSIONAL_REPLACEMENTS:
        if re.search(pattern, professional, flags=re.IGNORECASE):
            professional = re.sub(pattern, replacement, professional, flags=re.IGNORECASE)

    return {
        "original": original,
        "corrected": corrected,
        "mistakes_found": mistakes,
        "explanation": explanations,
        "professional_version": professional,
    }


def format_result(result: dict) -> str:
    explanation = " ".join(result["explanation"]) or "No basic issue found."
    mistakes = ", ".join(result["mistakes_found"]) or "None"
    return (
        f"Original:\n{result['original']}\n\n"
        f"Corrected:\n{result['corrected']}\n\n"
        f"Mistakes found:\n{mistakes}\n\n"
        f"Explanation:\n{explanation}\n\n"
        f"Professional version:\n{result['professional_version']}"
    )


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print('Usage: python scripts/check_sentence.py "He do not knows about this issue"')
        return 1
    result = check_sentence(" ".join(argv))
    print(format_result(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
