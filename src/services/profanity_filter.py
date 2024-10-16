import re

# Список заборонених слів (розширте його за потребою)
FORBIDDEN_WORDS = ["shit", "dick", "fuck"]


def contains_profanity(text: str) -> bool:
    text = text.lower()

    for word in FORBIDDEN_WORDS:
        if re.search(r"\b" + re.escape(word) + r"\b", text):
            return True

    return False
