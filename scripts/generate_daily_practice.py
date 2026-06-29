from __future__ import annotations

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def sample(items, count: int):
    return random.sample(items, min(count, len(items)))


def main() -> int:
    grammar = sample(load("grammar_questions.json"), 5)
    vocab = sample(load("vocabulary.json"), 5)
    corrections = sample(load("sentence_correction.json"), 3)
    paragraph = sample(load("paragraph_prompts.json"), 1)[0]
    pronunciation = sample(load("pronunciation_drills.json"), 1)[0]
    speaking_prompts = [
        "Introduce yourself in 60 seconds.",
        "Explain one technical issue simply.",
        "Give a meeting update.",
        "Answer: Tell me about yourself.",
        "Explain what you learned today.",
    ]

    print("# Daily English Practice\n")
    print("## Grammar Questions")
    for item in grammar:
        print(f"- ({item['type']}) {item['question']}")
    print("\n## Vocabulary")
    for item in vocab:
        print(f"- {item['word']}: {item['simple_meaning']}")
    print("\n## Sentence Correction")
    for item in corrections:
        print(f"- Correct this: {item['wrong_sentence']}")
    print("\n## Paragraph Prompt")
    print(f"- {paragraph['prompt']}")
    print("\n## Speaking Prompt")
    print(f"- {random.choice(speaking_prompts)}")
    print("\n## Pronunciation Drill")
    print(f"- {pronunciation['word']} ({pronunciation['IPA']}): {pronunciation['practice_sentence']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
