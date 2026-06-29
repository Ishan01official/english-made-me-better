from __future__ import annotations

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "ielts" / "data"


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def main() -> int:
    listening = random.choice(load("listening_drills.json"))
    reading = random.choice(load("reading_drills.json"))
    task1 = random.choice(load("writing_task1_prompts.json"))
    task2 = random.choice(load("writing_task2_prompts.json"))
    speaking = random.sample(load("speaking_questions.json"), 3)

    print("# IELTS Daily Practice\n")
    print(f"Listening: {listening['focus']} - {listening['drill']}")
    print(f"Reading: {reading['focus']} - {reading['drill']}")
    print(f"Writing Task 1: {task1['type']} - {task1['prompt']}")
    print(f"Writing Task 2: {task2['prompt']}")
    print("\nSpeaking:")
    for item in speaking:
        print(f"- {item['part']}: {item['question']}")
    print("\nFinish by adding mistakes to ielts/11-error-log.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
