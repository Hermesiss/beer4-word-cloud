import json
import re
from collections import Counter
from os.path import exists

from ignored_words import PRONOUNS, PREPOSITIONS, PARTICLES, CONJUNCTIONS, INTERJECTIONS, NUMERALS, \
    MISC_IGNORE


def extract_text(messages: list) -> list:
    """
    Extracts text from messages and returns a list of words.
    :param messages: List of messages.
    :return: List of words.
    """
    words = []
    for message in messages:
        if "text_entities" in message:
            for entity in message["text_entities"]:
                if "text" in entity:
                    words.extend(re.findall(r'\b\w+\b', entity["text"].lower()))

    ignore = PRONOUNS | PREPOSITIONS | PARTICLES | CONJUNCTIONS | INTERJECTIONS | NUMERALS | MISC_IGNORE
    words = [word for word in words if word not in ignore]
    words = [word for word in words if len(word) > 1]
    words = [word for word in words if not any(char.isdigit() for char in word)]
    return words


def run():
    if not exists("result.json"):
        print("Please place result.json file in the same directory as this script.")
        exit(1)

    with open("result.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    words_list = extract_text(data["messages"])

    word_counts = Counter(words_list)

    with open("word_frequencies.json", "w", encoding="utf-8") as file:
        json.dump(word_counts, file, ensure_ascii=False, indent=4)

    top_50_words = word_counts.most_common(50)
    with open("top_50_words.json", "w", encoding="utf-8") as file:
        json.dump(dict(top_50_words), file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    run()
